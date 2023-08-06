import json

import logging
import IPython

from kubeflow.fairing import utils
from kubernetes import client as k8s_client
from kubernetes.client.rest import ApiException

from kubeflow.fairing.notebook import notebook_util

logger = logging.getLogger(__name__)

BENTOML_DEFAULT_PORT = 5000
CURRENT_NAMESPACE = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"


class BentomlServing(object):
    """Serves a bentoml server using Kubernetes deployments and services"""

    def __init__(self, serving_image=None, service_type="LoadBalancer",
                 service_name="bentoml-serving", service_tag="0.0.1",
                 replicas=1, namespace=None, port=BENTOML_DEFAULT_PORT):
        """
        :param serving_image: bentoml serving container image
        :param service_type: service type default LoadBalancer
        :param service_name: service name
        :param service_tag: serving model version
        :param namespace: user's namespace
        :param replicas: server replicas amount
        :param port: serving container port
        """
        self.service_name = utils.get_service_name(service_name)
        self.service_tag = service_tag
        self.serving_image = serving_image
        self.service_type = service_type
        self.port = port
        self.replicas = replicas
        if namespace is None:
            namespace = open(CURRENT_NAMESPACE).read()
        self.namespace = namespace
        self.labels = {}
        self.annotations = {}
        self.api_client = k8s_client.ApiClient(
            utils.get_kubernetes_config_on_pod())

    def _is_exists_deployment(self):
        apps_v1 = k8s_client.AppsV1Api(self.api_client)
        try:
            deploy = apps_v1.read_namespaced_deployment(name=self.service_name,
                                                        namespace=self.namespace)
        except ApiException as e:
            if e.reason == 'Not Found':
                return False
            else:
                print(e)

        return True if deploy is not None else False

    def _get_service_port(self, service):
        service_result = self.api_client.sanitize_for_serialization(service)
        return service_result["spec"]["ports"][0]["nodePort"]

    def get_service_port(self, service_name=None):
        if service_name is None:
            service_name = self.service_name

        v1_api = k8s_client.CoreV1Api(self.api_client)
        svc = v1_api.read_namespaced_service(name=service_name,
                                             namespace=self.namespace)
        return self._get_service_port(svc)

    def go_swagger(self):
        """
        Open swagger browser for Bento API Server
        """
        if not notebook_util.is_in_notebook():
            raise RuntimeError("go_swagger support only in notebook")

        url = 'window.open("http://" + window.location.hostname + ":{}")'
        return IPython.display.Javascript(url.format(self.get_service_port()))

    def _is_exists_service(self):
        v1_api = k8s_client.CoreV1Api(self.api_client)
        try:
            svc = v1_api.read_namespaced_service(name=self.service_name,
                                                 namespace=self.namespace)
        except ApiException as e:
            if e.reason == 'Not Found':
                return False
            else:
                print(e)

        return True if svc is not None else False

    def deploy(self):
        """deploy a bentoml Server service
        """
        self.labels['fairing-id'] = self.service_tag
        self.labels[self.service_name] = self.service_tag
        pod_spec = self.generate_pod_spec()
        pod_template_spec = self.generate_pod_template_spec(pod_spec)
        deployment_spec = self.generate_deployment_spec(pod_template_spec)
        service_spec = self.generate_service_spec()

        job_output = self.api_client.sanitize_for_serialization(deployment_spec)
        logger.warning(json.dumps(job_output))
        service_output = self.api_client.sanitize_for_serialization(
            service_spec)
        logger.warning(json.dumps(service_output))

        v1_api = k8s_client.CoreV1Api(self.api_client)
        apps_v1 = k8s_client.AppsV1Api(self.api_client)
        if self._is_exists_deployment():
            logger.warning("deployment exists!")
        # TODO check service_tag whether match if same tag ignore else patch
        apps_v1.create_namespaced_deployment(self.namespace,
                                             deployment_spec)

        if self._is_exists_service():
            logger.warning("service exists!")

        # TODO check service_tag whether match if same tag ignore else patch
        service = v1_api.create_namespaced_service(self.namespace,
                                                   service_spec)
        port = self._get_service_port(service)

        logging.info("=================================")
        logging.info(f"Serving server AccessPort: {port}")
        logging.info("=================================")
        return port

    def generate_pod_spec(self):
        return k8s_client.V1PodSpec(
            containers=[k8s_client.V1Container(
                name=self.service_name,
                image=self.serving_image,
                security_context=k8s_client.V1SecurityContext(
                    run_as_user=0,
                ),
                ports=[k8s_client.V1ContainerPort(
                    container_port=self.port)
                ],
                env=[k8s_client.V1EnvVar(
                    name='FAIRING_RUNTIME',
                    value='1',
                ),
                ],
            )],
        )

    def generate_pod_template_spec(self, pod_spec):
        """Generate a V1PodTemplateSpec initiazlied with correct metadata
            and with the provided pod_spec

        :param pod_spec: pod spec

        """
        if not isinstance(pod_spec, k8s_client.V1PodSpec):
            raise TypeError('pod_spec must be a V1PodSpec, but got %s'
                            % type(pod_spec))
        if not self.annotations:
            self.annotations = {'sidecar.istio.io/inject': 'false'}
        else:
            self.annotations['sidecar.istio.io/inject'] = 'false'
        self.annotations["prometheus.io/scrape"] = 'true'
        self.annotations["prometheus.io/port"] = str(BENTOML_DEFAULT_PORT)

        return k8s_client.V1PodTemplateSpec(
            metadata=k8s_client.V1ObjectMeta(name=self.service_name,
                                             annotations=self.annotations,
                                             labels=self.labels),
            spec=pod_spec)

    def generate_deployment_spec(self, pod_template_spec):
        """generate deployment spec(V1Deployment)

        :param pod_template_spec: pod spec template

        """
        return k8s_client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=k8s_client.V1ObjectMeta(
                name=self.service_name,
                labels=self.labels,
            ),
            spec=k8s_client.V1DeploymentSpec(
                replicas=self.replicas,
                selector=k8s_client.V1LabelSelector(
                    match_labels=self.labels,
                ),
                template=pod_template_spec,
            )
        )

    def generate_service_spec(self):
        """ generate service spec(V1ServiceSpec)"""
        return k8s_client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=k8s_client.V1ObjectMeta(
                name=self.service_name,
                labels=self.labels,
            ),
            spec=k8s_client.V1ServiceSpec(
                selector=self.labels,
                ports=[k8s_client.V1ServicePort(
                    name="serving",
                    port=BENTOML_DEFAULT_PORT
                )],
                type=self.service_type,
            )
        )

    def _delete_deployment(self):
        try:
            apps_v1 = k8s_client.AppsV1Api(self.api_client)
            del_opts = k8s_client.V1DeleteOptions(
                propagation_policy="Foreground")
            apps_v1.delete_namespaced_deployment(self.service_name,
                                                 self.namespace,
                                                 body=del_opts)
            logger.info("Deleted deployment: {}".format(self.service_name))
        except ApiException as e:
            logger.error(e)
            logger.error(
                "Cannot delete deployment: {}".format(self.service_name))
        finally:
            pass

    def _delete_service(self):
        v1_api = k8s_client.CoreV1Api(self.api_client)
        try:
            v1_api.delete_namespaced_service(self.service_name,
                                             self.namespace)
            logger.info("Deleted service: {}".format(self.service_name))
        except ApiException as e:
            self.error = logger.error(e)
            logger.error(
                "Cannot delete service: {}".format(self.service_name))
        finally:
            pass

    def delete(self):
        self._delete_service()
        self._delete_deployment()

import os
import tarfile
import logging
import posixpath
import tempfile

from kubeflow import fairing
from kubeflow.fairing import utils
from kubeflow.fairing.constants import constants
from kubeflow.fairing.notebook import notebook_util

logger = logging.getLogger(__name__)


class BentomlProcessor(object):
    """Prepares a context that gets sent to the builder for the docker build and sets the entrypoint
    :param bundle_path: full path from local file system under the $BENTOML_HOME(~/bentoml) directory
    :param service_name: bentoml service class name
    :param service_tag: bentoml service tag name
    """

    def __init__(self,
                 path_prefix=constants.DEFAULT_DEST_PREFIX,
                 bundle_path=None,
                 service_name=None,
                 service_tag=None):

        if not notebook_util.is_in_notebook():
            raise RuntimeError("The BentomlProcessor is fit for using in a notebook")
        if bundle_path is not None:
            serivce_dir = bundle_path
        elif service_name is None:
            raise RuntimeError("service_name is empty.")
        elif service_tag is None:
            raise RuntimeError("service_tag is empty.")
        else:
            service_dir = f"/home/jovyan/bentoml/repository/{service_name}/{service_tag}"
        output_map = {}
        for (path, dir, files) in os.walk(service_dir):
            for filename in files:
                full_path = os.path.join(path, filename)
                output_map[full_path] = str(full_path).replace(service_dir, "")
        normalized_map = {}

        for src, dst in output_map.items():
            normalized_map[os.path.normpath(src)] = os.path.normpath(dst)
        self.input_files = []
        self.output_map = normalized_map
        self.path_prefix = path_prefix
        self.external_dockerfile = False

    def is_external_dockerfile(self):
        return self.external_dockerfile
    # TODO: Add workaround for users who do not want to set an executable for
    # their command.
    def set_default_executable(self):  # pylint:disable=inconsistent-return-statements
        """ Set the default executable file.

        :returns: executable: get the default executable file if it is not existing, Or None

        """
        if self.executable is not None:
            return self.executable
        if len(self.input_files) == 1:
            self.executable = list(self.input_files)[0]
            return
        python_files = [item for item in self.input_files if item.endswith(".py")
                        and item is not '__init__.py']  # pylint:disable=literal-comparison
        if len(python_files) == 1:
            self.executable = python_files[0]
            return

    def preprocess(self):
        """ Preprocess the 'input_files'.

        :returns: input_files: get the input files

        """
        return self.input_files

    def context_map(self):
        """ Create context mapping from destination to source to avoid duplicates in context archive

        :returns: c_map: a context map

        """
        c_map = {}
        for src, dst in self.fairing_runtime_files().items():
            if dst not in c_map:
                c_map[dst] = src
            else:
                logging.warning('{} already exists in Fairing context, skipping...'.format(src))

        for f in self.input_files:
            dst = os.path.join(self.path_prefix, f)
            if dst not in c_map:
                c_map[dst] = f
            else:
                logging.warning('{} already exists in Fairing context, skipping...'.format(f))

        for src, dst in self.output_map.items():
            if dst not in c_map:
                c_map[dst] = src
            else:
                logging.warning('{} already exists in Fairing context, skipping...'.format(src))

        return c_map

    def context_tar_gz(self, output_file=None):
        """Creating docker context file and compute a running cyclic redundancy check checksum.

        :param output_file: output file (Default value = None)
        :returns: output_file,checksum: docker context file and checksum

        """
        if not output_file:
            _, output_file = tempfile.mkstemp(prefix="/tmp/fairing_context_")
        logging.info("Creating docker context: %s", output_file)
        self.input_files = self.preprocess()
        with tarfile.open(output_file, "w:gz", dereference=True) as tar:
            for dst, src in self.context_map().items():
                logging.debug("Context: %s, Adding %s at %s", output_file,
                              src, dst)
                tar.add(src, filter=reset_tar_mtime, arcname=dst, recursive=False)
        self._context_tar_path = output_file
        return output_file, utils.crc(self._context_tar_path)

    def get_command(self):
        """ Get the execute with absolute path

        :returns: cmd: the execute with absolute path
        """
        if self.command is None:
            return []
        cmd = self.command.copy()
        if self.executable is not None:
            cmd.append(os.path.join(self.path_prefix, self.executable))
        return cmd

    def fairing_runtime_files(self):
        """Search the fairing runtime files 'runtime_config.py'
        :returns: cmd: the execute with absolute path
        """
        fairing_dir = os.path.dirname(fairing.__file__)
        ret = {}
        for f in ["__init__.py", "runtime_config.py"]:
            src = os.path.normpath(os.path.join(fairing_dir, f))
            dst = os.path.normpath(os.path.join(self.path_prefix, "fairing", f))
            ret[src] = dst
        return ret

    def is_requirements_txt_file_present(self):
        """ Verfiy the requirements txt file if it is present.

        :returns: res: get the present required files

        """
        dst_files = self.context_map().keys()
        reqs_file = posixpath.join(self.path_prefix, "requirements.txt")
        res = reqs_file in dst_files
        return res


def reset_tar_mtime(tarinfo):
    """Reset the mtime on the the tarball for reproducibility.

    :param tarinfo: the tarball var
    :returns: tarinfo: the modified tar ball
    """
    tarinfo.mtime = 0
    return tarinfo

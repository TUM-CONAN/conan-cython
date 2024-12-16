import os

from conan import ConanFile
from conan.tools.files import copy, get, chdir
from conan.tools.layout import basic_layout
from conan.tools.env import Environment

required_conan_version = ">=1.52.0"


class CythonConan(ConanFile):
    python_requires = "camp_common/0.5@camposs/stable"
    python_requires_extend = "camp_common.CampPythonBase"

    package_type = "application"

    name = "cython"
    version = "3.0.11-1"
    license = "Apache"
    description = "Cython language for python3"

    settings = "os", "compiler", "build_type", "arch"


    def build_requirements(self):
        if self._use_custom_python:
            self.requires("cpython/[~{}]".format(self._python_version))
            self.build_requires("python-pip/24.3.1@camposs/stable")
            self.build_requires("python-setuptools/75.6.0@camposs/stable")

    def layout(self):
        basic_layout(self, src_folder="src")

    def generate(self):
        env1 = Environment()
        env1.define("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
        envvars = env1.vars(self)
        envvars.save_script("py_env_file")

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        with chdir(self, self.source_folder):
            self.run('{0} -m pip install --prefix= --root="{1}" .'.format(self._python_exec, self.package_folder))

    def package_info(self):
        self.runenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
        self.buildenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))


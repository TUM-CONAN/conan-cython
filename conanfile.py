import os

from conans import ConanFile, tools


class CythonConan(ConanFile):
    name = "cython"
    version = tools.get_env("GIT_TAG", "0.29.16")
    license = "Apache"
    description = "Cython language for python3"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        tools.get("https://github.com/cython/cython/archive/{0}.tar.gz".format(self.version))

    def build_requirements(self):
        self.build_requires("generators/1.0.0@camposs/stable")

    def requirements(self):
        self.requires("python/[>=3.8.2]@camposs/stable")
        self.requires("python-setuptools/[>=41.2.0]@camposs/stable")

    def build(self):
        py_path = os.path.join(self.package_folder, "lib", "python3.8", "site-packages")
        env = {"PYTHONPATH": os.environ["PYTHONPATH"] + os.pathsep + py_path}
        os.makedirs(py_path)
        with tools.chdir("%s-%s" % (self.name, self.version)), tools.environment_append(env):
            self.run('python3 setup.py install --optimize=1 --prefix= --root="%s"' % self.package_folder)

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python3.8", "site-packages"))

from setuptools import setup
import pkgutil

with open("requirements.txt") as f:
    requires = f.read().splitlines()


def find_packages():
    for loader, module_name, is_pkg in pkgutil.walk_packages(["./dirt_plugins/"], "dirt_plugins."):
        if is_pkg:
            yield module_name
        loader.find_module(module_name).load_module(module_name)


setup(name='dirt-vcs',
      version="1.0.0-alpha",
      description="Dirt Git-based version control plugin",
      author='psrok1',
      packages=list(find_packages()),
      include_package_data=True,
      install_requires=requires,
      zip_safe=False)

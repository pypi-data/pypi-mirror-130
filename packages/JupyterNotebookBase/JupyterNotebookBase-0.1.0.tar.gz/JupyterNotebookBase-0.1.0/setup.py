# -*- coding:utf-8 -*-
import os
from setuptools import find_packages
from setuptools import setup

install_requires = []

exclude_file_patterns = ["*.gif"]
version = {}
with open(os.path.join("JupyterNotebookBase/version.py")) as fp:
    exec(fp.read(), version)

setup(
    name="JupyterNotebookBase",
    version=version["__version__"],
    description="",
    url="",
    author="tiger",
    install_requires=install_requires,
    packages=find_packages(where=".", exclude=exclude_file_patterns),
    package_data={"": ["*.so"]},
    include_package_data=True,
    entry_points={"console_scripts": ["JupyterNotebookBase_setup_jupyter=JupyterNotebookBase.__setup_jupyter__:main"]},
)

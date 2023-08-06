#!/usr/bin/env python

import setuptools

from os import environ, path
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call
from sys import executable

PACKAGE_DIR="ts_dataweave"
PACKAGE_NAME="ts-dataweave"

def download(dest_dir):
    call([executable, "download.py"], cwd=path.join(dest_dir, PACKAGE_DIR))

class PostDevelop(develop):
    def run(self):
        develop.run(self)
        self.execute(download, (self.egg_path,), msg=f"Running post-develop script with path {self.egg_path}")

class PostInstall(install):
    def run(self):
        install.run(self)
        self.execute(download, (self.install_lib,), msg=f"Running post-install script with path {self.install_lib}")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# get version from PACKAGE_DIR/_version.py
with open(path.join(PACKAGE_DIR, "_version.py")) as fh:
    version = fh.read().split('"')[1]

setuptools.setup(
    cmdclass={
        "develop": PostDevelop,
        "install": PostInstall
    },

    name=PACKAGE_NAME,
    version=version,
    description="Python wrapper around MuleSoft DataWeave data transformation engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Ian Cooper",
    author_email="icooper@tetrasience.com",
    url="https://developers.tetrascience.com",
    
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"
    ],
    keywords=[],
    install_requires=[],

    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.7"
)
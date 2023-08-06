from setuptools import setup, find_packages
from os import path

def _requires_from_file(filename):
    return open(filename).read().splitlines()
setup(
name="Ydl",
version="1.3.0",
author='Kerodon',
description='wrapper of YouTube-dl',
packages=find_packages(),
long_description=open('README.md').read(),
long_description_content_type="text/markdown",
install_requires=_requires_from_file('requirements.txt')
)
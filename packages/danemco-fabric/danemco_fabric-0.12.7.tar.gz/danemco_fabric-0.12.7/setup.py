#!/usr/bin/env python
from setuptools import setup, find_packages

exec(open('danemco_fabric/version.py').read())
setup(
    name='danemco_fabric',
    version=__version__,  # noqa: F821
    description="A collection of fabric utils",
    author="Danemco, LLC",
    author_email='dev@velocitywebworks.com',
    url='https://gitlab.com/virgodev/lib/danemco-fabric.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['fabric>=1.7.0,<2', 'requests', 'python-gitlab', 'six'],
)

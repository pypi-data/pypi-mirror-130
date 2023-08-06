#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='bdkpython',
    version='0.0.2',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"bdkpython": ["*.dylib"]},
    include_package_data=True,
    zip_safe=False,
)

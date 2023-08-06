#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='analytics-validator',
    version='0.0.17',
    packages=['validator'],
    scripts=['analytics-validator'],
    install_requires=[
        'pykwalify',
        'arrow',
        'pyyaml',
        'dateformat'
    ],
    include_package_data=True
)

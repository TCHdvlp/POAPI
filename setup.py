#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='sapi',
    version='1.0.0',
    packages=find_packages(exclude=["*_tests"]),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'flask',
        'flask-cors',
        'flask-sqlalchemy',
        'sqlalchemy-utils'
    ]
)
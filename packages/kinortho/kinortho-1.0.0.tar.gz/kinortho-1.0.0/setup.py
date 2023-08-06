#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='kinortho',
    version='1.0.0',
    author='Liang-Chin Huang',
    author_email='Leon1003@gmail.com',
    url='https://github.com/esbgkannan/KinOrtho',
    description='KinOrtho v1.0.0',
    packages=['kinortho'],
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'kinortho=kinortho:kinortho'
        ]
    }
)

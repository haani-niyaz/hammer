#!/usr/bin/python
# -*- coding: utf-8 -*-

from ducttape import __version__
from setuptools import setup, find_packages

setup(
    name='ducttape',
    version=__version__,
    author='Haani Niyaz',
    author_email='haani.niyaz@gmail.com',
    url='https://github.com/haani-niyaz/ducttape',
    license='MIT',
    description='A hacky utility tool to wrangle Kubernetes and an external cloud management system',
    keywords='automation helper',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'ducttape=ducttape.__main__:main',
        ],
    },
)

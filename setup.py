#!/usr/bin/python
# -*- coding: utf-8 -*-

from hammer import __version__
from setuptools import setup, find_packages

setup(
    name='hammer',
    version=__version__,
    author='Haani Niyaz',
    author_email='haani.niyaz@gmail.com',
    url='https://github.com/haani-niyaz/hammer',
    license='MIT',
    description='A hacky utility tool to wrangle Kubernetes',
    keywords='automation helper',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'hammer=hammer:main',
        ],
    },

)

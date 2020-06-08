#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io

from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='gophr-s2ds-project',
    version='0.1.0',
    # license='MIT license',
    description='Predict likelihood of job assignment acceptance',
    long_description=read('README.md'),
    author='Team Gophr @ S2DS',
    # author_email='example@example.net',
    url='https://bitbucket.org/s2ds-gophr-it/s2ds/',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=['numpy', 'matplotlib', 'pandas', 'mysql-connector', 'scikit-learn']
)


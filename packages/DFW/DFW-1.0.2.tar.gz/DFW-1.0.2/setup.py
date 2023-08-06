#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Alrash
# @Email: kasukuikawai@gmail.com

from setuptools import setup, find_packages

setup(
    name='DFW',
    packages=find_packages(),
    version='1.0.2',
    install_requires=[          # 添加了依赖的 package
        'scipy',
        'h5py',
        'sklearn',
        'numpy'
    ]
)

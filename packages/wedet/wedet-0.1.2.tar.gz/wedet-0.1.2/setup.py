#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import setuptools
import glob
import os


with open("wedet/__init__.py", "r") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(), re.MULTILINE
    ).group(1)


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_package_data():
    data = []
    data.append('structures/class_desc/*.txt')
    data.append('structures/class_desc/class_trans/*.txt')
    return {'wedet': data}


setuptools.setup(
    name="wedet",
    version=version,
    author="jario&team",
    author_email="jariof@foxmail.com",
    python_requires=">=3.6",
    long_description=long_description,
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
    package_dir={'wedet': 'wedet'},
    package_data=get_package_data(),
    packages=setuptools.find_packages(),
)

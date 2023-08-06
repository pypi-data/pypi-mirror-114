#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 12:03 下午
# @Author  : jianwei.lv

import setuptools
from weimobUI import __author__, __email__, __version__

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="weimob-ui",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=("ui自动化框架"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['selenium', 'pytest', 'openpyxl', 'pytest-html'],
    python_requires=">=3.6",

    entry_points={'console_scripts': [
        f' WeimobUi= weimobUI.__main__:main',
     ]},

    zip_safe=False
)

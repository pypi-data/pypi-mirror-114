#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="sztutil",
    version="0.0.6",
    author="Chen chuan",
    author_email="kcchen@139.com",
    description="深证通辅助工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/chenc224/sztutil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    scripts=["bin/sztutil"],
    zip_safe= False,
    include_package_data = True,
)

#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


import setuptools  # 导入setuptools打包工具



setuptools.setup(
    name="checkAuthByNet",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.3.1",  # 包版本号，便于维护版本
    author="golango",  # 作者，可以写自己的姓名
    author_email="nbotu666@gmail.com",  # 作者联系方式，可写自己的邮箱地址
    description="A small example package",  # 包的简述
    long_description="time and path tool",
    long_description_content_type="text/markdown",
    url="https://github.com/phpnbw",  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
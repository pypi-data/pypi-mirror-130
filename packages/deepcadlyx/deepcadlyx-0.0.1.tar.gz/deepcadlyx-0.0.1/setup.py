# -*- coding: utf-8 -*-
#############################################
# File Name: setup.py
# Author: Yixin Li
# Mail: 20185414@stu.neu.edu.cn
# Created Time:  2021-12-10
#############################################
from setuptools import setup, find_packages


# with open("README.rst") as f:
#     readme = f.read()
#
# with open("LICENSE") as f:
#     license = f.read()

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

setup(
    name="deepcadlyx",
    version="0.0.1",
    description=("implemenent deepcad to denoise data by "
                 "removing independent noise"),
    long_description="lyx testing...",
    author="YixinLi",
    author_email="20185414@stu.neu.edu.cn",
    url="https://github.com/STAR-811",
    license="MIT Licence",
    packages=find_packages(),
    install_requires=required,
)

#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import call

setup(
    name = 'mpyzeebe',
    version = '0.0.7',
    keywords='wx',
    description = 'a library for nmap scan',
    license = 'MIT License',
    url = 'https://192.168.1.146:8081/repo/packages',
    author = 'superman',
    author_email = '646390966@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
"oauthlib==3.1.0", "requests-oauthlib==1.3.0", "zeebe-grpc==0.26.0.0"],
)


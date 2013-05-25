#!/usr/bin/env python

from setuptools import setup

setup(
    name='health-search',
    version='1.0',
    description='Dig up similar health issue summaries',
    author='Shoubhik Bose',
    author_email='sbose78@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.3','pymongo>=2.5'],
)

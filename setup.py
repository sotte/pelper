#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pelper",
    description="pelper - python helper functions",
    long_description=read("README.rst"),
    author="Stefan Otte",
    url="https://github.com/sotte/pelper",
    download_url="https://github.com/sotte/tcr",
    author_email="stefan.otte@gmail.com",
    version="0.0.1",
    install_requires=[],
    packages=["pelper"],
    scripts=[],
    license="MIT",
)

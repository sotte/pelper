#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
    long_description = f.read()


setup(
    name="pelper",

    version="0.0.2",

    description="pelper - python helper functions",
    long_description=long_description,

    author="Stefan Otte",
    author_email="stefan.otte@gmail.com",

    license="MIT",

    url="https://github.com/sotte/pelper",
    download_url="https://github.com/sotte/NAME",

    keywords="development heper decorator contextmanager",

    packages=["pelper"],
    # install_requires=["sphinxcontrib-napoleon", ],
)

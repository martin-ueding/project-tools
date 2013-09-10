#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

from distutils.core import setup

__docformat__ = "restructuredtext en"

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    classifiers = [
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    description = "Finds non Python 3 scripts",
    download_url = "http://martin-ueding.de/download/python-find2/",
    name = "python-find2",
    scripts = ["python-find2"],
    url = "http://martin-ueding.de/projects/python-find2/",
    version = "1.0",
)

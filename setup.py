#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

setup(
    name = "projecttools",
    version = "1.9",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'git-autogc = projecttools.gitautogc:main',
            'git-autopush = projecttools.gitautopush:main',
            'git-repo-merge = projecttools.gitrepomerge:main',
            'github-repo-count = projecttools.githubrepocount:main',
            'ppa = projecttools.ppa:main',
            'python-find2 = projecttools.find2:main',
        ],
    },
    install_requires=[
        'termcolor'
    ],
)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2015 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

setup(
    name="projecttools",
    version="1.12",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'git-autogc = projecttools.gitautogc:main',
            'git-autopush = projecttools.gitautopush:main',
            'git-init-chaos = projecttools.gitinit:entry_init_chaos',
            'git-init-default = projecttools.gitinit:entry_init_default',
            'git-init-github = projecttools.gitinit:entry_init_github',
            'git-release-tar = projecttools.git.releasetar:main',
            'git-repo-merge = projecttools.gitrepomerge:main',
            'git-spull = projecttools.git:submodule_pull',
            'github-repo-count = projecttools.githubrepocount:main',
            'osc-auto-updater = projecttools.osc:main',
            'ppa = projecttools.ppa:main',
            'prolint = projecttools.lint.__init__:main',
            'python-find2 = projecttools.find2:main',
        ],
    },
    install_requires=[
        'requests',
        'termcolor',
    ],
)

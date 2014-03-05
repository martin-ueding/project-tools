#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import subprocess

__docformat__ = "restructuredtext en"

def spull():
    subprocess.check_call(['git', 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'])

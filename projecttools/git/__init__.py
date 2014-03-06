#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import os.path
import subprocess

__docformat__ = "restructuredtext en"

def submodule_pull():
    subprocess.check_call(['git', 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'])

def get_tags():
    return subprocess.check_output(['git', 'tag']).decode().strip().split()

def get_toplevel():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()

def get_project_name(path):
    return os.path.basename(path)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import subprocess

__docformat__ = "restructuredtext en"

def submodule_pull():
    subprocess.check_call(['git', 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'])

def remove_duplicate_remote(remote):
    remotes = subprocess.check_output(['git', 'remote']).decode().split()
    if remote in remotes:
        logger.warning('This already has remote “{}”.'.format(remote))
        subprocess.check_call(['git', 'remote', 'rm', remote])

def add_push_mirror(remote, url):
    subprocess.check_call(['git', 'remote', 'add', remote, url, '--mirror=push'])

def push_remote(remote):
    subprocess.check_call(['git', 'push', remote])

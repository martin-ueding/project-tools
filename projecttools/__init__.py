#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

import os.path
import subprocess
import glob

__docformat__ = "restructuredtext en"

def find_git_repos(root='~'):
    dirs = glob.glob(os.path.join(os.path.expanduser(root), '*'))
    if root == '~':
        dirs += [os.path.expanduser(x) for x in ['~/.vim', '~/.config']]

    command = [
        'find'
    ] + dirs + [
        '-type', 'd',
        '-name', '.git',
        '-print0',
    ]

    output = subprocess.check_output(command)
    repos = [repo.decode() for repo in output.split(b'\0')[:-1]]
    return repos

if __name__ == '__main__':
    print(find_git_repos('~/.vim'))

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

import glob
import configparser
import os.path
import subprocess

__docformat__ = "restructuredtext en"

def get_config():
    configfile = os.path.expanduser('~/.config/project-tools/conf.ini')
    config = configparser.ConfigParser()
    config.read(configfile)

    return config

def find_git_repos(root='~'):
    '''
    Finds git repos in the given path.

    Uses ``find`` to find all directories that end with ``.git`` and lists
    them. It uses zero-separated strings, which makes it safe for any file
    name.

    :param root: Starting point
    :type root: str
    '''
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

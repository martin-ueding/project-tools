#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import logging
import json
import subprocess
import sys

import requests

import projecttools

__docformat__ = "restructuredtext en"

logger = logging.getLogger(__name__)

def remove_duplicate_remote(remote):
    remotes = subprocess.check_output(['git', 'remote']).decode().split()
    if remote in remotes:
        logger.warning('This already has remote “{}”.'.format(remote))
        subprocess.check_call(['git', 'remote', 'rm', remote])

def add_push_mirror(remote, url):
    subprocess.check_call(['git', 'remote', 'add', remote, url, '--mirror=push'])

def push_remote(remote):
    subprocess.check_call(['git', 'push', remote])

def init_chaos(name):
    subprocess.check_call(['ssh', 'chaos', '/home/mu/bin/create-bare', name])
    remove_duplicate_remote('chaos')
    add_push_mirror('chaos', 'chaos:public_html/git/{}.git'.format(name))
    push_remote('chaos')


def init_github(name):
    config = projecttools.get_config()

    github_user = config['GitHub']['user']
    github_pass = config['GitHub']['password']

    data = {'name': name}

    r = requests.post('https://api.github.com/user/repos', data=json.dumps(data), auth=(github_user, github_pass))
    j = r.json()
    if not r.status_code == requests.codes.ok:
        for error in j['errors']:
            logger.error(error['message'])
        sys.exit(1)

    print('GitHub page:', j['html_url'])

    remove_duplicate_remote('github')
    add_push_mirror('github', 'git@github.com:{}/{}.git'.format(github_user, name))
    push_remote('github')

def entry_init_chaos():
    options = _parse_args()
    init_chaos(options.name)

def entry_init_github():
    options = _parse_args()
    init_github(options.name)

def entry_init_default():
    options = _parse_args()
    init_github(options.name)
    init_chaos(options.name)

def main():
    options = _parse_args()


def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("name", help="Name of the repository on the remote.")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")
    parser.add_argument("-v", dest='verbose', action="count", help='Enable verbose output. Can be supplied multiple times for even more verbosity.')

    options = parser.parse_args()

    # Try to set the logging level in case the logging module is imported.
    try:
        if options.verbose == 1:
            logging.basicConfig(level=logging.INFO)
        elif options.verbose == 2:
            logging.basicConfig(level=logging.DEBUG)
    except NameError as e:
        pass

    return options

if __name__ == "__main__":
    main()

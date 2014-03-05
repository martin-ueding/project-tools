#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import logging
import json
import subprocess
import pprint

import requests

import projecttools

__docformat__ = "restructuredtext en"

logger = logging.getLogger(__name__)

def init_github():
    options = _parse_args()
    config = projecttools.get_config()

    pp = pprint.PrettyPrinter()
    github_user = config['GitHub']['user']
    github_pass = config['GitHub']['password']

    data = {'name': options.name}

    r = requests.post('https://api.github.com/user/repos', data=json.dumps(data), auth=(github_user, github_pass))
    j = r.json()
    pp.pprint(j)

    print('GitHub page:', j['html_url'])

    remotes = subprocess.check_output(['git', 'remote']).decode().split()

    if 'github' in remotes:
        logger.warning('“{}” already has remote “github”.'.format(options.name))
        subprocess.check_call(['git', 'remote', 'rm', 'github'])

    subprocess.check_call(['git', 'remote', 'add', 'github', 'git@github.com:{}/{}.git'.format(github_user, options.name), '--mirror=push'])
    subprocess.check_call(['git', 'push', 'github'])

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

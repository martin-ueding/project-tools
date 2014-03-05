#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

"""
Retrieves a list of GitHub repositories with the GitHub API and counts them.
"""

import argparse

import requests

__docformat__ = "restructuredtext en"

def main():
    options = _parse_args()

    r = requests.get("https://api.github.com/users/{}".format(options.username))
    data = r.json()
    print(data['public_repos'])


def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("username", metavar="user", type=str, nargs="?", default="martin-ueding", help="Username")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()


if __name__ == "__main__":
    main()

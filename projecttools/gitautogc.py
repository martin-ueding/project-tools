#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

import argparse
import os
import subprocess

import projecttools

__docformat__ = "restructuredtext en"


def main():
    options = _parse_args()

    repos = projecttools.find_git_repos()

    for repo in repos:
        os.chdir(repo)
        print(repo)
        subprocess.call(['git', 'gc'])

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    #parser.add_argument("args", metavar="N", type=str, nargs="*", help="Positional arguments.")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()


if __name__ == "__main__":
    main()

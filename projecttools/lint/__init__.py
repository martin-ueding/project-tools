#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import glob
import concurrent.futures
import os

import requests

import projecttools.git

__docformat__ = "restructuredtext en"

class Check(object):
    @staticmethod
    def glob_exists(*patterns):
        for pattern in patterns:
            if len(glob.glob(pattern)) > 0:
                return True
        return False

    def test_and_return_message(self):
        if not self.succeeds():
            return self.message

class UrlExistsCheck(Check):
    def succeeds(self):
        r = requests.get(self.url)
        return r.status_code == requests.codes.ok

class CheckChangelog(Check):
    message = 'no-changelog'

    def succeeds(self):
        return self.glob_exists('CHANGELOG*', 'changelog*')

class CheckChaos(UrlExistsCheck):
    message = 'no-chaos'

    def __init__(self):
        name = projecttools.git.get_project_name(os.getcwd())
        self.url = 'http://chaos.stw-bonn.de/users/mu/git/{}.git'.format(name)

class CheckCopying(Check):
    message = 'no-copying'

    def succeeds(self):
        return self.glob_exists('COPYING*', 'copying*')

class CheckGithub(UrlExistsCheck):
    message = 'no-github'

    def __init__(self):
        name = projecttools.git.get_project_name(os.getcwd())
        self.url = 'https://github.com/martin-ueding/{}'.format(name)

class CheckMakefile(Check):
    message = 'no-makefile'

    def succeeds(self):
        return self.glob_exists('makefile', 'Makefile')

check_classes = [
    CheckChangelog,
    CheckChaos,
    CheckCopying,
    CheckGithub,
]

def main():
    options = _parse_args()

    with concurrent.futures.ThreadPoolExecutor(4) as executor:
        futures = []
        for check_class in check_classes:
            check = check_class()
            futures.append(executor.submit(check.test_and_return_message))

        for future in futures:
            if future.result() is not None:
                print(future.result())

def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    #parser.add_argument("args", metavar="N", type=str, nargs="*", help="Positional arguments.")
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

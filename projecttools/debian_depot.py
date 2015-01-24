#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import argparse
import glob
import subprocess
import os.path

DEBUILD = os.path.expanduser('~/debuild')


def main():
    options = _parse_args()

    packages = glob.glob(os.path.join(DEBUILD, '*/*.deb'))
    subprocess.check_call(['rsync', '-avhE'] + packages + ['df:subdomains/debian/binary/'])

def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    options = parser.parse_args()

    return options

if __name__ == '__main__':
    main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import argparse
import glob
import subprocess
import os.path

DEBUILD = os.path.expanduser('~/debuild')
STAGING = os.path.expanduser('~/.cache/project-tools/debian-depot')


def main():
    options = _parse_args()

    binary_staging_path = os.path.join(STAGING, 'binary')

    os.makedirs(STAGING, exist_ok=True)
    os.makedirs(binary_staging_path, exist_ok=True)

    packages = glob.glob(os.path.join(DEBUILD, '*/*.deb'))
    subprocess.check_call(['rsync', '-avhE'] + packages + [binary_staging_path+'/'])
    os.chdir(STAGING)
    subprocess.check_call('dpkg-scanpackages binary /dev/null | gzip -9c > Packages.gz', shell=True)
    subprocess.check_call(['gpg', '--sign', '--detach-sign', '-o', 'Packages.gpg', 'Packages.gz'])
    subprocess.check_call(['rsync', '-avhE', '--delete', './', 'df:subdomains/debian/'])

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

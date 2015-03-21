#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

'''
Creates new packages on the Open Build Service from upstream updates on my
webseite.

- Look at projects that are checked out in the home:martinueding project.
- Get the index from bulk.martin-ueding.de and check whether there is a new
  upstream version.
- Download new tar achive.
- Change version line in SPEC file.
- Delete all other tar files.
- Check changes into OSC.
- Upload changes.
'''

import argparse
import glob
import os
import re
import logging
import subprocess

import requests

import projecttools

__docformat__ = 'restructuredtext en'

logger = logging.getLogger(__name__)

config = projecttools.get_config()

upstream_pattern = re.compile('href="([\w\d-]+)_([\d.]+)\.tar\.gz"')

base = '.'

def path(name, filename):
    return os.path.join(base, name, filename)


def p(command):
    '''
    Prints the given command.
    '''
    print('$ {}'.format(' '.join(command)))


def find_latest_upstream(name):
    print('Fetching index for', name, '…')
    r = requests.get('http://bulk.martin-ueding.de/source/{}/'.format(name))

    results = upstream_pattern.findall(r.text)

    version_tuples = sorted([
        tuple([int(d) for d in version_match.split('.')])
        for name_match, version_match in results
        if name_match == name
    ])

    filename = '{}_{}.tar.gz'.format(
        name, '.'.join([str(x) for x in version_tuples[-1]])
    )

    url = 'http://bulk.martin-ueding.de/source/{}/{}'.format(name, filename)

    return filename, url


def download_file(url, dest):
    '''
    http://stackoverflow.com/a/16696317
    '''
    print('Fetching', url, 'to', dest, '…')
    r = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # Filter out keep-alive new chunks.
                f.write(chunk)
                f.flush()


def ensure_latest_source(name):
    filename, url = find_latest_upstream(name)

    # Abort here, if the file already exists.
    if os.path.isfile(path(name, filename)):
        return False

    download_file(url, path(name, filename))

    return True


def main():
    options = _parse_args()

    if options.verbose is not None:
        if options.verbose > 1:
            logging.basicConfig(level=logging.DEBUG)
        elif options.verbose > 0:
            logging.basicConfig(level=logging.INFO)

    global base
    base = options.base

    logger.debug('Starting up')

    if options.dry_run:
        subprocess.check_call = projecttools.ppa.p

    for name in os.listdir(base):
        if name.startswith('.'):
            continue
        ensure_latest_source(name)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', dest='dry_run', action='store_true', default=False, help='dry run')
    parser.add_argument('-u', dest='upgrade', action='store_true', default=False, help='use “dpkg -i” to install packages')
    parser.add_argument('-v', dest='verbose', action='count', help='more output (can be used multiple times)')
    parser.add_argument('base')
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()


if __name__ == '__main__':
    main()

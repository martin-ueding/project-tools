#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import os
import os.path
import subprocess
import sys
import collections
import uuid

__docformat__ = "restructuredtext en"

Repo = collections.namedtuple('Repo', ('path', 'remote', 'prefix'))

def main():
    options = _parse_args()

    repos = [Repo(path, str(uuid.uuid4()), os.path.basename(path)) for path in options.paths]

    if len(os.listdir()) > 0:
        print('This is no empty directory. Aborting')
        sys.exit(1)

    subprocess.check_call(['git', 'init'])
    subprocess.check_call(['git', 'commit', '--allow-empty', '-m', 'Initial empty commit'])

    for repo in repos:
        if os.path.isdir(repo.prefix):
            print('“{}” does already exist. Skipping this remote.'.format(repo.prefix))
            continue

        subprocess.check_call(['git', 'remote', 'add', '-f', repo.remote, repo.path])
        powershell_merge(repo, repos)
        subprocess.check_call(['git', 'remote', 'rm', repo.remote])

def subtree_merge(repo):
    subprocess.check_call(['git', 'merge', '-s', 'ours', '--no-commit', '{}/master'.format(repo.remote)])
    subprocess.check_call(['git', 'read-tree', '--prefix={}/'.format(repo.prefix), '-u', '{}/master'.format(repo.remote)])
    subprocess.check_call(['git', 'commit', '-m', "Merge “{}” as a subdirectory".format(repo.prefix)])
    subprocess.check_call(['git', 'pull', '-s', 'subtree', repo.remote, 'master'])

def powershell_merge(repo, repos):
    '''
    http://saintgimp.org/2013/01/22/merging-two-git-repositories-into-one-repository-without-losing-file-history/
    '''
    excludes = [repo.prefix for repo in repos]
    subprocess.check_call(['git', 'merge', repo.remote+'/master', '-m', 'Merge “{}” as a subdirectory'.format(repo.prefix)])
    os.mkdir(repo.prefix)
    command = ['find', '.', '-type', 'f']
    excludes.append('.git')
    for exclude in excludes:
        command.append('-and')
        command.append('(')
        command.append('-not')
        command.append('-path')
        command.append('*{}*'.format(exclude))
        command.append(')')
    command += ['-print', '-exec', 'git', 'mv', '{}', repo.prefix, ';']
    print(' '.join(command))
    subprocess.check_call(command)

    # Commit the move
    subprocess.check_call(['git', 'commit', '-m', 'Move “{}” files into subdir'.format(repo.prefix)])


def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="Merges several git repositories into the current one.")
    parser.add_argument("paths", nargs="+", help="Path to git repository that should be included")
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

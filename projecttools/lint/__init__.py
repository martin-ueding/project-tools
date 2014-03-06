#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import concurrent.futures
import glob
import os
import platform
import subprocess

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

class MakefileTargetCheck(Check):
    def __init__(self):
        self.message = 'no-make-' + self.target

    @staticmethod
    def find_makefile():
        for path in ['makefile', 'Makefile']:
            if os.path.isfile(path):
                return path
        return None

    def succeeds(self):
        makefile = self.find_makefile()
        if makefile is not None:
            with open(makefile) as f:
                for line in f:
                    if line.startswith(self.target + ':'):
                        return True

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

class CheckMakeClean(MakefileTargetCheck):
    target = 'clean'

class CheckMakeDistclean(MakefileTargetCheck):
    target = 'distclean'

class CheckMakeInstall(MakefileTargetCheck):
    target = 'install'

class CheckMakeHtml(MakefileTargetCheck):
    target = 'html'

class CheckReadme(Check):
    message = 'no-readme'

    def succeeds(self):
        return self.glob_exists('README*', 'readme*')

class CheckTags(Check):
    message = 'no-tags'

    def succeeds(Check):
        return len(projecttools.git.get_tags()) > 0

class CheckWebsite(UrlExistsCheck):
    message = 'no-website'

    def __init__(self):
        name = projecttools.git.get_project_name(os.getcwd())
        self.url = 'http://martin-ueding.de/projects/{}/'.format(name)

class CheckPpa(Check):
    message = 'no-ppa'

    def succeeds(self):
        dist, version, codename = platform.dist()
        name = projecttools.git.get_project_name(os.getcwd())
        r = requests.get('https://launchpad.net/~martin-ueding/+archive/stable/+packages?field.series_filter={}&batch=300'.format(codename))
        return name in r.text

class CheckScm(Check):
    message = 'no-scm'

    def succeeds(self):
        return self.glob_exists('.git', '.bzr', '.svn', '.hg')

class CheckPackage(Check):
    message = 'no-package'

    def succeeds(self):
        name = projecttools.git.get_project_name(os.getcwd())
        package_path = os.path.join(os.path.expanduser('~/debuild'), name)
        contents = os.listdir(package_path)
        for entry in contents:
            if os.path.isdir(os.path.join(package_path, entry)):
                return True

        return False

class CheckUntaggedCommits(Check):
    message = 'untagged-commits'

    def succeeds(self):
        log = subprocess.check_output(
            ['git', 'log', '--oneline', '--decorate', 'master^..master']
        )
        return b'tag: ' in log

check_classes = [
    CheckChangelog,
    CheckChaos,
    CheckCopying,
    CheckGithub,
    CheckMakefile,
    CheckMakeClean,
    CheckMakeDistclean,
    CheckMakeInstall,
    CheckMakeHtml,
    CheckPackage,
    CheckPpa,
    CheckReadme,
    CheckScm,
    CheckTags,
    CheckUntaggedCommits,
    CheckWebsite,
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
    options = parser.parse_args()

    return options

if __name__ == "__main__":
    main()

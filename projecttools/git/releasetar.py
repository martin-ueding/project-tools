#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import logging
import os
import re

import projecttools.git

__docformat__ = "restructuredtext en"

def archive_tags(path, destination, pattern):
    toplevel = projecttools.git.get_toplevel()
    name = projecttools.git.get_project_name(toplevel)
    os.chdir(toplevel)
    tags = projecttools.git.get_tags()

    if len(tags) == 0:
        logging.warning('Project %s has no tags, skipping', path)
        return

    for tag in tags:
        matcher = pattern.match(tag)
        if matcher:
            version = matcher.group(1)

            tar_file = '{destination}/{project}/{project}_{version}.tar.gz'.format(
                destination=destination,
                project=name,
                version=version,
            )

            print(tar_file)


def main():
    options = _parse_args()

    if len(options.project) == 0:
        options.project.append('.')

    pattern = re.compile(options.version_regex)

    for project in options.project:
        archive_tags(project, options.destination, pattern)

def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="*", help="Projects to export")
    parser.add_argument("-d", dest="destination")
    parser.add_argument("--version-regex", default='v(.+)', help='Default: %(default)s')
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

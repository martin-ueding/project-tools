.. Copyright © 2012-2013, 2017 Martin Ueding <dev@martin-ueding.de>

#############
project-tools
#############

A collection of tools that are handy to work with programming projects.

This is a merge of:

- chaos-repos
- codetodo
- compress-tarball (from maintenance)
- git-autopush (from maintenance)
- git-autopush (from maintenance)
- git-gc-all (from maintenance)
- git-tarball (now git-release-tar)
- github-repo-count
- ppa (from maintenance)
- prolint
- python-find2

Create tarballs from the tags in a git repository. Optionally, upload them to
your FTP server.

Installation
============

You can use the scripts right away. For easy access, put them into your
``$PATH``, like ``/usr/local/bin`` for instance. To install them for all users,
you can just call::

    # make install

Contained Programs
==================

Prolint
-------

Checks projects for common errors, like a missing readme. It prints a list of
tags that were found, kind of like lintian for Debian packages.

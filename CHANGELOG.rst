.. Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

#########
Changelog
#########

v1.13
    - Change paths to ``~/.config/project-tools`` and
      ``~/.cache/project-tools``.
    - Delete two remaining bash scripts: ``compress-tarball`` and
      ``git-no-tags``.

v1.12.2
    Released:

    - Really fix makefile (I hope)

v1.12.1
    Released: 2014-03-07

    - Fix makefile

v1.12
    Released: 2014-03-07

    - Convert ``prolint`` to Python 3

v1.11
    - Convert ``git-release-tar`` to Python 3

v1.10
    - Update version in ``setup.py``
    - Move Python scripts into package
    - Convert ``spull`` script to Python 3
    - Convert ``git-init-default`` script to Python 3

v1.9.1
    - Use Python instead of ``find``

v1.9
    - Add git repo merge script

v1.8
    - Switch to the termcolor module, replacing colorcodes

v1.7.5
    - *ppa*: Remove backports for raring

v1.7.4
    - Remove bitbucket

v1.7.3
    - Search for repos in ``.vim`` and ``.config`` as well

v1.7.2
    - Do not search dotfiles for now

v1.7.1
    - Fix clean target

v1.7
    - Rewrite some scripts in Python

v1.6
    - *ppa*: Add ``nobackport.js`` support

v1.5
    - *ppa*: Automatic backporting

v1.4
    - *ppa*: Only build when installing packages. This is unneeded work
      otherwise.

v1.3
    - *ppa*: Add ``-u`` switch to upgrade packages locally

v1.2.2
    - *git-autpush*: Make it more robust

v1.2.1
    - *ppa*: Disable installation

v1.2
    - **Added**: ``git-spull``

v1.1.1
    - Update folders

v1.1
    - *git-release-tar*: Add ``-d`` option
    - *ppa*: Update paths

v1.0
    Initial release

Old Changelog for ``chaos-repos``
=================================

v1.5
    - Rename scripts to ``git-init-*``

v1.4.2
    - Supress output

v1.4.1
    - Actually install script

v1.4
    - Add script for Bitbucket.org

v1.3
    - Changelog in the repo itself
    - Script for both, ``git-push-default``

v1.2.1
    - Add GPLv2+ copying file

v1.2
    - Add github push script
    - Rename scripts

v1.1
    - Push the current folder only

v1.0.1
    - Use absolute path

v1.0
    Initial release

Old Changelog for ``prolint``
=============================

v0.6.3
    - Use new environment variables for folders

v0.6.2
    - Actually install report script

v0.6.1
    - Check for more make targets

v0.6
    - Check for untagged commits
    - Add a report generating script
    - Add README

v0.5
    - Check for Debian packaging

V0.4
    - Check for PPA
    - Check for COPYING file
    - Central license file
    - Background all checks for parallel processing

v0.3
    - Check on my personal homepage

v0.2
    - Check for github and chaos as well

v0.1
    Initial release.

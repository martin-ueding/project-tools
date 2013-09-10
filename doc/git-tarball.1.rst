.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

###############
git-release-tar
###############

**********************************
Generate release tar from git tags
**********************************

:Author: Martin Ueding <dev@martin-ueding.de>
:Date: 2013-09-10
:Manual section: 1


SYNOPSIS
========

::

    git release-tar [-d destination] [repo1 ...]

DESCRIPTION
===========

This script will go into each git repository given on the command line and
create a tarball for each tag in the git repository.

The tarballs will be named in a Debian friendly way, which is
``repo_1.2.tar.gz``. When extracting the tarballs, a folder ``repo-1.2`` will
be created, with all the files in it. That way, it is very easy for Debian
packagers to package the program.

The generated tarballs will be put into a folder with the name of the repo into
a folder which has to be specified in the git configuration file in key
``tarball.destdir``.

OPTIONS
=======

You can supply a list of folders which are git repositories. If you do not supply any, the current repo will be used, with its directory name as the project name.

``-d destination``
    Create the tar archive in the given location.

ENVIRONMENT
===========

It will use these keys from the ``.gitconfig``:

- tarball.destdir

FILES
=====

- ``.gitconfig``

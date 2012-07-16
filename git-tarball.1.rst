###########
git-tarball
###########

******************************
Generate tarball from git tags
******************************

:Author: Martin Ueding <dev@martin-ueding.de>
:Date: 2012-07-15
:Manual section: 1


SYNOPSIS
========

::

    git tarball [repo1 ...]

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

ENVIRONMENT
===========

It will use these keys from the ``.gitconfig``:

- tarball.destdir
- tarball.ftp

It will use the ``.netrc`` file to determine username and password for the
given FTP server.

FILES
=====

- ``.gitconfig``
- ``.netrc``

SEE ALSO
========

git-upload-tarballs(1)

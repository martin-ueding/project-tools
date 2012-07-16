###################
git-upload-tarballs
###################

***************************************
Upload tarballs packaged by git-tarball
***************************************

:Author: Martin Ueding <dev@martin-ueding.de>
:Date: 2012-07-14
:Manual section: 1

SYNOPSIS
========

::

    git upload-tarballs

DESCRIPTION
===========

This will upload all the source tarballs that are stored in the directory given
in git option ``tarball.destdir`` to the FTP server given in option
``tarballs.ftp``.

OPTIONS
=======

There are no options.

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

git-tarball(1)

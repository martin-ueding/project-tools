#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

'''
Goes through the folder with my projects, exports the current git tags with
``git release-tar`` into the packaging folder. Then it uses ``uupdate`` and
``debuild``, as well as ``dput`` to make sure that all packages in the
Launchpad PPA are up do date.
'''

import argparse
import functools
import glob
import json
import logging
import os
import platform
import re
import subprocess
import sys
import termcolor

import projecttools

__docformat__ = 'restructuredtext en'

current_release = platform.dist()[2]
'''
Ubuntu release that the packages should be on.
'''

basedir = os.path.expanduser('~/debuild')
branchesdir = os.path.expanduser('~/Projekte')
packages = sorted(os.listdir(basedir))

public = []
'''
List of packages that should be uploaded.
'''

upgrades = []

logger = logging.getLogger("ppa")

config = projecttools.get_config()

def check_for_debian():
    dist = platform.dist()

    if not dist[0] in ["Debian", "Ubuntu"]:
        logger.error("This is not a Debian or Ubuntu machine. This is {}.".format(dist[0]))
        sys.exit(15)

def p(command):
    '''
    Prints the given command.
    '''
    print('$ {}'.format(' '.join(command)))


class PackagingError(Exception):
    '''
    General exception class for this script.
    '''
    pass


class Package(object):
    '''
    Models a Debian Package.
    '''
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Package('{}')".format(self.name)

    def auto(self, options):
        termcolor.cprint(self.name, 'cyan')

        os.chdir(basedir)

        self.export_latest()
        if self.needs_uupdate():
            self.uupdate()

        if self.has_debian_watch():
            self.uscan()

        if self.name in public:
            if self.needs_building(True) or self.needs_new_series():
                self.build(True)
                self.backport()
            try:
                self.upload()
            except PackagingError as e:
                logger.warning('Caught error, trying to build source again.')
                self.build(True)
                self.upload()

        if options.upgrade:
            built_now = False

            if self.needs_building(False):
                self.build(False)
                built_now = True

            needs_upgrade, installed, latest = self.needs_upgrade()
            if needs_upgrade:
                logger.info('This package needs upgrading, {} → {}'.format(installed, latest))
                if not built_now:
                    self.clean()
                    self.build(False)
                upgrades.append(
                    os.path.join(basedir, self.name, self.get_latest('.deb'))
                )

        self.clean_old()

    def build(self, source=True):
        '''
        Builds the given package, binary or source.
        '''
        logger.debug('Building {}'.format('source' if source else 'binary'))
        latest_folder = self.get_latest_folder()

        os.chdir(os.path.join(basedir, self.name, latest_folder, 'debian'))
        sed_command = ['sed', '-i', 's/UNRELEASED/{}/'.format(current_release), 'changelog']
        subprocess.check_call(sed_command)

        if source:
            self.bump_release()

        os.chdir(os.path.join(basedir, self.name, self.get_latest_folder()))

        command = ['debuild']

        if source:
            command.append('-S')

        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            print(e)
            raise PackagingError('Build failed.')

    def bump_release(self):
        if self.needs_new_series():
            latest_folder = self.get_latest_folder()
            os.chdir(os.path.join(basedir, self.name, latest_folder, 'debian'))
            logger.info('This needs to be uploaded with the new release.')
            subprocess.check_call(['pwd'])
            subprocess.check_call(['dch', '-D', current_release, 'Rebuild for {}'.format(current_release)])

    def clean(self):
        '''
        Remove everything that can be build.
        '''
        logger.debug('Cleaning')
        suffixes = [
            '.deb',
        ]

        for suffix in suffixes:
            files = glob.glob('*{}'.format(suffix))
            for file_ in files:
                logger.debug('Cleaning {}'.format(file_))
                os.unlink(file_)

    def clean_old(self):
        '''
        Remove everything that can be build.
        '''
        logger.debug('Cleaning old files')
        suffixes = [
            '.build',
            '.changes',
            '.deb',
            '.dsc',
            '.upload',
        ]

        for suffix in suffixes:
            files = glob.glob('*{}'.format(suffix))
            latest = self.get_latest(suffix)
            for file_ in files:
                if file_ == latest:
                    logger.debug('Skipping ' + file_)
                    continue
                logger.debug('Cleaning {}'.format(file_))
                os.unlink(file_)

    def backport(self):
        '''
        Creates backports for the older versions of Ubuntu.
        '''
        if self.name in nobackport:
            return

        logger.debug('Backporting ...')

        old_series_list = config['PPA']['backport to'].split()

        for old_series in old_series_list:
            subprocess.check_call([
                'backportpackage',
                '-d', old_series,
                '-r',
                '-y',
                '-u', 'stable',
                self.get_latest('.dsc'),
            ])

    def export_latest(self):
        '''
        Goes into the ``~/Projekte`` folder and generates a tar archive with the
        latest version.

        Changes the current working directory.
        '''
        logger.debug('Exporting latest version with “git release-tar”.')
        for d in [branchesdir, os.path.expanduser('~/.vim/bundle')]:
            try:
                os.chdir(os.path.join(branchesdir, self.name))
                subprocess.check_call(['git', 'release-tar', '-d', basedir])
            except subprocess.CalledProcessError:
                pass
            except OSError:
                pass

    def get_latest(self, suffix, function=None, folder=False):
        logger.debug('Finding latest of “{}” with filter “{}”.'.format(suffix, str(function)[:9]))
        os.chdir(os.path.join(basedir, self.name))
        output = subprocess.check_output('ls | sort -V', shell=True)
        lines = output.decode().strip().split('\n')
        files = [x for x in lines
                 if (
                     (not folder and os.path.isfile(os.path.join(basedir, self.name, x)))
                     or (folder and os.path.isdir(os.path.join(basedir, self.name, x)))
                 )
                 and x.endswith(suffix)]

        if function is not None:
            files = [x for x in files if function(x)]

        if len(files) == 0:
            raise PackagingError('No latest *{} found'.format(suffix))

        return files[-1]

    def get_latest_folder(self):
        '''
        Retrieves the folder (without ``.orig``) which has the latest version
        number. If there is no such folder, ``None`` is returned.
        '''
        logger.debug('Finding latest folders.')
        def function(x):
            return not x.endswith('.orig')

        return self.get_latest('', function, folder=True)

    def get_latest_tar(self):
        logger.debug('Finding latest .tar.')
        def function(x):
            return not x.endswith('.orig.tar.gz') and not x.endswith('.debian.tar.gz')

        return self.get_latest('.tar.gz', function)

    def get_release(self):
        '''
        Checks the changelog for the Ubuntu series this package is on.
        '''
        logger.debug('Read the release in the debian/changelog.')
        changelog_file = os.path.join(self.get_latest_folder(), 'debian', 'changelog')

        with open(changelog_file) as f:
            first_line = f.readline()

        m = re.match(r'.*? \(.*?\) (\w+); urgency=\w+', first_line)

        if m:
            return m.group(1)

    def has_debian_watch(self):
        '''
        Checks whether this package has a debian/watch file.
        '''
        logger.debug('Checking for debian/watch.')
        latest_folder = self.get_latest_folder()
        return os.path.isfile(os.path.join(basedir, self.name, latest_folder, 'debian', 'watch'))

    def installed_version(self):
        '''
        Checks ``apt-cache`` for the installed version of the package.

        I am aware that there is an ``apt`` module for Python which does the
        very thing. But I feel lazy and just get it out of the output and parse
        that.
        '''
        logger.debug('Reading installed version of this package.')
        try:
            command = ['apt-cache', 'show', self.name]
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            print(e)
        else:
            lines = output.decode().strip().split('\n')
            for line in lines:
                if line.startswith('Version:'):
                    words = line.strip().split()

                    return words[1]

    def needs_building(self, source=True):
        '''
        Checks whether the package needs to be build.

        It checks the latest ``.changes`` and ``.deb`` in the folder and
        compares them to the latest folder.
        '''
        logger.debug('Determining whether {} need building.'.format('source' if source else 'binary'))
        os.chdir(os.path.join(basedir, self.name))

        latest_folder = self.get_latest_folder()
        try:
            if source:
                latest = self.get_latest('_source.changes')
            else:
                latest = self.get_latest('.deb')
        except PackagingError:
            return True

        prefix = latest[:len(latest_folder)]
        prefix = prefix[:len(self.name)] + '-' + prefix[len(self.name) + 1:]

        return latest_folder != prefix

    def needs_new_series(self):
        logger.debug('Determine whether this needs a rebuild for this series.')
        release = self.get_release()
        return_value = release != current_release
        logger.debug("Found and current: release={} current_release={} return={}".format(release, current_release, return_value))
        return return_value

    def needs_upgrade(self):
        '''
        Checks whether the package needs to be updated.
        '''
        logger.debug('Determine whether package need to be installed.')
        installed = self.installed_version()
        latest_deb = self.get_latest('.deb')
        pattern = r'{}_([^_]+)_.+\.deb'.format(self.name)
        m = re.match(pattern, latest_deb)
        if m:
            latest_version = m.group(1)

        return latest_version != installed, installed, latest_version

    def needs_uupdate(self):
        logger.debug('Determine whether uupdate is needed.')
        os.chdir(os.path.join(basedir, self.name))

        latest_folder = self.get_latest_folder()
        latest_tar = self.get_latest_tar()

        prefix = latest_tar[:-len('.tar.gz')]
        prefix = prefix[:len(self.name)] + '-' + prefix[len(self.name) + 1:]

        return latest_folder != prefix

    def upload(self):
        changes = self.get_latest('_source.changes')
        logger.debug('Upload to Launchpad PPA.')
        try:
            os.chdir(os.path.join(basedir, self.name))
            subprocess.check_call(['dput', 'stable', changes])
        except subprocess.CalledProcessError as e:
            print(e)
            raise PackagingError('Upload failed')

    def uupdate(self):
        '''
        Goes into the latest folder and calls ``uupdate`` onto the latest tar
        archive.

        After that, there should be a new latest folder.
        '''
        latest_tar = self.get_latest_tar()
        latest_folder = self.get_latest_folder()

        os.chdir(os.path.join(basedir, self.name, latest_folder))

        logger.info('Running “uupdate”.')
        try:
            command = ['uupdate', '../'+latest_tar]
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            print(e)
            raise PackagingError('uupdate failed')

    def uscan(self):
        '''
        Runs uscan.
        '''
        latest_tar = self.get_latest_tar()
        latest_folder = self.get_latest_folder()

        os.chdir(os.path.join(basedir, self.name, latest_folder))

        logger.info('Running “uscan“.')
        command = ['uscan']
        return_value = subprocess.call(command)
        logger.debug('Return value of uscan is {}.'.format(return_value))


def main():
    options = _parse_args()

    if options.verbose is not None:
        if options.verbose > 1:
            logging.basicConfig(level=logging.DEBUG)
        elif options.verbose > 0:
            logging.basicConfig(level=logging.INFO)

    logger.debug('Starting up')

    check_for_debian()

    if options.dry_run:
        subprocess.check_call = p

    publicfile = os.path.expanduser('~/.config/project-tools/public.js')

    if os.path.isfile(publicfile):
        with open(publicfile) as f:
            global public
            public = json.load(f)

    nobackportfile = os.path.expanduser('~/.config/project-tools/nobackport.js')

    if os.path.isfile(nobackportfile):
        with open(nobackportfile) as f:
            global nobackport
            nobackport = json.load(f)

    for name in packages:
        try:
            package = Package(name)
            package.auto(options)
        except OSError as e:
            termcolor.cprint(e, 'red')
            termcolor.cprint('Packaging of {0} failed.'.format(package), 'red')
        except PackagingError as e:
            termcolor.cprint(e, 'red')
            termcolor.cprint('Packaging of {0} failed.'.format(package), 'red')

    if len(upgrades) > 0:
        print()
        print('possible upgrades')
        print('-----------------')
        print()
        command = ["pkexec", "dpkg", "-i"] + upgrades
        print(" ".join(command))
        print()
        subprocess.call(command)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    #parser.add_argument('args', metavar='N', type=str, nargs='*', help='Positional arguments.')
    #parser.add_argument('', dest='', type='', default=, help=)
    parser.add_argument('-n', dest='dry_run', action='store_true', default=False, help='dry run')
    parser.add_argument('-u', dest='upgrade', action='store_true', default=False, help='use “dpkg -i” to install packages')
    parser.add_argument('-v', dest='verbose', action='count', help='more output (can be used multiple times)')
    #parser.add_argument('--version', action='version', version='<the version>')

    return parser.parse_args()

if __name__ == '__main__':
    main()

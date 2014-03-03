#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import termcolor
import json
import os
import re
import glob
import shutil
import logging
import subprocess

import projecttools

__docformat__ = "restructuredtext en"

logger = logging

mirrors = ["chaos", "github"]

status = {
    "ok": 0,
    "init": 0,
    "push": 0,
}

last_commits = {}
commits_file = os.path.expanduser("~/.cache/maintenance/last-commits.js")

def load_last_commits():
    global last_commits

    try:
        with open(commits_file) as f:
            last_commits = json.loads(f.read())
    except FileNotFoundError as e:
        logger.warning(e)
    except ValueError as e:
        logger.warning(e)

def migrate_to_mirror(repo, remote):
    try:
        is_mirror = (subprocess.check_output(["git", "config", "remote.{}.mirror".format(remote)]).decode().strip() == "true")
    except subprocess.CalledProcessError:
        is_mirror = False
        pass

    if not is_mirror:
        print("Migrating to mirror:", repo, remote)
        url = subprocess.check_output(["git", "config", "remote.{}.url".format(remote)]).decode().strip()

        subprocess.check_output(["git", "remote", "rm", remote])
        subprocess.check_output(["git", "remote", "add", "--mirror=push", remote, url])

    for file_ in glob.glob(".git/refs/remotes/{}/*".format(remote)):
        print("Deleting mirror ref:", file_)
        shutil.rmtree(file_)

def save_last_commits():
    global last_commits

    exported = json.dumps(last_commits, sort_keys=True, indent=4)

    with open(commits_file, "w") as f:
        f.write(exported)

def find_remotes(repo):
    output = subprocess.check_output(["git", "remote"]).decode().strip()
    remotes = [x for x in output.split("\n") if len(x) > 0]
    return remotes

def handle_repo(repo, options):
    os.chdir(repo.replace('.git', ''))
    remotes = find_remotes(repo)

	# If there are no remotes in this repo, there is nothing more to do.
    if len(remotes) == 0:
        return

    if not options.nofetch:
        fetch(repo, remotes)
    init(repo, remotes)
    push(repo, remotes)

def fetch(repo, remotes):
    for remote in remotes:
        if remote in mirrors:
            continue

        termcolor.cprint("{:8} {:12} {}".format("FETCH", remote, repo), 'blue')
        subprocess.call(["git", "fetch", remote, "--prune"])

def init(repo, remotes):
    is_public = False
    for mirror in mirrors:
        if mirror in remotes:
            is_public = True
            break

    if not is_public:
        return

    remote_name = find_remote_name(repo, remotes)

    for mirror in mirrors:
        if mirror in remotes:
            continue

        termcolor.cprint("{:8} {:12} {}".format("INIT", mirror, repo), 'red')
        global status
        status["init"] += 1
        subprocess.call(["git", "init-{}".format(mirror), remote_name])

def push(repo, remotes):
    global status
    for remote in remotes:
        if not remote in mirrors:
            continue

        if not repo in last_commits:
            last_commits[repo] = {}

        if remote in last_commits[repo]:
            last_commit = last_commits[repo][remote]
        else:
            last_commit = ""

        migrate_to_mirror(repo, remote)

        try:
            master_commit = subprocess.check_output(["git", "rev-parse", "refs/heads/master"]).decode().strip()
        except subprocess.CalledProcessError as e:
            print(e)
            raise
        else:
            #print("master:", master_commit, "last", last_commit)
            if master_commit == last_commit:
                status["ok"] += 1
                termcolor.cprint("{:8} {:12} {}".format("OK", remote, repo), 'green')
            else:
                status["push"] += 1
                termcolor.cprint("{:8} {:12} {}".format("PUSH", remote, repo), 'yellow')
                try:
                    subprocess.check_call(["git", "push", remote, "--mirror"])
                except subprocess.CalledProcessError as e:
                    print(e)
                else:
                    last_commits[repo][remote] = master_commit
                    save_last_commits()


def find_remote_name(repo, remotes):
    reponame = None

    for remote in remotes:
        output = subprocess.check_output(["git", "config", "--get", "remote.{}.url".format(remote)]).decode().strip()
        match = re.search(r"([^/.]+)(\.git)?$", output)
        if match:
            reponame = match.group(1)
            break

    if reponame is None:
        reponame = os.path.basename(repo)
        termcolor.cprint("Could not determine remote name for {}!.".format(os.path.basename(repo)), 'red')

    return reponame

def print_stats():
    print()

    global status
    for status, number in sorted(status.items()):
        termcolor.cprint("{:8} {:4d}".format(status, number), 'cyan')

def main():
    options = _parse_args()

    load_last_commits()

    termcolor.cprint("Populating list of git repositories …", 'cyan')
    repos = projecttools.find_git_repos()
    termcolor.cprint("Done. Found {} git repositories.".format(len(repos)), 'cyan')

    repos.sort()

    for repo in repos:
        try:
            handle_repo(repo, options)
        except FileNotFoundError as e:
            print(e)

    print_stats()

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")
    #parser.add_argument("args", metavar="N", type=str, nargs="*", help="Positional arguments.")
    parser.add_argument("--nofetch", action="store_true", help="Skip “git fetch”")
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()

if __name__ == "__main__":
    main()

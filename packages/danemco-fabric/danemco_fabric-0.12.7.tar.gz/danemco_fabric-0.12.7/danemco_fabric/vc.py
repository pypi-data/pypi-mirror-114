from __future__ import print_function

import random
import time

from fabric.api import (abort, cd, env, execute, local, require, run,
                        runs_once, settings, task)

from .base import exists, lrun


def git_root(is_local=False):

    if is_local or 'local' in env.roles:
        return local("git rev-parse --show-toplevel", capture=True)

    require('conf')
    with cd(env.conf.path):
        print("path is", env.conf.path)
        return run("git rev-parse --show-toplevel")


@task
@runs_once
def push():
    """Send your local changes up."""
    local("git push")


@task
def changes():
    """Output the number of new commits"""
    with cd(env.conf.path):
        lrun("git fetch")
        changes = int(lrun("git rev-list HEAD..@{u} --count", capture=True))
        print("%s changes to apply" % changes)
        return changes


@task
def clone():
    repo = local('git config --get remote.origin.url', capture=True)
    lrun('git clone %s %s' % (repo, env.conf.path))


@task
def pull():
    """Update the repository."""
    require("conf")
    if not exists(env.conf.path):
        execute('vc.clone', host=env.host)
    with cd(env.conf.path):
        with settings(warn_only=True):
            result = lrun("git diff --quiet HEAD && git diff --cached --quiet HEAD")
        if result.failed:
            abort("There are uncommitted changes on %s" % env.roles)
        lrun('git checkout %s' % env.conf.branch)
        for attempt in range(10):
            with settings(warn_only=True):
                response = lrun("git pull", capture=True)
                if 'fatal:' in response:
                    print('=' * 10)
                    print(response)
                    print('-' * 10)
                    seconds = (attempt + 1) ** 2 + random.randint(1, 5)
                    print('= Pull failed, trying again in {} seconds'.format(seconds))
                    time.sleep(seconds)
                    print('= Pull attempt #{}'.format(attempt + 2))
                else:
                    if 'Already up to date' not in response:
                        print(response)
                    break

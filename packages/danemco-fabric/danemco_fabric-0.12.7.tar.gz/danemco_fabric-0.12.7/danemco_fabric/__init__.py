__author__ = 'brian'

import os
from fabric.api import cd, env, local, require, task
from fabric.utils import abort

from .base import *  # noqa
from .config import configure  # noqa: F401
from . import deploy, build, ci, test, vc  # noqa: F401

from .version import __version__  # noqa: F401

env.use_ssh_config = True

pull_db = build.pull_db


@task
def pull_media(dry_run=False):
    """Rsync the remote media files to the local media folder"""
    require("conf")
    user = env.user
    media_dir = 'media/'
    dry_run = '--dry-run' if dry_run else ''
    exclude = ' '.join(['--exclude="/%s"' % s for s in
                       ('CACHE', 'captcha*', 'css', 'js', 'dash', 'img',
                        'office', 'global', 'scripts', 'styles', 'static')])

    if hasattr(env.conf, 'exclude_media'):
        # remove leading and trailing whitespace and commas
        xcl = getattr(env.conf, 'exclude_media', '').strip().strip(',')
        exclude += ''.join([
            ' --exclude="%s"' % s for s in xcl.split(',') if s != ''
        ])

    with cd(env.conf.path):
        if os.path.exists('../media'):
            media_dir = '../media/'
        elif not os.path.exists('media/'):
            abort('Could not find the `media/` directory in . or .. for %s'
                  % env.conf.path)

        local('rsync -vru %(dry_run)s --include=*.css --include=*.jpg --include=*.png %(exclude)s'
              ' -e "ssh -p %(port)s" "%(user)s@%(host)s:%(path)s/%(media)s*" %(media)s'
              % dict(user=user, host=env.host, port=env.port, dry_run=dry_run,
                     path=env.conf.path, media=media_dir, exclude=exclude))

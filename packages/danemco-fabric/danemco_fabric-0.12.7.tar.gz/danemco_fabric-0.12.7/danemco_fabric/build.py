from __future__ import print_function
import os
import random
import six
import string
from six.moves import xrange
from fabric.api import (cd, env, execute, get, local, require, runs_once,
                        settings, task)
from .vc import git_root
from .base import lrun, venv, get_db_settings, exists, settings_flag

if six.PY2:
    from string import uppercase
else:
    from string import ascii_uppercase as uppercase


@task(default=True)
def build(db_action="migrate", hostname=None):
    """ Build/set up the project for the first time"""

    execute("deploy.protected_files", host=env.host)
    execute('build.virtualenv', host=env.host)
    execute('build.requirements', host=env.host)
    execute("build.db", hostname, host=env.host)
    if db_action == "use_live_db":
        with settings(conf=env.sections.production):
            execute("pull_db", role="production")
    elif db_action == "migrate":
        execute("deploy.migrate", host=env.host)
        with settings(warn_only=True):
            execute('deploy.command', cmd='loaddata bootstrap', host=env.host)
    else:
        print("No database loading, use db_action=migrate or db_action=use_live_db")
    if not env.conf.virtualenv.startswith('.'):
        # this is a shared virtualenv so make sure the symlinks are set up
        execute(
            'deploy.command', cmd='changepath %s' % env.conf.virtualenv,
            host=env.host
        )
    execute("deploy.staticfiles", host=env.host)


@task
def update_build():
    """Run the update, migrate, and staticfiles tasks"""

    execute('vc.pull', host=env.host)
    execute('build.virtualenv', host=env.host)
    execute('build.requirements', include_shared_venvs=True, host=env.host)
    execute('deploy.migrate', host=env.host)
    execute('deploy.staticfiles', host=env.host)


@task
def virtualenv():
    """Create the virtual environment if it is local and doesn't exist."""
    require("conf")
    if env.conf.virtualenv.startswith('.'):
        kwargs = dict(
            path=os.path.join(git_root(), env.conf.virtualenv),
            python='-p ' + env.conf.get('python', 'python2'),
        )
        if not exists(kwargs.get('path')):
            lrun("virtualenv {python} {path}".format(
                **kwargs)
            )
        else:
            print("The virtualenv {path} exists".format(**kwargs))


@task
def requirements(include_shared_venvs=False, update=None, flags=None):
    """Install the requirements for the virtualenv"""
    require("conf")

    # probably should just use flags instead of update
    if update is None:
        update = env.conf.update_requirements

    if flags is None:
        flags = env.conf.pip_flags

    pip_cmd = "pip install {flags} {update} -r {file}"
    kwargs = dict(
        update=update and "-U" or "",
        flags=flags or "",
    )

    with cd(env.conf.path):
        if env.conf.virtualenv.startswith('.'):
            kwargs['file'] = os.path.join(git_root(), env.conf.requirements)
            if exists(kwargs['file']):
                with venv():
                    lrun(pip_cmd.format(**kwargs))
        elif include_shared_venvs:
            kwargs['file'] = os.path.join(
                os.sep, 'vagrant', 'virtualenvs', env.conf.virtualenv,
                'requirements.txt'
            )
            with venv():
                lrun(pip_cmd.format(**kwargs))


@task
@runs_once
def db(hostname=None):
    """create the database and user based on the default database settings"""
    require("conf")
    dbsettings = get_db_settings()

    # if no host is specified, use the settings file
    if hostname is None:
        hostname = '10.0.0.%'
        if dbsettings['HOST'] == 'localhost':
            hostname = 'localhost'

    if "mysql" in dbsettings["ENGINE"]:
        with settings(warn_only=True):
            lrun("mysqladmin create %s " % dbsettings['NAME'])

        lrun('echo "%s" | mysql' % "CREATE USER IF NOT EXISTS '%s'@'%s' IDENTIFIED BY '%s';" % (
            dbsettings['USER'],
            hostname,
            dbsettings['PASSWORD'],
        ))

        lrun('echo "%s" | mysql' % "GRANT ALL ON %s.* TO '%s'@'%s';" % (
            dbsettings['NAME'],
            dbsettings['USER'],
            hostname,
        ))
    # post in "postgres" also "postgis"
    elif "post" in dbsettings["ENGINE"]:
        with settings(warn_only=True):
            sqls = [
                "CREATE USER {USER} WITH password '{PASSWORD}'",
                "CREATE DATABASE {NAME} WITH OWNER={USER}"
            ]
            for sql in sqls:
                sql = sql.format(**dbsettings)
                lrun("psql -U postgres -h {host} -c \"{sql}\"".format(
                    host=hostname,
                    sql=sql
                ))
    else:
        print("Sorry, can't create a db for engine: {}".format(
            dbsettings["ENGINE"]
        ))


@task
@runs_once
def pull_db(clear_data=True, local_label="local"):
    """Load a copy of the remote database locally"""
    require("conf")

    dbsettings = get_db_settings()

    # The database dump's filename should include a random string in
    # case multiple people are pulling the database for the same site at
    # the same time.

    filename = "db_dump_%s_%s.sql.gz" % (
        dbsettings['NAME'],
        ''.join(
            random.SystemRandom().choice(
                uppercase + string.digits
            ) for _ in xrange(6)
        )
    )

    if "mysql" in dbsettings['ENGINE']:
        cmd = "mysqldump %s --single-transaction --quick --lock-tables=false" \
            % dbsettings['NAME']
    # post in "postgres" also "postgis"
    elif "post" in dbsettings['ENGINE']:
        cmd = (
            "pg_dump {NAME}"
            "   --username {USER}"
            "   --host {HOST}"
            "   --clean"
            "   --no-privileges"
        ).format(**dbsettings)
    else:
        cmd = None

        print("Sorry, can't pull db for engine: {}".format(
            dbsettings["ENGINE"]
        ))

    if cmd:
        lrun("%s | gzip > %s" % (cmd, filename))

        lrun("du -h %s | cut -f1 # This command's output shows the size of the database dump" % filename)
        get(filename, filename)
        lrun("rm %s" % filename)

        with settings(conf=getattr(env.sections, local_label, "")), venv():
            local("zcat %s | python manage.py dbshell %s" % (filename, settings_flag()))
            local("rm %s" % filename)

            if clear_data:
                # clear payment api keys
                with settings(warn_only=True):
                    sql = r"""
                        DELETE FROM \`livesettings_setting\`
                        WHERE \`group\` LIKE '%%authorize%%'
                        OR \`key\` LIKE '%%authorize%%'
                        OR \`group\` LIKE '%%newsletter%%'
                        OR \`group\` LIKE '%%paypal%%'
                        OR \`key\` LIKE '%%paypal%%';
                    """
                    sql = ' '.join(sql.split())

                    # post in "postgres" also "postgis"
                    if "post" in dbsettings['ENGINE']:
                        sql = sql.replace('`', '"')

                    local('echo "%s" | python manage.py dbshell %s' % (
                        sql,
                        settings_flag()
                    ))

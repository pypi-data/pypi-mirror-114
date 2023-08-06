import os
import re

from fabric.api import cd
from fabric.context_managers import path
from fabric.contrib import files
from fabric.operations import require, local, run
from fabric.state import env


def venv():
    """ sets up local calls to use the site's virtualenv """
    require("conf")
    if env.conf.virtualenv.startswith("."):
        return path(os.path.join(env.conf.path, env.conf.virtualenv, "bin"), behavior="prepend")
    return path(os.path.join("/var/www/virtualenvs", env.conf.virtualenv, "bin"), behavior="prepend")


def lrun(*args, **kwargs):
    if env.host in ['localhost', '127.0.0.1']:
        return local(*args, **kwargs)
    # to return results local uses capture, run uses quiet
    # convert capture to quiet for remote commands
    if 'capture' in kwargs:
        kwargs['quiet'] = kwargs.pop('capture')
    return run(*args, **kwargs)


def exists(*args, **kwargs):
    """ Use local or remote version based on the host it is connecting to"""

    if env.host in ['localhost', '127.0.0.1']:
        return os.path.exists(*args, **kwargs)
    return files.exists(*args, **kwargs)


def settings_flag():
    if env.conf.settings == "settings":
        # django-admin defaults to using settings so no need to pass it on
        return ""
    return "--settings=%s" % env.conf.settings


def get_db_settings(name='default'):
    django_settings = {}
    python_settings = "-W ignore::UserWarning"
    with cd(env.conf.path):
        with venv():
            out = lrun(
                "python %s manage.py diffsettings %s 2>/dev/null | grep DATABASE" % (
                    python_settings, settings_flag()
                ),
                capture=True
            )
            out = re.sub(r'<(class|function) <?[\w\'.]+>?( at \w+)?>', 'None', out)
            exec(out, django_settings)
            if "DATABASES" in django_settings:
                if name is None:
                    return django_settings['DATABASES']
                return django_settings['DATABASES'][name]
            else:
                # 1.2 setup
                return {
                    'NAME': django_settings['DATABASE_NAME'],
                    'USER': django_settings['DATABASE_USER'],
                    'PASSWORD': django_settings['DATABASE_PASSWORD'],
                    'HOST': django_settings['DATABASE_HOST'],
                }

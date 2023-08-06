from __future__ import print_function
import os
import six
from fabric.api import env, require
# from fabric.contrib import django

try:
    import configparser
    # from ConfigParser import SafeConfigParser
except ImportError:
    from six.moves import configparser

from .vc import git_root


SERVERS = {
    'sirius-a': '209.33.249.194:4402',
    'sirius-b': '209.33.249.194:4406',
    'sirius-dev': '209.33.249.194:4407',
    'venus': '209.33.249.194:4405',
    'handiquilter': '209.33.202.194:4403',  # Handi Quilter
    'superior': '209.33.249.194:4404',  # Superior Threads
    'local': 'localhost',
}


class AttrDict(dict):
    """
    Dictionary subclass enabling attribute lookup/assignment of keys/values.
    Copied from fabric.state._AttributeDict as it was a private class there.
    """""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *names):
        for name in names:
            value = self.get(name)
            if value:
                return value


def get_django_settings(settings=None):
    """
    Returns the actual Django Settings module using
    `fabric.contrib.django.settings_module` which also sets DJANGO_SETTINGS_MODULE
    in the shell environment.

    See http://fabric.readthedocs.org/en/latest/api/contrib/django.html

    THIS DOESN'T SEEM TO BE WORKING. It sets the django settings module for
    os.environ, however it doesn't update the os.environ['PATH'] so it never
    finds the settings module.
    """

    require("conf")
    settings = settings if settings else env.conf.get('settings', 'settings')

#     os_envpath = '%s:%s' % (env.conf.path, os.environ['PATH'])
#
#     with cd(env.conf.path):
#         django.settings_module('%s.%s' % (env.conf.project, settings))
#
#         from django.conf import settings

    return settings


def set_conf():
    """ map env.conf to the first role in env.roles as a shortcut. """
    if env.roles and env.roles[0] in env.sections:
        # used to wipe out other variables
        env.conf = env.sections[env.roles[0]]


def parse_config_file(conf_path, default_overrides={}, update=False):
    defaults = {
        'name': os.path.basename(os.path.dirname(os.getcwd())),
        'path': os.getcwd(),
        'virtualenv': '1.4',
        'server': 'sirius-a',
        'branch': 'master',
        'test_modules': '',
        'requirements': 'requirements.txt',
        'settings': "settings",
        'update_requirements': False,
        'npm': "true",
        'bower': "true",
        'pip_flags': ''
    }
    defaults.update(default_overrides)
    if six.PY2:
        config_parser = configparser.SafeConfigParser(defaults)
    else:
        config_parser = configparser.ConfigParser(defaults)

    if not os.path.exists(conf_path):
        print("Could not find configuration file. Creating `%s'" % conf_path)
        config_parser.add_section("production")
        config_parser.add_section("local")
        config_parser.set("local", 'server', 'local')
        update = True

    config_parser.read(conf_path)

    if update:
        for key, value in default_overrides.items():
            config_parser.set("DEFAULT", key, value)
        with open(conf_path, 'w+') as fp:
            config_parser.write(fp)

    return config_parser


def configure(servers=SERVERS, conf_file="site.conf"):
    """
    Read configuration from a config file into env.conf

    This will update the env.roldefs, env.roles with the configuration
    """
    conf_path = os.path.join(git_root(is_local=True), conf_file)
    config_parser = parse_config_file(conf_path)

    # map env.conf to the config file,
    env.sections = AttrDict()

    for section in config_parser.sections():
        env.roledefs[section] = []

        # allow multiple servers separated by comma
        if six.PY2:
            section_servers = (config_parser.get(section, 'server') or '').split(",")
        else:
            section_servers = (config_parser.get(section, 'server') or '').split(",")

        for server in section_servers:
            env.roledefs[section].append(servers.get(server, server))

        # default to production if no role is specified on the command line
        if not env.roles and section == "production":
            env.roles = [section]
        env.sections[section] = AttrDict(config_parser.items(section))
        for b in ['update_requirements', 'npm', 'bower']:
            try:
                env.sections[section][b] = config_parser.getboolean(section, b)
            except ValueError:
                continue

    set_conf()

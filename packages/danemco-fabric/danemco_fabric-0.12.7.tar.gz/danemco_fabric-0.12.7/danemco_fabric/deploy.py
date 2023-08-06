import datetime
import getpass
import os
import re
import six
import sys
from distutils.version import LooseVersion

from fabric.api import (cd, env, execute, hide, hosts, require, roles, run,
                        runs_once, settings, sudo, task)
from fabric.contrib.files import exists

from .base import lrun, settings_flag, venv

SYSTEM_USERS = (
    "ansible",
    "backup",
    "bin",
    "ci_user",
    "colord",
    "daemon",
    "dev",
    "games",
    "gnats",
    "irc",
    "landscape",
    "libuuid",
    "list",
    "lp",
    "mail",
    "man",
    "messagebus",
    "nagios",
    "news",
    "nobody",
    "ntp",
    "postfix",
    "proxy",
    "root",
    "sshd",
    "statd",
    "sync",
    "sys",
    "syslog",
    "uucp",
    "www-data",
    "cody"
)


@task
def protected_files():
    """ create/update the protected files """
    require("conf")

    key = ''
    file_with_key = os.path.join(os.path.expanduser('~'), '.danemco', '.git', 'config')

    try:
        with open(file_with_key, 'r') as f:
            contents = f.read()
    except IOError:
        print('Unable to get the decryption key from the expected location:')
        print('')
        print(file_with_key)
        print('')
        print('The above file either does not exist or it is unreadable. That being the case,')
        print('you will need to manually enter the decryption key.')
        print('')
    else:
        key_result = re.search('smudge = openssl enc -d -base64 -aes-256-ecb -k ([^ ]+)', contents)
        if key_result:
            key = key_result.group(1)
        else:
            print('Unable to get the decryption key from the following file:')
            print('')
            print(file_with_key)
            print('')
            print('The above file exists and is readable, but the key pattern was not found. That')
            print('being the case, you will need to manually enter the decryption key.')
            print('')

    while key == '':
        key = getpass.getpass(prompt='Enter the decryption key: ')

    with cd(env.conf.path):
        with hide('running'):
            tmp_name = 'tmp' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            tar_name = 'protected-{}.tar'.format(tmp_name)

            with settings(warn_only=True):
                lrun('git archive --remote=git@gitlab.com:virgodev/sites/danemco.net.git HEAD ' + env.conf.name + ' > ' + tar_name)

            is_empty = False

            if env.host in ['localhost', '127.0.0.1']:
                if not os.stat(tar_name).st_size:
                    is_empty = True
                    os.unlink(tar_name)
            else:
                with settings(hide('everything')):
                    if run('find . -type f -name "{}" -empty'.format(tar_name)):
                        is_empty = True
                        run('rm ' + tar_name)

            if not is_empty:
                lrun('tar --strip 1 -xf ' + tar_name)
                tar_contents = lrun('tar -tf ' + tar_name, capture=True).replace('\r\n', '\n').replace('\r', '\n').rsplit('\n')
                lrun('rm ' + tar_name)

                protected_files = []
                for item in tar_contents:
                    if item.endswith('/'):
                        continue
                    protected_files.append('/'.join(item.split('/')[1:]))

                for protected_file in protected_files:
                    protected_file_tmp_name = protected_file + tmp_name

                    lrun(
                        'mv "{protected_file}" "{protected_file_tmp_name}" && openssl enc -d -base64 -aes-256-ecb -k {key} -in "{protected_file_tmp_name}" -out "{protected_file}" -md md5 && rm "{protected_file_tmp_name}"'.format(
                            key=key,
                            protected_file=protected_file,
                            protected_file_tmp_name=protected_file_tmp_name,
                        )
                    )


@task
def upgrade():
    """Deploy and upgrade the packages based on the requirements file"""

    require("conf")
    execute('vc.pull', host=env.host)
    execute('build.virtualenv', host=env.host)
    execute('build.requirements', host=env.host, update=True)
    execute('deploy.migrate', host=env.host)
    execute('deploy.staticfiles', host=env.host)
    execute('deploy.restart', host=env.host)
    if 'true' in getattr(env.conf, 'deploy-cronjobs', 'true').lower():
        execute('deploy.cronjobs', host=env.host)


@task
@runs_once
def staticfiles():
    """Collect Static files"""

    require("conf")

    execute("deploy.npm")
    execute("deploy.bower")

    with settings(warn_only=True):
        if env.host in ['localhost', '127.0.0.1']:
            execute('deploy.command', cmd="collectstatic --noinput -l -v0", host=env.host)
        else:
            execute('deploy.command', cmd="collectstatic --noinput -v0", host=env.host)


@task
@runs_once
def bower():
    install_util("bower.json", "bower install --config.interactive=false", "bower")


@task
def npm():
    if env.host in ['localhost', '127.0.0.1']:
        cmd = "npm install"
    else:
        cmd = "npm ci --production"
    install_util("package.json", cmd, "npm")


def install_util(filename, cmd, check_setting=None):
    """ if the given file exists, run the command """
    require("conf")

    if env.host in ['localhost', '127.0.0.1']:
        if os.path.exists(filename):
            lrun(cmd)
    else:
        if check_setting and env.conf[check_setting]:
            with cd(env.conf.path):
                with settings(warn_only=True):
                    if exists(filename):
                        lrun(cmd)


@task
@runs_once
def migrate():
    """Migrate the Database"""

    require("conf")
    with cd(env.conf.path):
        with venv():
            dj_version = lrun('python -c "import django;print(django.get_version())"', capture=True)
            if LooseVersion(dj_version) >= LooseVersion("1.7.0"):
                execute('deploy.command', cmd="migrate --noinput -v0", host=env.host)
            else:
                execute('deploy.command', cmd="syncdb --noinput -v0", host=env.host)
                with settings(warn_only=True):
                    execute('deploy.command', cmd="migrate --noinput -v0 --all", host=env.host)


@task
def restart():
    """Restart the website"""
    require("conf")

    if getattr(env.conf, 'clear_caches', None):
        execute('deploy.clearcache', host=env.host)

    if hasattr(env.conf, "restart_cmd"):
        with cd(env.conf.path):
            lrun(env.conf.restart_cmd)
    elif env.conf.name:
        lrun("sudo /etc/init.d/django-sites restart %s" % env.conf.name)


@task
@runs_once
def cronjobs():
    require('conf')
    with cd(env.conf.path):
        with venv():
            with settings(warn_only=True):
                lrun('python manage.py installtasks %s -v0' % settings_flag())


@task
@runs_once
def clearcache(key=None):
    """
    Clear configured django cache backends based on site.conf.

    Two options for clearing cache.
    # site.conf - simple option #1; will just clear default cache

    clear_caches = True
    ...

    # site.conf - specific option #2; will clear each cache key

    clear_caches = default,my-custom-cache,my-second-custom-cache
    """
    require("conf")

    with settings(warn_only=True):
        caches = getattr(env.conf, 'clear_caches', None)
        keys = []

        # manual call to refresh cache
        if key and isinstance(key, six.string_types):
            caches = key

        if caches and isinstance(caches, six.string_types):

            if 'true' in caches.lower():
                keys = ['default']

            else:
                keys = [
                    k.strip()
                    for k in caches.strip().strip(',').split(',')
                    if k != ''
                ]

            execute(
                'deploy.command', cmd="clear_cache {} -v0".format(' '.join(keys)),
                host=env.host
            )
        else:
            sys.stdout.write('No actions taken to clear caches.\n')


@task
def command(cmd):
    with cd(env.conf.path):
        with venv():
            settings = settings_flag()
            if "--settings=" in cmd:
                settings = ""
            lrun('python manage.py {cmd} {settings}'.format(
                cmd=cmd,
                settings=settings,
            ))


@task(default=True)
def deploy(force=False):
    """Run the update, migrate, staticfiles and restart tasks"""

    require("conf")
    with settings(conf=env.sections.local, warn_only=True):
        if 'true' in getattr(env.conf, 'vc-push', 'true').lower():
            execute('vc.push', role="local", host=env.host)
    if force:
        hosts_with_changes = True
    else:
        changes = execute('vc.changes', host=env.host)
        hosts_with_changes = [h for h, v in changes.items() if v]
    if hosts_with_changes:
        execute('vc.pull', host=env.host)
        execute('build.virtualenv', host=env.host)
        execute('build.requirements', host=env.host)
        execute('deploy.protected_files', host=env.host)
        execute('deploy.migrate', host=env.host)
        execute('deploy.staticfiles', host=env.host)
        execute('deploy.restart', host=env.host)
        if 'true' in getattr(env.conf, 'deploy-cronjobs', 'true').lower():
            execute('deploy.cronjobs', host=env.host)


def proxy_command_to_mars(func, *args, **kwargs):
    host = env.host
    with settings(host_string="mars.velocitywebworks.com"):
        func(server=host, *args, **kwargs)


@task()
def grant_access():
    proxy_command_to_mars(server_grant)


@task()
def revoke_access(username):
    proxy_command_to_mars(server_revoke, username)


@task()
def delete_expire_password(username):
    password_de(server_revoke, username)


@task()
@roles([])
@hosts("mars.velocitywebworks.com")
def server_grant(server):
    home = os.path.expanduser("~")
    with open("{}/.ssh/id_rsa.pub".format(home), "r") as fh:
        content = fh.read().strip()

    sudo("""
ssh -t root@{server} <<'END1'
if [ ! -d "/home/{user}" ]; then
    useradd {user} -g www-data --groups www-data,sudo -m -s /bin/bash
    sudo -Hu {user} ssh-keygen -N "" -f /home/{user}/.ssh/id_rsa
    passwd -de {user}
fi
echo '{key}' >> /home/{user}/.ssh/authorized_keys
chown {user} -R /home/{user}/.ssh
chmod 700 /home/{user}/.ssh
chmod 600 /home/{user}/.ssh/authorized_keys
END1""".format(server=server, user=env.user, key=content), user="cody")


@task()
@roles([])
@hosts("mars.velocitywebworks.com")
def server_revoke(username, server):
    if username in SYSTEM_USERS:
        raise Exception("Can't delete system accounts!")
    sudo("ssh -t root@{server} userdel {user} -r".format(
        server=server, user=username), user="cody")


@task()
@roles([])
@hosts("mars.velocitywebworks.com")
def password_de(username, server):
    if username in SYSTEM_USERS:
        raise Exception("Can't change password for system accounts!")
    sudo("ssh -t root@{server} passwd -de {user}".format(
        server=server, user=username), user="cody")
    exit()

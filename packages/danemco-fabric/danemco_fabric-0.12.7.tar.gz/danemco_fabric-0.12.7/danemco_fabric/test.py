import re
from fabric.api import cd, env, execute, require, task

from .base import exists, lrun, settings_flag


@task(default=True)
def modules():
    """Test just the modules defined in the configuration"""
    require("conf")

    with cd(env.conf.path):
        lrun("python manage.py test %s %s" % (settings_flag(), env.conf.test_modules))


@task
def script():
    """
    Attempt to execute shell script 'runtests.sh' and fall back to task 'modules'.
    """
    require("conf")

    with cd(env.conf.path):
        present = exists('runtests.sh')

        if present:
            exp = r'fab[a-z\s\w]+\.script'
            contents = lrun("cat ./runtests.sh", capture=True)
            occurs = re.findall(exp, contents, re.DOTALL)

            if not occurs:
                lrun("./runtests.sh")
                return

            else:
                print(
                    "\n\tFound an occurrence of the command 'fab test.script' "
                    "within the script. Executing the default command "
                    "'fab test.modules' to avoid recursion.\n"
                )

        execute('test.modules', host=env.host)


@task
def all():
    """Test the whole site"""
    require("conf")

    with cd(env.conf.path):
        lrun("python manage.py test %s" % settings_flag())

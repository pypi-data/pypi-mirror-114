from __future__ import print_function

from fabric.decorators import task
from fabric.operations import require, local
from fabric.state import env
from fabric.tasks import execute
import gitlab
import requests

from .config import set_conf


GITLAB_CI = "https://gitlab-ci.velocitywebworks.com/"
GITLAB = "https://git.velocitywebworks.com/"
# GITLAB_TOKEN = "NOT HERE ANYMORE"
GITLAB_TOKEN = "NOT HERE ANYMORE"


def get_gitlab():
    git = gitlab.Gitlab(GITLAB, private_token=GITLAB_TOKEN)
    git.auth()
    return git


@task(default=True)
def deploy():
    """Run deploy on beta then production """
    require("conf")
    for server in ['beta', 'production']:
        if server in env.roldefs:
            env.roles = [server]
            set_conf()
            execute('build', host=env.host)
            execute('test', host=env.host)
            execute('deploy', host=env.host)


@task
def get_gitlab_project():
    git_remote = local("git config --get remote.origin.url", capture=True)
    namespace, project_slug = git_remote[:-4].rsplit("/", 2)[1:]

    # urlencoded / == %2F, required if you don't have the actual id
    project_id = "%s%%2F%s" % (namespace, project_slug)
    git = get_gitlab()
    project = git.Project(project_id)
    if not project:
        print("adding permission")
        project.Member(user_id=git.currentuser()["id"], access_level="reporter")

    return project


@task
def register(command=None):

    if command is None:
        command = "fab test.script deploy -u ci_user"

    project = get_gitlab_project()

    if project:
        print("Creating project on CI server...")

        ci_project = None
        response = requests.get(
            "%sapi/v1/projects" % (GITLAB_CI,),
            data=dict(url=GITLAB),
            headers={"PRIVATE-TOKEN": GITLAB_TOKEN}
        )

        if response.ok:
            for p in response.json():
                if p['gitlab_id'] == project.id:
                    ci_project = p
                    break

        if not ci_project:
            data = dict(
                url=GITLAB,
                name=project.name,
                gitlab_id=project.id,
                gitlab_url=project.web_url,
                ssh_url_to_repo=project.ssh_url_to_repo,
                http_url_to_repo=project.http_url_to_repo,
                scripts=command
            )
            response = requests.post(
                "%sapi/v1/projects" % (GITLAB_CI,),
                data=data,
                headers={"PRIVATE-TOKEN": GITLAB_TOKEN}
            )
            if response.ok:
                ci_project = response.json()
            else:
                print("Failed to add: {}".format(response.text))
                exit(1)

        if ci_project:
            print("Registering project on GitLab...")

            # we can't get to see if it exists, so we'll try to remove it
            requests.delete(
                "%s/api/v3/projects/%s/services/gitlab-ci.json" % (
                    GITLAB, project.id),
                headers={"PRIVATE-TOKEN": GITLAB_TOKEN}
            )

            # and then add it back
            requests.put(
                "%s/api/v3/projects/%s/services/gitlab-ci.json" % (
                    GITLAB, project.id),
                data=dict(
                    token=ci_project["token"],
                    project_url="{}projects/{}".format(GITLAB_CI, ci_project["id"])
                ),
                headers={"PRIVATE-TOKEN": GITLAB_TOKEN}
            )

            # TODO: on next version update. list jobs, add if none exist
            print(("\n\nYou'll need to add a job for testing this app. "
                   "You can do so at this location:\n\n"
                   "    {gitlabci}projects/{project_id}/jobs\n\n"
                   "If you are uploading an **app**, "
                   "You should put this as the job command:\n\n"
                   "    {command}\n\n"
                   "App developers can create another job to build on tags:\n\n"
                   "    {command}\n"
                   "    python setup.py -q sdist upload -r vww\n").format(
                gitlabci=GITLAB_CI,
                project_id=ci_project['id'],
                command=command
            ))

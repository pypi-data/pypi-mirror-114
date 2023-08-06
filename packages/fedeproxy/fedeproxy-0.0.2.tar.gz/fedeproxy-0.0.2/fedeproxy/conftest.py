import os

import pytest

from fedeproxy.architecture.forge.gitea import Gitea
from fedeproxy.architecture.forge.gitlab import GitLab

gitea_url = f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781"
gitlab_url = f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8181"


@pytest.fixture(
    params=[
        (Gitea, gitea_url),
        (GitLab, gitlab_url),
    ],
    ids=[
        Gitea.__name__,
        GitLab.__name__,
    ],
)
def forge(request):
    marker = request.node.get_closest_marker("forges")
    (Forge, url) = request.param
    if marker is not None:
        forges = marker.args[0]
        if Forge.__name__ not in forges:
            pytest.skip(f"the test has a 'mark' excluding {Forge.__name__} ")
    return Forge(url)


@pytest.fixture
def password():
    return "Wrobyak4"


@pytest.fixture
def make_user(forge, password):

    usernames = []

    def _make_user(username):
        forge.authenticate(username="root", password="Wrobyak4")
        forge.user_delete(username)
        email = f"{username}@example.com"
        forge.user_create(username, password, email)
        usernames.append(username)

    yield _make_user

    forge.authenticate(username="root", password="Wrobyak4")
    for username in usernames:
        forge.user_delete(username)


@pytest.fixture
def make_project(forge, password):
    projects = []

    def _make_project(username, project):
        forge.project_delete(username, project)
        p = forge.project_create(username, project)
        projects.append((username, project))
        return p

    yield _make_project

    forge.authenticate(username="root", password=password)
    for project in projects:
        forge.project_delete(*project)

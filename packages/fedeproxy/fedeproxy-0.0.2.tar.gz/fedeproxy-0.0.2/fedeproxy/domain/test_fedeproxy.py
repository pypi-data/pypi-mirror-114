import os

import pytest

from .fedeproxy import Fedeproxy


@pytest.mark.forges(["GitLab"])
def test_fedeproxy_init(forge):
    Forge = type(forge)
    f = Fedeproxy(Forge, forge.url)
    f.init()
    assert isinstance(f.own, Forge)
    assert isinstance(f.forge, Forge)


@pytest.mark.forges(["GitLab"])
def test_fedeproxy_export(tmpdir, forge, make_user, password, make_project):
    f = Fedeproxy(type(forge), forge.url)
    f.base_directory = f"{tmpdir}/fedeproxy"
    f.init()

    username = "testuser1"
    make_user(username)
    f.forge.authenticate(username=username, password=password)
    make_project(username, "testproject")

    make_user(f.own.owner)
    f.own.authenticate(username=f.own.owner, password=password)
    make_project(f.own.namespace, "fedeproxy")

    pathname = f.project_export(username, "testproject")
    os.path.exists(pathname)

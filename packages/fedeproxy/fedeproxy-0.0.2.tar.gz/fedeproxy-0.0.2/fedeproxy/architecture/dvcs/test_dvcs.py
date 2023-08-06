import os

import pytest
import sh

from .git import Git
from .hg import Hg


def populate_repository(d):
    open(f"{d}/README.md", "w").write("# testrepo")
    open(f"{d}/info.txt", "w").write("# someinfo")


def git_repository(d):
    sh.git.init(d)
    populate_repository(d)
    sh.git("-C", d, "add", "README.md", "info.txt")
    sh.git("-C", d, "commit", "-m", "initial")
    sh.git("-C", d, "checkout", "-b", "otherbranch")


def hg_repository(d):
    sh.hg.init(d)
    open(f"{d}/.hgkeep", "w").write("# init")
    sh.hg("--cwd", d, "add", ".hgkeep")
    sh.hg("--cwd", d, "commit", "-m", "initial")

    sh.hg("--cwd", d, "branch", "master")
    populate_repository(d)
    sh.hg("--cwd", d, "add", "README.md", "info.txt")
    sh.hg("--cwd", d, "commit", "-m", "initial")

    sh.hg("--cwd", d, "branch", "otherbranch")


@pytest.fixture(
    params=[
        (Git, git_repository),
        (Hg, hg_repository),
    ],
    ids=[
        "Git",
        "Hg",
    ],
)
def dvcs(request, tmpdir):
    (DVCS, repository) = request.param
    directory = f"{tmpdir}/testrepository"
    origin = f"{tmpdir}/origin"
    repository(origin)
    return DVCS(dir=directory, url=origin)


def test_dvcs_properties(dvcs):
    assert dvcs.directory
    assert dvcs.url


def test_dvcs_clone_master(dvcs):
    assert dvcs.clone("master") is True
    assert os.path.exists(f"{dvcs.directory}/README.md")
    assert dvcs.clone("master") is False


def test_dvcs_clone_not_master(dvcs):
    assert dvcs.clone("other") is True
    assert not os.path.exists(f"{dvcs.directory}/README.md")
    assert dvcs.clone("other") is False


def test_dvcs_commit(dvcs, tmpdir):
    assert dvcs.clone("master") is True
    content = "C"
    open(f"{dvcs.directory}/README.md", "w").write(content)
    dvcs.commit("message", "README.md")
    dvcs.push("master")

    DVCS = type(dvcs)
    other_dvcs = DVCS(dir=f"{tmpdir}/other", url=dvcs.url)
    assert other_dvcs.clone("master") is True
    assert open(f"{other_dvcs.directory}/README.md").read() == content


def test_dvcs_push_pull(dvcs, tmpdir):
    assert dvcs.clone("master") is True

    DVCS = type(dvcs)
    other_dvcs = DVCS(dir=f"{tmpdir}/other", url=dvcs.url)
    assert other_dvcs.clone("master") is True
    content = "C"
    open(f"{other_dvcs.directory}/README.md", "w").write(content)
    other_dvcs.commit("message", "README.md")
    other_dvcs.push("master")

    dvcs.pull("master")
    assert open(f"{dvcs.directory}/README.md").read() == content

import os
from pathlib import Path

import git
import gitdb
import sh

from fedeproxy.interfaces.dvcs import DVCS


class Git(DVCS):
    def __init__(self, dir, url):
        self._url = url
        self.d = dir
        self.g = sh.git.bake("-C", self.d)

    @property
    def directory(self):
        return self.d

    @property
    def url(self):
        return self._url

    def clone(self, branch):
        clone = not os.path.exists(self.d)
        if clone:
            sh.git.clone(self.url, self.d)
        try:
            self.g.checkout(branch)
        except sh.ErrorReturnCode_1:
            self._create_branch(branch)
        return clone

    def _branch_exists(self, branch):
        r = git.Repo(self.d)
        try:
            r.commit(f"origin/{branch}")
            return True
        except gitdb.exc.BadName:
            return False

    def _create_branch(self, branch):
        if self._branch_exists(branch):
            return False
        self.g.checkout("--orphan", branch)
        gitkeep = f"{self.d}/.gitkeep"
        Path(gitkeep).touch()
        self.g.add(gitkeep)
        self.g.commit("-m", ".gitkeep", gitkeep)
        self.g.push("origin", branch)
        self.g.reset("--hard", branch)
        return True

    def pull(self, branch):
        self.g.checkout(branch)
        self.g.pull()

    def push(self, branch):
        self.g.checkout(branch)
        self.g.push("origin", branch)

    def commit(self, message, *pathnames):
        self.g.add(*pathnames)
        self.g.commit("-m", message)

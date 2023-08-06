import os

import sh

from fedeproxy.interfaces.dvcs import DVCS


class Hg(DVCS):
    def __init__(self, dir, url):
        self._url = url
        self.d = dir
        self.h = sh.hg.bake("--cwd", self.d)

    @property
    def directory(self):
        return self.d

    @property
    def url(self):
        return self._url

    def clone(self, branch):
        clone = not os.path.exists(self.d)
        if clone:
            sh.hg.clone(self.url, self.d)
        try:
            self.h.update(branch)
        except sh.ErrorReturnCode_255:
            self._create_branch(branch)
        return clone

    def pull(self, branch):
        self.h.pull("--branch", branch)
        self.h.update(branch)

    def push(self, branch):
        self.h.push("--branch", branch)

    def commit(self, message, *pathnames):
        self.h.add(*pathnames)
        self.h.commit("-m", message)

    def _branch_exists(self, branch):
        try:
            self.h.branches("--rev", branch)
            return True
        except sh.ErrorReturnCode_255:
            return False

    def _create_branch(self, branch):
        if self._branch_exists(branch):
            return False
        self.h.update("--rev", "0")
        self.h.branch(branch)
        self.h.commit("-m" f"create branch {branch}")
        self.h.push("--new-branch", "--branch", branch)
        return True

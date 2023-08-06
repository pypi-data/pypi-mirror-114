import copy
import logging
import time

import requests

from fedeproxy.common.retry import retry

from . import forge

logger = logging.getLogger(__name__)


class Gitea(forge.Forge):
    def __init__(self, url):
        super().__init__(url)
        self._s = requests.Session()

    def authenticate(self, **kwargs):
        self._session()
        if "token" in kwargs:
            self.set_token(kwargs["token"])
        else:
            self.login(kwargs["username"], kwargs["password"])
        self._user = self.s.get(f"{self.s.api}/user").json()

    @property
    def username(self):
        return self._user["login"]

    @property
    def is_admin(self):
        return self._user["is_admin"]

    def _session(self):
        self.s.api = f"{self.url}/api/v1"

    def login(self, username, password):
        r = self.s.post(
            f"{self.s.api}/users/{username}/tokens",
            auth=(username, password),
            json={
                "name": f"TEST{time.time()}",
            },
        )
        r.raise_for_status()
        self.set_token(r.json()["sha1"])

    def _finalize_user_create(self, username, password):
        r = self.s.post(
            f"{self.url}/user/login",
            data={
                "user_name": username,
                "password": password,
            },
        )
        r.raise_for_status()
        r = self.s.post(
            f"{self.url}/user/settings/change_password",
            data={
                "password": password,
                "retype": password,
                "_csrf": self.s.cookies["_csrf"],
            },
        )
        r.raise_for_status()

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
        self.s.headers["Authorization"] = f"token {token}"

    def user_delete(self, username):
        user = self.user_get(username)
        if user is None:
            return False
        while True:
            r = self.s.delete(f"{self.s.api}/admin/users/{username}")
            if r.status_code == 404:
                break
            logger.debug(r.text)
            r.raise_for_status()
        return True

    def user_factory(self):
        return GiteaUser

    def user_get(self, username):
        if username == self.username:
            r = self.s.get(f"{self.s.api}/user")
        elif self.is_admin:
            r = self.s.get(f"{self.s.api}/user", params={"sudo": username})
        else:
            r = self.s.get(f"{self.s.api}/users/{username}")
        if r.status_code == 404:
            return None
        else:
            r.raise_for_status()
            return self.user_factory()(self, r.json())

    def user_create(self, username, password, email):
        info = self.user_get(username)
        if info is None:
            r = self.s.post(
                f"{self.s.api}/admin/users",
                data={
                    "username": username,
                    "email": email,
                    "password": password,
                },
            )
            logger.debug(r.text)
            r.raise_for_status()
            info = r.json()
            Gitea(self.url)._finalize_user_create(username, password)
            info = self.user_get(username)
        return info

    def project_delete(self, namespace, project):
        p = self.project_get(namespace, project)
        if p is None:
            return False
        r = self.s.delete(f"{self.s.api}/repos/{namespace}/{project}")
        r.raise_for_status()
        while self.project_get(namespace, project) is not None:
            time.sleep(1)
        return True

    def project_factory(self):
        return GiteaProject

    def project_get(self, namespace, project):
        r = self.s.get(f"{self.s.api}/repos/{namespace}/{project}")
        if r.status_code == requests.codes.ok:
            return self.project_factory()(self, r.json())
        else:
            return None

    class ForkingInProgress(Exception):
        pass

    @retry(ForkingInProgress, tries=5)
    def _project_wait_fork(self, namespace, project):
        p = self.project_get(namespace, project)
        if p is None:
            raise Gitea.ForkingInProgress(f"Waiting for {namespace}/{project} fork to finish.")
        return p

    def project_fork(self, namespace, project, target_namespace=None):
        data = {}
        if target_namespace is None:
            target_namespace = self.username
        else:
            data["organization"] = target_namespace
        p = self.project_get(target_namespace, project)
        if p is not None:
            return p
        r = self.s.post(f"{self.s.api}/repos/{namespace}/{project}/forks", json=data)
        r.raise_for_status()
        return self._project_wait_fork(target_namespace, project)

    class DeletionInProgress(Exception):
        pass

    @retry(DeletionInProgress, tries=5)
    def _project_create(self, namespace, project, **data):
        data.update(
            {
                "name": project,
            }
        )
        r = self.s.post(f"{self.s.api}/user/repos", data=data)
        logger.info(r.text)
        if r.status_code == 201:
            return self.project_get(namespace, project)
        r.raise_for_status()

    def project_create(self, namespace, project, **data):
        p = self.project_get(namespace, project)
        if p is None:
            return self._project_create(namespace, project, **data)
        else:
            return p


class GiteaProject(forge.Project):
    @property
    def id(self):
        return self._project["id"]

    @property
    def namespace(self):
        return self._project["owner"]["login"]

    @property
    def project(self):
        return self._project["name"]

    def milestones_factory(self):
        return GiteaMilestones

    def issues_factory(self):
        return GiteaIssues

    @property
    def ssh_url_to_repo(self):
        return self._project["ssh_url"]

    @property
    def http_url_to_repo(self):
        return self._project["clone_url"]


class GiteaMilestones(forge.Milestones):
    def _build_url(self):
        return f"{self.s.api}/repos/{self.project.namespace}/{self.project.project}/milestones"

    def get(self, id):
        r = self.s.get(f"{self._build_url()}/{id}")
        if r.status_code == requests.codes.ok:
            return GiteaMilestone(self.project, r.json())
        else:
            return None

    def delete(self, id):
        p = self.get(id)
        if p is None:
            return False
        r = self.s.delete(f"{self._build_url()}/{id}")
        r.raise_for_status()
        return True

    def create(self, title, **data):
        data = copy.copy(data)
        data.update({"title": title})
        r = self.s.post(self._build_url(), data=data)
        logger.info(r.text)
        if r.status_code == 201:
            m = r.json()
            return self.get(m["id"])
        r.raise_for_status()

    def list(self):
        pass


class GiteaMilestone(forge.Milestone):
    @property
    def id(self):
        return self._milestone["id"]


class GiteaIssues(forge.Issues):
    def get(self, id):
        pass

    def delete(self, id):
        pass

    def create(self, title, **data):
        pass

    def list(self):
        pass


class GiteaIssue(forge.Issue):
    @property
    def id(self):
        return self._issue["iid"]

    def to_json(self):
        pass

    def from_json(self, j):
        pass


class GiteaUser(forge.User):
    @property
    def url(self):
        return f"{self.forge.url}/{self.username}"

    @property
    def username(self):
        return self._user["username"]

    @property
    def emails(self):
        return [self._user["email"]]

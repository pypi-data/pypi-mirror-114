import copy
import logging
import time

import gitlab
import requests

from fedeproxy.common.retry import retry

from . import forge

logger = logging.getLogger(__name__)


class GitLab(forge.Forge):
    def __init__(self, url):
        super().__init__(url)

    def authenticate(self, **kwargs):
        if "token" in kwargs:
            self.set_token(kwargs["token"])
        else:
            self.login(kwargs["username"], kwargs["password"])
        self._s = gitlab.Gitlab(url=self.url, oauth_token=self.token)
        self.s.auth()

    @property
    def username(self):
        return self.s.user.username

    @property
    def is_admin(self):
        return self.s.user.is_admin

    def login(self, username, password):
        r = requests.post(
            self.url + "/oauth/token",
            json={
                "username": username,
                "password": password,
                "grant_type": "password",
            },
        )
        logger.debug(r.text)
        r.raise_for_status()
        self.set_token(r.json()["access_token"])

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_namespace_id(self, name):
        r = self.s.namespaces.list(search=name)
        return r[0].id

    def user_delete(self, username):
        user = self.user_get(username)
        if user is None:
            return False
        while True:
            try:
                self.s.users.delete(user.id)
            except gitlab.exceptions.GitlabDeleteError as e:
                if e.response_code == 404:
                    break
                raise
            time.sleep(0.1)
        return True

    def user_factory(self):
        return GitLabUser

    def user_get(self, username):
        if username == self.username:
            return self.user_factory()(self, self.s.user)

        for found in self.s.users.list(username=username):
            #
            # There may be more than one match because the search is case insensitive
            #
            if found.username == username:
                return self.user_factory()(self, found)
        return None

    def user_create(self, username, password, email):
        info = self.user_get(username)
        if info is None:
            self.s.users.create(
                {
                    "name": username,
                    "username": username,
                    "email": email,
                    "password": password,
                    "skip_confirmation": True,
                }
            )
            info = self.user_get(username)
        return info

    def project_delete(self, namespace, project):
        p = self.project_get(namespace, project)
        if p is None:
            return False
        self.s.projects.delete(f"{namespace}/{project}")
        while self.project_get(namespace, project) is not None:
            time.sleep(1)
        return True

    def project_factory(self):
        return GitLabProject

    def project_get(self, namespace, project):
        try:
            p = self.s.projects.get(f"{namespace}/{project}")
            return self.project_factory()(self, p)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                return None
            raise

    class DeletionInProgress(Exception):
        pass

    @retry(DeletionInProgress, tries=5)
    def _project_create(self, namespace, project, **data):
        namespace_id = self.get_namespace_id(namespace)
        data.update(
            {
                "name": project,
                "namespace_id": int(namespace_id),
                "visibility": "public",
            }
        )
        try:
            self.s.projects.create(data)
        except gitlab.exceptions.GitlabCreateError as e:
            if e.response_code == 400 and (
                "still being deleted" in e.response_body.decode()
                or "has already been taken" in e.response_body.decode()
            ):
                raise GitLab.DeletionInProgress()
            raise
        return self.project_get(namespace, project)

    def project_create(self, namespace, project, **data):
        info = self.project_get(namespace, project)
        if info is None:
            return self._project_create(namespace, project, **data)
        else:
            return info


class GitLabProject(forge.Project):
    @property
    def id(self):
        return self._project.id

    @property
    def namespace(self):
        return self._project.namespace.path

    @property
    def project(self):
        return self._project.path

    def milestones_factory(self):
        return GitLabMilestones

    def issues_factory(self):
        return GitLabIssues

    @property
    def ssh_url_to_repo(self):
        return self._project.ssh_url_to_repo

    @property
    def http_url_to_repo(self):
        return self._project.http_url_to_repo


class GitLabMilestones(forge.Milestones):
    def get(self, id):
        pass

    def delete(self, id):
        pass

    def create(self, title, **data):
        pass

    def list(self):
        pass


class GitLabMilestone(forge.Milestone):
    @property
    def id(self):
        pass


class GitLabIssues(forge.Issues):
    def get(self, id):
        try:
            i = self.project._project.issues.get(id)
            return GitLabIssue(self.project, i)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                return None
            raise

    def delete(self, id):
        info = self.get(id)
        if info is None:
            return False
        self.project._project.issues.delete(id)
        return True

    def create(self, title, **data):
        data = copy.copy(data)
        data.update({"title": title})
        i = self.project._project.issues.create(data)
        return self.get(i.iid)

    def list(self):
        for i in self.project._project.issues.list(scope="all"):
            yield GitLabIssue(self.project, i)


class GitLabIssue(forge.Issue):
    @property
    def id(self):
        return self._issue.iid

    def to_json(self):
        i = self._issue
        j = {
            "url": i.web_url,
            "title": i.title,
            "description": i.description or "",
            "repository": self.project.http_url_to_repo,
            "user": i.author["web_url"],
            "created_at": i.created_at,
            "state": i.state == "closed" and "closed" or "open",
            "comments": [],
            "id": str(i.iid),
        }
        if i.closed_at is not None:
            j["closed_at"] = i.closed_at
        return j

    def from_json(self, j):
        self._issue.title = j["title"]
        self._issue.description = j["description"]
        self._issue.state = j["state"]
        self._issue.save()


class GitLabUser(forge.User):
    @property
    def url(self):
        return self._user.web_url

    @property
    def username(self):
        return self._user.username

    @property
    def emails(self):
        if hasattr(self._user, "email"):
            return [self._user.email]
        elif hasattr(self._user, "public_email"):
            return [self._user.public_email]
        else:
            return []

    @property
    def id(self):
        return self._user.id

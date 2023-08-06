import abc


class Persistent(abc.ABC):
    @abc.abstractmethod
    def save(self, pathname):
        ...

    @abc.abstractmethod
    def load(self, pathname):
        ...


class Forge(abc.ABC):
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @property
    def s(self):
        return self._s

    @property
    @abc.abstractmethod
    def username(self):
        ...

    @abc.abstractmethod
    def authenticate(self, **kwargs):
        ...

    @abc.abstractmethod
    def get_token(self):
        ...

    @abc.abstractmethod
    def user_factory(self):
        ...

    @abc.abstractmethod
    def user_get(self, username):
        ...

    @abc.abstractmethod
    def user_create(self, username, password, email):
        ...

    @abc.abstractmethod
    def user_delete(self, username):
        ...

    @abc.abstractmethod
    def project_factory(self):
        ...

    @abc.abstractmethod
    def project_get(self, namespace, project):
        ...

    @abc.abstractmethod
    def project_create(self, namespace, project, **data):
        ...

    @abc.abstractmethod
    def project_delete(self, namespace, project):
        ...


class Project(Persistent):
    def __init__(self, forge, project):
        self._forge = forge
        self._project = project
        self._issues = self.issues_factory()(self)
        self._milestones = self.milestones_factory()(self)

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    @property
    @abc.abstractmethod
    def id(self):
        ...

    @property
    @abc.abstractmethod
    def namespace(self):
        ...

    @property
    @abc.abstractmethod
    def project(self):
        ...

    @abc.abstractmethod
    def issues_factory(self):
        ...

    @property
    def issues(self):
        return self._issues

    @abc.abstractmethod
    def milestones_factory(self):
        ...

    @property
    def milestones(self):
        return self._milestones

    @property
    @abc.abstractmethod
    def ssh_url_to_repo(self):
        ...

    @property
    @abc.abstractmethod
    def http_url_to_repo(self):
        ...

    @abc.abstractmethod
    def dvcs_factory(self):
        ...

    @abc.abstractmethod
    def dvcs(self, directory):
        ...


class Milestones(abc.ABC):
    def __init__(self, project):
        self._project = project

    @property
    def project(self):
        return self._project

    @property
    def s(self):
        return self.project.s

    @abc.abstractmethod
    def get(self, id):
        ...

    @abc.abstractmethod
    def create(self, title, **data):
        ...

    @abc.abstractmethod
    def delete(self, id):
        ...

    @abc.abstractmethod
    def list(self):
        ...


class Milestone(abc.ABC):
    def __init__(self, project, milestone):
        self._project = project
        self._milestone = milestone

    @property
    def project(self):
        return self._project

    @property
    def s(self):
        return self.project.s

    @property
    @abc.abstractmethod
    def id(self):
        ...


class Issues(Persistent):
    def __init__(self, project):
        self._project = project

    @property
    def project(self):
        return self._project

    @property
    def s(self):
        return self.project.s

    @abc.abstractmethod
    def get(self, id):
        ...

    @abc.abstractmethod
    def create(self, title, **data):
        ...

    @abc.abstractmethod
    def delete(self, id):
        ...

    @abc.abstractmethod
    def list(self):
        ...


class Issue(abc.ABC):
    def __init__(self, project, issue):
        self._project = project
        self._issue = issue

    @property
    def project(self):
        return self._project

    @property
    def s(self):
        return self.project.s

    @property
    @abc.abstractmethod
    def id(self):
        ...

    @abc.abstractmethod
    def to_json(self):
        ...

    @abc.abstractmethod
    def from_json(self, j):
        ...


class User(abc.ABC):
    def __init__(self, forge, user):
        self._forge = forge
        self._user = user

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    @property
    @abc.abstractmethod
    def url(self):
        ...

    @property
    @abc.abstractmethod
    def username(self):
        ...

    @property
    @abc.abstractmethod
    def emails(self):
        ...

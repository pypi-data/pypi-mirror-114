import hashlib

from fedeproxy.interfaces import forge

from .identity import Identities


class Fedeproxy(object):
    def __init__(self, forge_factory, url):
        self._forge_factory = forge_factory
        self._url = url
        self.base_directory = None

    def init(self):
        self.own_forge_create()
        self.forge_create()

    @property
    def url(self):
        return self._url

    @property
    def own(self):
        return self._own

    def own_forge_create(self):
        class F(FedeproxyOwnForge, self._forge_factory):
            pass

        self._own = F(self.url)
        self.own.base_directory = self.base_directory

    @property
    def forge(self):
        return self._forge

    def forge_create(self):
        class F(FedeproxyForge, self._forge_factory):
            pass

        self._forge = F(self.url)

    def project_export(self, namespace, project):
        p = self.forge.project_create(namespace, project)
        d = self.own.project_create().dvcs()
        d.clone(p.name)
        p.save(d.directory)
        d.commit("exported project", "issues.json")
        d.push(p.name)
        return f"{d.directory}/issues.json"


class FedeproxyOwnForge(forge.Forge):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._namespace = "fedeproxy"
        self._owner = "fedeproxy"

    def init(self):
        self.identities = Identities(self)
        self.identities.init()

    @property
    def owner(self):
        return self._owner

    @property
    def namespace(self):
        return self._namespace

    def project_delete(self):
        return super().project_delete(self.namespace, "fedeproxy")

    def project_factory(self):
        class F(FedeproxyOwnProject, super().project_factory()):
            pass

        return F

    def project_create(self):
        return super().project_create(self.namespace, "fedeproxy")


class FedeproxyOwnProject(forge.Project):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dvcs(self):
        return super().dvcs(f"{self.forge.base_directory}/fedeproxy")


class FedeproxyForge(forge.Forge):
    def project_factory(self):
        class F(FedeproxyProject, super().project_factory()):
            pass

        return F


class FedeproxyProject(forge.Project):
    @property
    def name(self):
        return hashlib.sha256(self.http_url_to_repo.encode("ascii")).hexdigest()

import hashlib
import json
import os


class Identity(object):
    def __init__(self):
        self.emails = []
        self.url = None
        self.owned = False

    def is_staged(self):
        return len(self.emails) == 0

    def is_owned(self):
        return self.owned

    def serialize(self):
        return self.__dict__

    def unserialize(self, d):
        self.__dict__.update(d)
        return self


class IdentityPrivate(Identity):
    def __init__(self):
        super().__init__()
        self.token = None


class IdentityPublic(Identity):
    def from_private(self, identity):
        self.emails = [hashlib.sha256(e.encode("UTF-8")).hexdigest() for e in identity.emails]
        self.url = identity.url
        self.owned = identity.owned


class Identities(object):
    def __init__(self, forge):
        self.forge = forge
        self.email = None
        self.identities = []

    def init(self):
        self.d = self.forge.project_create().dvcs()
        self.p = f"{self.d.directory}/identities.json"
        self.load()

    def load(self):
        self.d.clone("identities")
        if os.path.exists(self.p):
            for i in json.load(open(self.p)):
                self.identities.append(self.IdentityClass().unserialize(i))
            return True
        else:
            return False

    def save(self):
        self.identities = [i.serialize() for i in self.identities]
        json.dump(self.identities, open(self.p, "w"))


class IdentitiesPrivate(Identities):

    IdentityClass = IdentityPrivate


class IdentitiesPublic(Identity):

    IdentityClass = IdentityPublic

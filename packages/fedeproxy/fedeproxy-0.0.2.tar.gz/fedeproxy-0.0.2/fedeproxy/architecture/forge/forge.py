import ndjson
from furl import furl

from ...format import format
from ...interfaces import forge
from ..dvcs import git


class Forge(forge.Forge):
    pass


class Project(forge.Project):
    def save(self, pathname):
        self.issues.save(f"{pathname}/issues.json")

    def load(self, pathname):
        return self.issues.load(f"{pathname}/issues.json")

    def dvcs_factory(self):
        return git.Git

    def dvcs(self, directory):
        o = furl(self.http_url_to_repo)
        o.username = "oauth2"
        o.password = self.forge.get_token()
        return self.dvcs_factory()(directory, o.tostr())


class Milestones(forge.Milestones):
    pass


class Milestone(forge.Milestone):
    pass


class Issues(forge.Issues):
    def save(self, pathname):
        with open(pathname, "w") as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for i in self.list():
                writer.writerow(i.to_json())

    def load(self, pathname):
        fi = format.FormatIssue()
        count = 0
        with open(pathname) as f:
            for j in ndjson.reader(f):
                fi.validate(j)
                self.create_from_json(j)
                count += 1
        return count

    def create_from_json(self, j):
        i = self.get(j["id"])
        if i is None:
            i = self.create(j["title"])
        i.from_json(j)


class Issue(forge.Issue):
    pass


class User(forge.User):
    pass

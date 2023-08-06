import json
import logging
import os

from jschon import JSON, Catalogue, JSONSchema

logger = logging.getLogger(__name__)

Catalogue.create_default_catalogue("2020-12")


class LoadError(Exception):
    pass


class Format(object):
    def __init__(self):
        self.d = f"{os.path.dirname(__file__)}/data"
        self.schema = None

    def load(self, filename):
        return json.load(open(filename))

    def save(self, filename, data):
        json.dump(data, open(filename, "w"))

    def validate(self, data):
        j = JSON(data)
        r = self.schema.evaluate(j)
        if r.valid:
            return True
        logger.error(r.output("verbose"))
        raise LoadError(j.path)


class FormatIssue(Format):
    def __init__(self):
        super().__init__()
        JSONSchema.loadf(f"{self.d}/comment.json")
        self.schema = JSONSchema.loadf(f"{self.d}/issue.json")

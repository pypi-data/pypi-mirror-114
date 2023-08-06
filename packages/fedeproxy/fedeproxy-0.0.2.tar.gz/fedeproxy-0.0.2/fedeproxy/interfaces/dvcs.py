import abc


class DVCS(abc.ABC):
    @abc.abstractmethod
    def __init__(self, dir, url):
        ...

    @property
    @abc.abstractmethod
    def directory(self):
        ...

    @property
    @abc.abstractmethod
    def url(self):
        ...

    @abc.abstractmethod
    def clone(self, branch):
        ...

    @abc.abstractmethod
    def pull(self, branch):
        ...

    @abc.abstractmethod
    def push(self, branch):
        ...

    @abc.abstractmethod
    def commit(self, message, *pathnames):
        ...

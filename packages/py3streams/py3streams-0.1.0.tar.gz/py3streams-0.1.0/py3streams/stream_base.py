from abc import ABC, abstractmethod
from .optional import Optional


class StreamBase(ABC):

    def __init__(self, iterable_object):
        self.iterable_object = iterable_object
        self.lazy_actions = []

    def get_lazy(self):
        return self.lazy_actions[-1] if len(self.lazy_actions) > 0 else (self.iterable_object.items() if isinstance(self.iterable_object, dict) else self.iterable_object)

    def add(self, generator):
        self.lazy_actions.append(generator)

    def get_first(self, default_value=None):
        return Optional.of(next(self.__iter__(), default_value))

    def __iter__(self):
        yield from self.get_lazy()

    def operations(self):
        return self.lazy_actions

    def fmap(self, func):
        from .dict_stream import DictStream
        def _wrap(streams):
            for s in streams:
                yield from (s.iterable_object.items() if isinstance(s, DictStream) else s.iterable_object)

        self.add(_wrap((func(i) for i in self.get_lazy())))
        return self

    @abstractmethod
    def filter(self, func):
        pass

    @abstractmethod
    def map(self, func):
        pass

    @abstractmethod
    def to_list(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def reverse(self):
        pass

    @abstractmethod
    def limit(self, limit):
        pass



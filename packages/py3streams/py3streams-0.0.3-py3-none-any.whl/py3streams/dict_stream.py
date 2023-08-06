
from .stream_base import StreamBase
from .stream import Stream


class DictStream(StreamBase):

    def __init__(self, value: dict):
        super().__init__(value)

    def filter(self, func):
        self.add((k, v) for k, v in self.get_lazy() if func(k, v))
        return self

    def map(self, func):
        self.add((func(k, v) for k, v in self.get_lazy()))
        return self

    def to_list(self):
        return list(self.get_lazy())

    def to_dict(self):
        return {k:v for k,v in self.get_lazy()}

    def items(self):
        return self.__iter__()

    def values(self):
        return Stream((v for _, v in self.get_lazy()))

    def keys(self):
        return Stream((k for k, _ in self.get_lazy()))

    def limit(self, limit):
        def _wrap(iterator):
            for i, e in enumerate(iterator):
                if i < limit:
                    yield e
                else:
                    break

        self.add(_wrap(self.get_lazy()))

    def reverse(self):
        raise NotImplementedError("Method cannot be implemented in dict, because of no order")


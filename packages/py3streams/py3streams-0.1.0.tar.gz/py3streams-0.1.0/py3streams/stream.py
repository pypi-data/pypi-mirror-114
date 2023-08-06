
from .stream_base import StreamBase
import re


class Stream(StreamBase):

    REGEX_DIGITS = re.compile(r'^\d+\.{0,1}\d*$')

    def __init__(self, value):
        super().__init__(value)

    def filter(self, func):
        self.add((i for i in self.get_lazy() if func(i)))
        return self

    def map(self, func):
        self.add((func(i) for i in self.get_lazy()))
        return self

    def to_dict(self):
        raise NotImplementedError("Method is not implemented for Stream. Use Dictstream instead.")

    def to_list(self):
        return [e for e in self.get_lazy()]

    def limit(self, limit):
        def _wrap(gen):
            for i, e in enumerate(gen):
                if i < limit:
                    yield e
                else:
                    break
        self.add(_wrap(self.get_lazy()))
        return self

    def reverse(self):
        return reversed(self.to_list())

    def joining(self, delimiter):
        return delimiter.join(self.get_lazy())

    def map_to_str(self):
        return self.map(lambda x: str(x))

    def map_to_int(self):
        return self.map(lambda x: int(x))

    def map_to_float(self):
        return self.map(lambda x: float(x))

    def count(self):
        return sum(1 for _ in self.get_lazy())

    def any_match(self, func):
        return any(func(i) for i in self.get_lazy())

    def all_match(self, func):
        return all(func(i) for i in self.get_lazy())

    def only_dict(self):
        return self.filter(lambda x: isinstance(x, dict))

    def only_list(self):
        return self.filter(lambda x: isinstance(x, (list, set, tuple)))

    def only_digits(self):
        return self.filter(lambda x: isinstance(x, (int, float)) or (isinstance(x, (str, bytes)) and self.REGEX_DIGITS.match(x)))

    def sum(self):
        return sum(self.get_lazy())

    def max(self):
        return max(self.get_lazy())

    def min(self):
        return min(self.get_lazy())

    def no_none(self):
        return self.filter(lambda x: x is not None)

    def no_list(self):
        return self.filter(lambda x: not isinstance(x, (list, set, tuple)))

    def exists(self):
        return self.filter(lambda x: x)

    def even(self):
        return self.filter(lambda x: x%2 == 0)

    def odd(self):
        return self.filter(lambda x: (x%2 - 1) == 0)

    def gt(self, value):
        return self.filter(lambda x: x > value)

    def lt(self, value):
        return self.filter(lambda x: x < value)

    def ge(self, value):
        return self.filter(lambda x: x >= value)

    def le(self, value):
        return self.filter(lambda x: x <= value)

    def eq(self, value):
        return self.filter(lambda x: x == value)



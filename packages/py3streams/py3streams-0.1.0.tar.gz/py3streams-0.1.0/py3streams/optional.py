

def no_empty(value):
    return (value is not None) and value


def is_empty(value):
    return (value is None) or (not value)


def get_or_else(value, default_value=None):
    return value if no_empty(value) else default_value


class Optional:

    _EMPTY = None

    def __init__(self, data: object):
        self._data = data

    @classmethod
    def empty(cls):
        if cls._EMPTY is None:
            cls._EMPTY = Optional(cls._EMPTY)
        return cls._EMPTY

    @classmethod
    def of(cls, data: object):
        return cls.empty() if is_empty(data) else Optional(data)

    def get(self):
        return self._data

    def get_or_else(self, default_value):
        return get_or_else(self._data, default_value)

    @property
    def present(self):
        return no_empty(self._data)

    def is_present(self):
        return self.present

    def if_present(self, func, default_value=None):
        return func(self._data) if self.present else default_value


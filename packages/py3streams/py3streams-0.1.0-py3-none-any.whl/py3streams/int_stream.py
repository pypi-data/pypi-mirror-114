"""
IntStream module. Includes IntStream class which extends Stream.
"""
from .stream import Stream


class IntStream(Stream):
    """
    Constructor takes 3 arguments similar to range() method.

    :param start: int range's start value,
    :param end: int range's end value,
    :param step: int range's step. Default is '1'.
    """

    def __init__(self, start: int, end: int, step: int = 1):
        super().__init__(range(start, end, step))


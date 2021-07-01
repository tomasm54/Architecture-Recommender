import abc
from tour.iterator.iterator import Iterator


class Visitor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def visit_sequential(self, it: Iterator) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def visit_global(self, it: Iterator) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def visit_neutral(self, it: Iterator) -> str:
        raise NotImplementedError

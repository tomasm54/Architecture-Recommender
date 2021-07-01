import abc
from typing import Dict, List

from tour import iterator 

class Visitor(metaclass=abc.ABCMeta):
    
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def visit_sequential(it : iterator.SequentialIterator) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def visit_global(it : iterator.GlobalIterator) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def visit_neutral(it : iterator.NeutralIterator) -> str:
        raise NotImplementedError

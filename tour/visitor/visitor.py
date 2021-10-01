import abc
from tour.conversation_flow.conversation_flow import ConversationFlow


class Visitor(metaclass=abc.ABCMeta):
    """
    Abstract implementation of Visitor design pattern.
    """
    @abc.abstractmethod
    def visit_sequential(self, it: ConversationFlow) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def visit_global(self, it: ConversationFlow) -> str:
        raise NotImplementedError

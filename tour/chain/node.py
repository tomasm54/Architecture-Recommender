import abc


from rasa.shared.core.trackers import DialogueStateTracker

from tour.chain.criterion import Criterion
from tour.visitor.get_topic import GetTopic
from tour.iterator.iterator import Iterator
from tour.visitor.ask import Ask
from tour.visitor.example import Example


class Node(metaclass=abc.ABCMeta):

    def __init__(self, criterion: Criterion) -> None:
        self._criterion = criterion

    @abc.abstractmethod
    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        raise NotImplementedError


class NodeGet(Node):

    def __init__(self, node: Node, criterion: Criterion, jump: bool = None, example: bool = None) -> None:
        self._node = node
        self._jump = jump
        self._example = example
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            if self._jump is not None:
                it.set_jump(self._jump)
                return it.accept(GetTopic(it.get_current_topic(),self._example))
            if self._example is not None:
                return it.accept(GetTopic(it.get_current_topic(),self._example))
            return it.accept(GetTopic(next(tracker.get_latest_entity_values("tema"), None),self._example))
        else:
            return self._node.next(it, tracker)


class DefaultNode(Node):

    def __init__(self, criterion: Criterion) -> None:
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        return "utter_default"


class NodeActionListen(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        super().__init__(criterion)
        self._node = node

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return "action_listen"
        else:
            return self._node.next(it, tracker)

class NodeRepeat(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return it.repeat()
        else:
            return self._node.next(it, tracker)

class NodeNext(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return it.next()
        else:
            return self._node.next(it, tracker)

class NodeAsk(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return it.accept(Ask())
        else:
            return self._node.next(it, tracker)

class NodeExample(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return it.accept(Example(next(tracker.get_latest_entity_values("tema"), None)))
        else:
            return self._node.next(it, tracker)

class NodeResponse(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            if tracker.latest_message.intent["name"]==it.get_to_explain()[-1].get_question():
                return "utter_ask_good"
            else: 
                return "utter_ask_bad"
        else:
            return self._node.next(it, tracker)

class NodeReset(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)

    def next(self, it: Iterator, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            it.restart()
            return it.next()
        else:
            return self._node.next(it, tracker)




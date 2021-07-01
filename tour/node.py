
import abc
from tour.criterion import Criterion

from tour import get_topic

from rasa.shared.core.trackers import DialogueStateTracker

from tour import iterator
from typing import Dict, Iterator, List



class Node(metaclass=abc.ABCMeta):
    
    def __init__(self, criterion : Criterion) -> None:
        self._criterion = criterion

    @abc.abstractmethod
    def next(self, it : iterator.Iterator, tracker : DialogueStateTracker) -> str:
        raise NotImplementedError
    
class NodeGet(Node):
    
    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)
    
    def next(self, it : iterator.Iterator, tracker : DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return it.accept(get_topic.GetTopic(next(tracker.get_latest_entity_values("tema"), None)))
        else: 
            return self._node.next(it,tracker)

class DefaultNode(Node):

    def __init__(self, criterion: Criterion) -> None:
        super().__init__(criterion)

    def next(self, it : iterator.Iterator, tracker : DialogueStateTracker) -> str:
        return "utter_default"
    
class NodeActionListen(Node):
    
    def __init__(self, node: Node, criterion: Criterion) -> None:
        super().__init__(criterion)
        self._node = node
    
    def next(self, it : iterator.Iterator, tracker : DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return "action_listen"
        else: 
            return self._node.next(it,tracker)

class NodeNext(Node):
    
    def __init__(self, node: Node, criterion: Criterion) -> None:
        self._node = node
        super().__init__(criterion)
    
    def next(self, it : iterator.Iterator, tracker : DialogueStateTracker) -> str:
        if self._criterion.check(tracker):
            return it.next()
        else: 
            return self._node.next(it,tracker)
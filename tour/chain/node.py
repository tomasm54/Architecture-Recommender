import abc
import json
from tour.arch_designer import find_architecture
from tour.topic.topics import parse_topic
from tour.visitor.next_topic import NextTopic

from rasa.shared.core.trackers import DialogueStateTracker

from tour.chain.criterion import Criterion
from tour.visitor.get_topic import GetTopic
from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.visitor.ask import Ask
from tour.visitor.example import Example


class Node(metaclass=abc.ABCMeta):
    """
    Abstract node of the chain of responsibility

    Author: Adrian
    """
    def __init__(self, criterion: Criterion) -> None:
        """
        Constructor of the abstract node

        Author: Adrian

        Parameters
        ----------

        criterion
            Criterion to check to go to the next node or doing some function.
        """
        self._criterion = criterion

    @abc.abstractmethod
    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        Abstract next method, that each concrete node has to define.

        Author: Adrian

        Parameters
        ----------

        it
            Current conversation_flow to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        raise NotImplementedError

class NodeRequirement(Node):

    def __init__(self, node: Node, criterion: Criterion, flows: dict) -> None:
        super().__init__(criterion)
        self._node = node
        self._flows = flows
    
    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(it,tracker):
            arch = find_architecture(tracker.latest_message.text)
            if arch is None:
                return "utter_no_architecture"
            else:
                if arch in self._flows:
                    with open(self._flows[arch]) as file:
                        flow = [parse_topic(raw_topic) for raw_topic in json.load(file)]
                    it.load(flow)
                    return "utter_architecture"
                else:
                    return "utter_no_explain"               
        else:
            return self._node.next(it, tracker)

class NodeExplain(Node):

    def __init__(self, node: Node, criterion: Criterion, flows: dict) -> None:
        super().__init__(criterion)
        self._node = node
        self._flows = flows
    
    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(it,tracker):
            tema = next(tracker.get_latest_entity_values("tema"), None)
            if tema is None:
                return "utter_no_tema"
            else:
                print(tema)
                if tema in self._flows:
                    with open(self._flows[tema]) as file:
                        flow = [parse_topic(raw_topic) for raw_topic in json.load(file)]
                    it.load(flow)
                    return "utter_architecture"
                else:
                    return "utter_no_explain"               
        else:
            return self._node.next(it, tracker)

class NodeGivesRequirement(Node):

    def __init__(self, node: Node, criterion: Criterion) -> None:
        super().__init__(criterion)
        self._node = node

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        if self._criterion.check(it,tracker):
            empty = []
            it.load(empty)
            return "utter_requirement"
        else:
            return self._node.next(it, tracker)

class DefaultNode(Node):
    """
    Node that describes as a default action. It is used when none of the nodes criterion is checked.

    Author: Adrian
    """

    def __init__(self, criterion: Criterion) -> None:
        """
        Constructor of the node

        Author: Adrian

        Parameters
        ----------

        criterion
            Criterion to check if it has to make the functionality specified in the node or it has to go to the next node.
        """
        super().__init__(criterion)

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        Default utter.

        Author: Adrian

        Parameters
        ----------

        it
            Current conversation_flow to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns a default utter.
        """
        return "utter_default"


class NodeActionListen(Node):
    """
    Node that returns the action listen if the criterion is checked as true.
    """

    def __init__(self, node: Node, criterion: Criterion) -> None:
        """
        Constructor of the node

        Author: Adrian

        Parameters
        ----------

        node
            Next node.
        criterion
            Criterion to check if it has to make the functionality specified in the node or it has to go to the next node.
        """
        super().__init__(criterion)
        self._node = node

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        If the criterion is true, it returns an "action_listen", else it checks the next node

        Author: Adrian

        Parameters
        ----------

        it
            Current conversation_flow to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns an "action_listen"
        """
        if self._criterion.check(it,tracker):
            return "action_listen"
        else:
            return self._node.next(it, tracker)


class NodeRepeat(Node):
    """
    Repeats the explanation if the criterion is true

    Author: Tomas
    """

    def __init__(self, node: Node, criterion: Criterion) -> None:
        """
        Constructor of the node

        Author: Tomas

        Parameters
        ----------

        node
            Next node.
        criterion
            Criterion to check if it has to make the functionality specified in the node or it has to go to the next node.
        """
        self._node = node
        super().__init__(criterion)

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        If the criterion is true, it repeats the current topic's explanation, else it checks the next node

        Author: Tomas

        Parameters
        ----------

        it
            Current conversation_flow to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns the current topic's explanation repetition
        """
        if self._criterion.check(it,tracker):
            return it.repeat()
        else:
            return self._node.next(it, tracker)


class NodeNext(Node):
    """
    Node that does the next explanation in the conversation flow if the criterion is checked as true.

    Author: Adrian
    """
    def __init__(self, node: Node, criterion: Criterion) -> None:
        """
        Constructor of the node

        Author: Adrian

        Parameters
        ----------

        node
            Next node.
        criterion
            Criterion to check if it has to make the functionality specified in the node or it has to go to the next node.
        """
        self._node = node
        super().__init__(criterion)

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        Returns the next explanation from the conversation flow

        Author: Adrian

        Parameters
        ----------

        it
            Current conversation_flow to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns the next explanation from the conversation flow depending on the learning style from the conversation_flow if
        the criterion is checked as true, otherwise it checks the next node.
        """
        if self._criterion.check(it,tracker):
            return it.accept(NextTopic())
        else:
            return self._node.next(it, tracker)



class NodeExample(Node):
    """
    Node that calls the Example visitor if the criterion is checked as true, otherwise it checks the next node.

    Author: Adrian
    """
    def __init__(self, node: Node, criterion: Criterion) -> None:
        """
        Constructor of the node

        Author: Adrian

        Parameters
        ----------

        node
            Next node.
        criterion
            Criterion to check if it has to make the functionality specified in the node or it has to go to the next node.
        """
        self._node = node
        super().__init__(criterion)

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        Calls the Example visitor if the criterion is checked as true, otherwise it checks the next node.

        Author: Adrian

        Parameters
        ----------

        it
            Current conversation_flow to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        if self._criterion.check(it,tracker):
            return it.accept(Example(next(tracker.get_latest_entity_values("tema"), None)))
        else:
            return self._node.next(it, tracker)


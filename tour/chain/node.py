import abc

from rasa.shared.core.trackers import DialogueStateTracker

from tour.chain.criterion import Criterion
from tour.visitor.get_topic import GetTopic
from tour.iterator.conversation_flow import ConversationFlow
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
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        raise NotImplementedError


class NodeGet(Node):
    """
    Node that uses the GetTopic visitor
    """

    def __init__(self, node: Node, criterion: Criterion, jump: bool = None, example: bool = None) -> None:
        """
        Constructor of the node

        Author: Tomas

        Parameters
        ----------

        node
            Next node.
        criterion
            Criterion to check if it has to make the functionality specified in the node or it has to go to the next node.
        jump
            Boolean to make the decision to jump or not. Default value = None.
        example
            Boolean value to check if the user wants an example or not. Default value = None.
        """
        self._node = node
        self._jump = jump
        self._example = example
        super().__init__(criterion)

    def next(self, it: ConversationFlow, tracker: DialogueStateTracker) -> str:
        """
        If the criterion is checked as true, it does the visitor functionality,
        otherwise it checks the next node.

        Author: Tomas

        Parameters
        ----------

        it
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        if self._criterion.check(tracker):
            if self._jump is not None:
                it.set_jump(self._jump)
                return it.accept(GetTopic(it.get_current_topic(), self._example))
            if self._example is not None:
                return it.accept(GetTopic(it.get_current_topic(), self._example))
            return it.accept(GetTopic(next(tracker.get_latest_entity_values("tema"), None), self._example))
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
            Current iterator to iterate over the conversation flow.
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
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns an "action_listen"
        """
        if self._criterion.check(tracker):
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
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns the current topic's explanation repetition
        """
        if self._criterion.check(tracker):
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
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        Returns the next explanation from the conversation flow depending on the learning style from the iterator if
        the criterion is checked as true, otherwise it checks the next node.
        """
        if self._criterion.check(tracker):
            return it.next()
        else:
            return self._node.next(it, tracker)


class NodeAsk(Node):
    """
    Node that calls the Ask visitor if the criterion is checked.

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
        Calls the Ask visitor if the criterion is checked as true, otherwise it checks the next node.

        Author: Tomas

        Parameters
        ----------

        it
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        if self._criterion.check(tracker):
            return it.accept(Ask())
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
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        if self._criterion.check(tracker):
            return it.accept(Example(next(tracker.get_latest_entity_values("tema"), None)))
        else:
            return self._node.next(it, tracker)


class NodeResponse(Node):
    """
    Node that checks the response of the user to the question made.

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
        Checks if the answer made by the student is right to the question made if the criterion is true,
        otherwise it checks the next node.

        Author: Tomas

        Parameters
        ----------

        it
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.

        Returns
        -------

        "utter_ask_good" if the answer was right
        "utter_ask_bad" if the answer was not right
        """
        if self._criterion.check(tracker):
            if tracker.latest_message.intent["name"] == it.get_to_explain()[-1].get_question():
                return "utter_ask_good"
            else:
                return "utter_ask_bad"
        else:
            return self._node.next(it, tracker)


class NodeReset(Node):
    """
    Node that resets the conversation flow.

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
        Resets the conversation flow if the criterion is checked as true, otherwise it checks the next node.

        Author: Adrian

        Parameters
        ----------

        it
            Current iterator to iterate over the conversation flow.
        tracker
            Rasa tracker.
        """
        if self._criterion.check(tracker):
            it.restart()
            return it.next()
        else:
            return self._node.next(it, tracker)

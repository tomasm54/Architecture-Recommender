from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.visitor.visitor import Visitor

AMT_EXAMPLE_NEUTRAL = 2


class Example(Visitor):
    """
    Concrete implementation of Visitor, it returns the example of a specified topic
    """
    def __init__(self, topic: str = None) -> None:
        """
        Constructor

        Author: Adrian

        Parameters
        ----------

        topic
            ID of the specified topic
        """
        self._topic = topic

    def visit_sequential(self, it: ConversationFlow) -> str:
        """
        Concrete implementation that describes the behaviour of a Sequential learning style student.
        It gives each one of the examples to the student.

        Author: Adrian

        Parameters
        ----------

        it
            Sequential

        Returns
        -------

        utter associated to the example of the specified topic.
        """
        example = self.search(it)
        if example is None:
            return it.get_intents_to_topic()[self._topic].get_example()
        return example

    def visit_global(self, it: ConversationFlow) -> str:
        """
        Concrete implementation that describes the behaviour of a Global learning style student.
        It gives only the first example of the specified topic.

        Author: Adrian

        Parameters
        ----------

        it
            Global

        Returns
        -------

        utter associated to the example of the specified topic.
        """
        example = self.search(it)
        if example is None:
            example = it.get_intents_to_topic()[self._topic].get_example()
            it.get_intents_to_topic()[self._topic].set_current_example(0)
        return example

    def visit_neutral(self, it: ConversationFlow) -> str:
        """
        Concrete implementation that describes the behaviour of a Neutral learning style student.
        It gives @AMT_EXAMPLE_NEUTRAL examples of the specified topic.

        Author: Adrian

        Parameters
        ----------

        it
            Neutral

        Returns
        -------

        utter associated to the example of the specified topic.
        """
        example = self.search(it)
        if example is None:
            example = it.get_intents_to_topic()[self._topic].get_example()
            if it.get_intents_to_topic()[self._topic].get_current_example() > AMT_EXAMPLE_NEUTRAL:
                it.get_intents_to_topic()[self._topic].set_current_example(0)
        return example

    def search(self, it: ConversationFlow) -> str:
        """
        Searches the utter associated to the example of the specified topic

        Author: Adrian

        Parameters
        ----------

        it
            Concrete conversation_flow

        Returns
        -------

        utter associated to the example of the specified topic
        "action_topic_not_recognized" when @_topic is not in intents_to_topic.json
        None if the specified topic is a valid topic.
        """
        if self._topic is None:
            return it.get_to_explain()[-1].get_example()
        else:
            if self._topic not in it.get_intents_to_topic():
                return "action_topic_not_recognized"
            else:
                return None

from tour.topic.topics import Topic
from tour.iterator.conversation_flow import ConversationFlow
from tour.visitor.visitor import Visitor


class GetTopic(Visitor):
    """
    Concrete implementation of Visitor, it returns the explanation of a specified topic
    """
    def __init__(self, topic: str, example: bool = None) -> None:
        """
        Constructor

        Author: Tomas

        Parameters
        ----------

        topic
            ID of the specified topic
        example
            Boolean value that means that user wants an example of the specified topic if it is True, or does not
            want an example if it is False. Default value = None.
        """
        self._topic = topic
        self._example = example

    def visit_sequential(self, it: ConversationFlow) -> str:
        """
        Concrete implementation that describes the behaviour of a sequential learning style student.
        If the specified topic has already been explained, it checks if the user wants to jump to that topic
        and get those explanations again, otherwise, it does the explanation.

        Author: Tomas

        Parameters
        ----------

        it
            Sequential Iterator

        Returns
        -------

        Utter associated with the explanation/example the user wants.
        """
        if it.is_older_topic(Topic(self._topic, [])):
            if it.get_jump() is None:
                it.set_current_topic(self._topic)
                return "utter_cross_examine_jump_sequential"
            else:
                return self.get_topic(it)
        else:
            return self.get_topic(it)

    def visit_global(self, it: ConversationFlow) -> str:
        """
        Concrete implementation that describes the behaviour of a global learning style student.
        If the specified topic has not been explained yet, it checks if the user wants to jump to
        that specified topic. No matter if the students wants to make the jump or not,
        the response is the utter associated to the topic the user wants.

        Author: Tomas

        Parameters
        ----------

        it
            Global Iterator

        Returns
        -------

        Utter associated with the explanation/example the user wants.
        """
        if not it.is_older_topic(Topic(self._topic, [])) and not it.get_to_explain()[-1].get_id() == self._topic:
            if it.get_jump() is None:
                it.set_current_topic(self._topic)
                return "utter_cross_examine_jump_global"
            else:
                return self.get_topic(it, it.get_jump())
        else:
            return self.get_topic(it)

    def visit_neutral(self, it: ConversationFlow) -> str:
        """
        Concrete implementation that describes the behaviour of a neutral learning style student.
        Respond the explanation/example without checking the jump.

        Author: Tomas

        Parameters
        ----------

        it
            Neutral Iterator

        Returns
        -------

        Utter associated with the explanation/example the user wants.
        """
        return self.get_topic(it)

    def get_topic(self, it: ConversationFlow, jump: bool = False) -> str:
        """
        Returns the explanation/example according to the parameters and attributes given.

        Author: Tomas

        Parameters
        ----------

        it
            concrete ConversationFlow
        jump
            Boolean value to check if the student wants to make the jump or not. Default value = None.

        Returns
        -------

        "utter_cross_examine_example" when the topic has already been explained and @_example takes its default value.
        "action_topic_not_recognized" when the topic is not in the domain of the explanations.
        Returns an example if @_example is True.
        If none of the above are satisfied, it returns the topic explanation.
        """
        if it.is_older_topic(Topic(self._topic, [])):
            if self._example == None:
                it.set_current_topic(self._topic)
                return "utter_cross_examine_example"
        if self._topic not in it.get_intents_to_topic():
            return "action_topic_not_recognized"
        if jump:
            it.jump_to_topic(Topic(self._topic, []))
        if self._example == True:
            return it.get_intents_to_topic()[self._topic].get_example()
        return it.get_intents_to_topic()[self._topic].get_explanation()

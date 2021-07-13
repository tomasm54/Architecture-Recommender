from tour.topic.topics import Topic
from tour.iterator.conversation_flow import ConversationFlow
from tour.visitor.visitor import Visitor
from random import randint


class Ask(Visitor):
    """
    Concrete implementation of Visitor, it returns the question of a specified topic
    """
    def __init__(self) -> None:
        """
        Constructor

        Author: Adrian
        """
        super().__init__()

    def visit_sequential(self, it: ConversationFlow) -> str:
        """
        Get a question from a random topic in conversation flow.

        Author: Adrian

        Parameters
        ----------

        it
            Sequential Iterator

        Returns
        -------

        utter associated to a question from a random topic in conversation flow.
        """
        return self.search_question(it)

    def visit_global(self, it: ConversationFlow) -> str:
        """
        Get a question from a random subtopic in conversation flow.

        Author: Adrian

        Parameters
        ----------

        it
            Global Iterator

        Returns
        -------

        utter associated to a question from a random subtopic in conversation flow.
        """
        return self.search_question(it)

    def visit_neutral(self, it: ConversationFlow) -> str:
        """
        Get a question from a random topic in conversation flow.

        Author: Adrian

        Parameters
        ----------

        it
            Neutral Iterator

        Returns
        -------

        utter associated to a question from a random topic in conversation flow.
        """
        return self.search_question(it)

    def search_question(self, it: ConversationFlow) -> str:
        """
        Get a question from a random topic in conversation flow.

        Author: Adrian

        Parameters
        ----------

        it
            Concrete ConversationFlow

        Returns
        -------

        utter associated to a question from a random topic in conversation flow.
        """
        respond = "utter_sin_question"
        it.restart()
        question : int
        keys = list(it.get_intents_to_topic().keys())
        while respond.find("utter_cross_examine")==-1:
            question = randint(0, len(it.get_intents_to_topic()) - 1)
            respond = it.get_intents_to_topic()[keys[question]].get_question()
        it.jump_to_topic(Topic(keys[question],[]))
        return respond
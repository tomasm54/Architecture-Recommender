from tour.topic.topics import Topic
from typing import Dict, List
from tour.iterator.conversation_flow import ConversationFlow
from tour.visitor.visitor import Visitor


class SequentialIterator(ConversationFlow):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        """
        Sequential learning style constructor.

        Author: Tomas
        """
        super().__init__(intents_to_topics, flow)

    def next(self) -> str:
        """
        Get the next utter with a conversation flow iteration that describes a sequential person.
        It enters to the main topic and each one of the subtopics.

        Author: Tomas

        Returns
        -------

        Utter associated to the next explanation for a Sequential person.
        """
        while len(self._to_explain) > 0 and self._to_explain[-1].is_explained:
            next_to_explain = self._to_explain[-1].next()
            if next_to_explain is None:
                self._to_explain.pop()
            else:
                self._to_explain.append(next_to_explain)

        if len(self._to_explain) == 0:
            return "utter_ask"

        return self._to_explain[-1].get_explanation()

    def accept(self, visitor: Visitor) -> str:
        """
        Accepts the visitor

        Author: Tomas

        Returns
        -------

        Utter associated to the visitor functionality.
        """
        return visitor.visit_sequential(self)


class GlobalIterator(ConversationFlow):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        """
        Global learning style constructor.

        Author: Adrian
        """
        super().__init__(intents_to_topics, flow)

    def next(self) -> str:
        """
        Iterates over the conversation flow not entering in the subtopics of the topic, describing a global person

        Author: Adrian.

        Returns
        -------
            Utter associated to the next topic.
        """
        if self._to_explain[-1].is_explained:
            self._to_explain.pop()
        if len(self._to_explain) == 0:
            return "utter_ask"

        return self._to_explain[-1].get_explanation()

    def accept(self, visitor: Visitor) -> str:
        """
        Accepts the visitor

        Author: Adrian

        Returns
        -------

        Utter associated to the visitor functionality.
        """
        return visitor.visit_global(self)


class NeutralIterator(ConversationFlow):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        """
        Global learning style constructor.

        Author: Tomas
        """
        super().__init__(intents_to_topics, flow)

    def next(self) -> str:
        """
        Iterates over the conversation flow entering only in the first subtopic of the topic, describing a Neutral person

        Author: Tomas.

        Returns
        -------
            Utter associated to the next topic.
        """
        while len(self._to_explain) > 0 and self._to_explain[-1].is_explained:
            if self._to_explain[-1].get_amount_subtopics() < 1:
                next_to_explain = self._to_explain[-1].next()
                if next_to_explain is None:
                    self._to_explain.pop()
                else:
                    self._to_explain.append(next_to_explain)
            else:
                self._to_explain.pop()

        if len(self._to_explain) == 0:
            return "utter_ask"

        return self._to_explain[-1].get_explanation()

    def accept(self, visitor: Visitor) -> str:
        """
        Accepts the visitor

        Author: Tomas

        Returns
        -------

        Utter associated to the visitor functionality.
        """
        return visitor.visit_neutral(self)

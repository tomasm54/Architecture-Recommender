import json
from tour.topic.topics import Topic, parse_topic
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

    def accept(self, visitor: Visitor) -> str:
        """
        Accepts the visitor

        Author: Tomas

        Returns
        -------

        Utter associated to the visitor functionality.
        """
        return visitor.visit_sequential(self)
     
    def load(intents_to_topics: Dict[str, str], flow: List[Topic])-> ConversationFlow:
        return SequentialIterator(intents_to_topics, flow)



class GlobalIterator(ConversationFlow):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        """
        Global learning style constructor.

        Author: Adrian
        """
        super().__init__(intents_to_topics, flow)

    def accept(self, visitor: Visitor) -> str:
        """
        Accepts the visitor

        Author: Adrian

        Returns
        -------

        Utter associated to the visitor functionality.
        """
        return visitor.visit_global(self)
        
    def load(intents_to_topics: Dict[str, str], flow: List[Topic])-> ConversationFlow:
        return GlobalIterator(intents_to_topics, flow)


class NeutralIterator(ConversationFlow):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        """
        Global learning style constructor.

        Author: Tomas
        """
        super().__init__(intents_to_topics, flow)

    def accept(self, visitor: Visitor) -> str:
        """
        Accepts the visitor

        Author: Tomas

        Returns
        -------

        Utter associated to the visitor functionality.
        """
        return visitor.visit_neutral(self)
    
    def load(intents_to_topics: Dict[str, str], flow: List[Topic]) -> ConversationFlow:
        return NeutralIterator(intents_to_topics, flow)

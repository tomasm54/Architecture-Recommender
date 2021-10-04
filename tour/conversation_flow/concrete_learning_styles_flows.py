import json
from tour.topic.topics import Topic
from typing import Dict, List
from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.visitor.visitor import Visitor


class Sequential(ConversationFlow):

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



class Global(ConversationFlow):

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



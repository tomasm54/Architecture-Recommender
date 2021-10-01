from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.visitor.visitor import Visitor

class NextTopic(Visitor):
    
    def __init__(self) -> None:
        """
        Constructor

        Author: Adrian
        """
        super().__init__()
    
    def visit_sequential(self, it: ConversationFlow) -> str:
        """
        Get the next utter with a conversation flow iteration that describes a sequential person.
        It enters to the main topic and each one of the subtopics.

        Author: Tomas

        Returns
        -------

        Utter associated to the next explanation for a Sequential person.
        """
        while len(it.get_to_explain()) > 0 and (it.get_to_explain()[-1].is_explained or it.topic_in_flow(it.get_to_explain()[-1])):
            it.get_to_explain()[-1].get_explanation()
            next_to_explain = it.get_to_explain()[-1].next()
            if next_to_explain is None:
                it.pop_not_explained_topic()
            else:
                it.append_topic_to_explain(next_to_explain)

        if len(it.get_to_explain()) == 0:
            return "utter_final"

        return it.get_to_explain()[-1].get_explanation()

    def visit_global(self, it: ConversationFlow) -> str:
        """
        Iterates over the conversation flow not entering in the subtopics of the topic, describing a global person

        Author: Adrian.

        Returns
        -------
            Utter associated to the next topic.
        """
        if it.get_to_explain()[-1].is_explained:
            it.pop_not_explained_topic()
        if len(it.get_to_explain()) == 0:
            return "utter_final"
        return it.get_to_explain()[-1].get_explanation()

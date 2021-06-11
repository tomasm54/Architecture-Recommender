import abc
from typing import Dict, List

from tour.topics import Topic


class Iterator(metaclass=abc.ABCMeta):
    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        all_topics = {}
        for topic in flow:
            all_topics.update(topic.get())
        self._intents_to_topics = {intent: all_topics[topic] for
                                   intent, topic in intents_to_topics.items()}

        self._flow = flow
        self._to_explain = [topic for topic in reversed(flow)]

    def in_tour(self, intent_name: str) -> bool:
        return intent_name in self._intents_to_topics

    @abc.abstractmethod
    def next(self) -> str:
        raise NotImplementedError

    def get(self, intent_name: str) -> str:
        if intent_name not in self._intents_to_topics:
            return "action_topic_not_recognized"

        return self._intents_to_topics[intent_name].get_explanation(
            mark_as_explained=False)

    def repeat(self) -> str:
        return self._to_explain[-1].repeat

    def restart(self):
        self._to_explain = [topic for topic in reversed(self._flow)]
        for topic in self._to_explain:
            topic.restart()
    
    def get_last_topic(self) -> Topic:
        #Returns the next topic to the last topic explained(not subtopic)
        i=1
        while self._to_explain[-i] not in self._flow:
            i+=1
        i+=1
        return self._to_explain[-i]
    
    def jump_to_topic(self,topic:Topic):
        #Jumps to the specified topic
        while self._to_explain[-1] != topic:
            self._to_explain.pop()


class SequentialIterator(Iterator):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        super().__init__(intents_to_topics, flow)

    def next(self) -> str:
        while len(self._to_explain) > 0 and self._to_explain[-1].is_explained:
            next_to_explain = self._to_explain[-1].next()
            if next_to_explain is None:
                self._to_explain.pop()
            else:
                self._to_explain.append(next_to_explain)

        if len(self._to_explain) == 0:
            return "utter_end_tour"

        return self._to_explain[-1].get_explanation()

class GlobalIterator(Iterator):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        super().__init__(intents_to_topics, flow)
    """
    Iterates over the conversation flow not entering in the subtopics of the topic

    Author: Tomas.

    Returns
    -------
        Utter associated to the next topic.
    """
    def next(self) -> str:
        if self._to_explain[-1].is_explained:
            self._to_explain.pop()
        if len(self._to_explain) == 0:
            return "utter_end_tour"

        return self._to_explain[-1].get_explanation()

class NeutralIterator(Iterator):

    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        super().__init__(intents_to_topics, flow)
    """
    Iterates over the conversation flow entering only in the first subtopic of the topic

    Author: Adrian.

    Returns
    -------
        Utter associated to the next topic.
    """
    def next(self) -> str:
        while len(self._to_explain) > 0 and self._to_explain[-1].is_explained:
            if self._to_explain[-1].get_amount_subtopics()< 1:
                next_to_explain = self._to_explain[-1].next()
                if next_to_explain is None:
                    self._to_explain.pop()
                else:
                    self._to_explain.append(next_to_explain)
            else:
                self._to_explain.pop()

        if len(self._to_explain) == 0:
            return "utter_end_tour"

        return self._to_explain[-1].get_explanation()
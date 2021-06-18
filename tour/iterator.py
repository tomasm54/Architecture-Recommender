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
        self._jump = None
        self._current_topic = None

    def in_tour(self, intent_name: str) -> bool:
        return intent_name in self._intents_to_topics

    @abc.abstractmethod
    def next(self) -> str:
        raise NotImplementedError

    def get_current_topic(self)-> str:
        return self._current_topic

    def get(self, topic: str , jump : bool = False, example : bool = None ) -> str:
        if self.is_older_topic(Topic(topic,[])):
            if example is None:
                self._current_topic = topic
                return "utter_cross_examine_example"
        if topic not in self._intents_to_topics:
            return "action_topic_not_recognized"
        if jump:
            self.jump_to_topic(Topic(topic,[]))
        if example is not None and example:
            return self._intents_to_topics[topic].get_example()

        return self._intents_to_topics[topic].get_explanation()

    def set_jump(self, jump : bool):
        self._jump = jump

    def repeat(self) -> str:
        return self._to_explain[-1].repeat

    def is_older_topic(self, topic : Topic)-> bool:
        if topic in self._to_explain:
            return False
        else:
            return True

    def example(self, topic : str = None) -> str:
        if topic is None:
            return self._to_explain[-1].get_example()
        else:
            if topic not in self._intents_to_topics:
                return "action_topic_not_recognized"
            else:
                return  self._intents_to_topics[topic].get_example()
    
    def restart(self):
        self._to_explain = [topic for topic in reversed(self._flow)]
        for topic in self._to_explain:
            topic.restart()
    
    def get_last_topic(self) -> Topic:
        #Returns the next topic to the last topic explained(not subtopic)
        i=1
        while self._to_explain[-i] not in self._flow:
            i+=1
        return self._to_explain[-i]
    
    def jump_to_topic(self,topic:Topic):
        #Jumps to the specified topic
        if topic.get_id() in self._intents_to_topics:
            while  len(self._to_explain)==0 or self._to_explain[-1] != topic:
                if len(self._to_explain)>0:
                    self._to_explain.pop()
                else:
                    self.restart()
            while self._to_explain[-1] not in self._flow:
                self._to_explain.pop()
            self._to_explain[-1].set_explained(True)
        


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
    
    def get(self, topic: str, jump : bool = False , example : bool = None) -> str:
        if self.is_older_topic(Topic(topic,[])):
            if self._jump is None:
                self._current_topic = topic
                return "utter_cross_examine_jump_sequential"
            else:
                return super().get(topic,self._jump,example = example)
        else:
            return super().get(topic,example = example)



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
    
    def get(self, topic: str, jump : bool = False,  example : bool = None) -> str:
        print("llegue")
        if not self.is_older_topic(Topic(topic,[])) and not self._to_explain[-1].get_id() == topic:
            print("entre al if")
            if self._jump is None:
                print("hice todo")
                self._current_topic = topic
                return "utter_cross_examine_jump_global"
            else:
                return super().get(topic,jump =self._jump, example = example)
        else:
            print("llegue afuera del if")
            return super().get(topic, example = example)

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
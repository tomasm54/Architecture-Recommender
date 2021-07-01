import abc
from tour.topics import Topic
from typing import Dict, List

from tour import iterator
from tour.visitor import Visitor

class GetTopic(Visitor):
    
    def __init__(self, topic: str, jump : bool = False, example : bool = False) -> None:
        self._topic = topic
        self._jump = jump
        self._example = example

    def visit_sequential(self, it : iterator.SequentialIterator) -> str:
        if it.is_older_topic(Topic(self._topic,[])):
            if it.get_jump() is None:
                it.set_current_topic(self._topic)
                return "utter_cross_examine_jump_sequential"
            else:
                return self.get_topic(it)
        else:
            return self.get_topic(it)

    
    def visit_global(self, it : iterator.GlobalIterator) -> str:
        if not it.is_older_topic(Topic(self._topic,[])) and not it.get_to_explain[-1].get_id() == self._topic:
            if self._jump is None:
                self._current_topic = self._topic
                return "utter_cross_examine_jump_global"
            else:
                return self.get_topic(it)
        else:
            return self.get_topic(it)

    def visit_neutral(self, it : iterator.NeutralIterator) -> str:
        return self.get_topic(it)

    def get_topic(self,it : iterator.Iterator) -> str:
        if it.is_older_topic(Topic(self._topic,[])):
            if self._example == False:
                it.set_current_topic(self._topic)
                return "utter_cross_examine_example"
        if self._topic not in it.get_intents_to_topic():
            return "action_topic_not_recognized"
        if self._jump:
            it.jump_to_topic(Topic(self._topic,[]))
        return it.get_intents_to_topic()[self._topic].get_explanation()
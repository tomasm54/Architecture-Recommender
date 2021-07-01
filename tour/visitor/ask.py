from tour.topic.topics import Topic
from tour.iterator.iterator import Iterator
from tour.visitor.visitor import Visitor
from random import randint


class Ask(Visitor):

    def __init__(self) -> None:
        super().__init__()

    def visit_sequential(self, it: Iterator) -> str:
        respond = "utter_sin_question"
        while respond == "utter_sin_question":
            it.restart()
            question = randint(0, len(it.get_intents_to_topic()) - 1)
            it.jump_to_topic(Topic(it.get_intents_to_topic()[question].get_id(), []))
            respond = it.get_to_explain()[-1].get_question()
        return respond

    def visit_global(self, it: Iterator) -> str:
        raise NotImplementedError

    def visit_neutral(self, it: Iterator) -> str:
        raise NotImplementedError

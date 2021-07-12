import abc
from typing import Dict, List

from tour.topic.topics import Topic


class ConversationFlow(metaclass=abc.ABCMeta):
    """
    Saves the conversation flow.
    """
    def __init__(self, intents_to_topics: Dict[str, str], flow: List[Topic]):
        """
        Constructor.

        Author: Adrian

        Parameters
        ----------

        intents_to_topics
            Dictionary saved in intents_to_topics.json
        flow
            List of topics saved in flow.json.
        """
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
        """
        Abstract method that gives the next topic in the conversation flow.
        """
        raise NotImplementedError

    def get_current_topic(self) -> str:
        """
        Get the current topic's ID

        Author: Tomas

        Returns
        -------
        Returns the current topic's ID
        """
        return self._current_topic

    def set_current_topic(self, topic: str):
        """
        Set the current topic's ID

        Author: Tomas

        Parameters
        ----------

        topic
            ID of the topic we want to set.
        """
        self._current_topic = topic

    def get_jump(self) -> bool:
        """
        Get the jump decision previously taken

        Author: Tomas

        Returns
        -------

        Boolean value to return the jump decision previously done
        None if the jump decision was not defined.
        """
        return self._jump

    def set_jump(self, jump: bool):
        """
        Sets the jump decision

        Author: Tomas

        Parameters
        ----------

        jump
            Boolean value to set if we want to make the jump or not.
        """
        self._jump = jump

    def repeat(self) -> str:
        """
        Repeats the current topic

        Author: Adrian

        Returns
        -------

        Explanation of the current topic.
        """
        return self._to_explain[-1].repeat

    def get_to_explain(self) -> List:
        """
        Get the topics that has not been explained yet

        Author: Tomas

        Returns
        -------
        Copy of the List with the topics that has not been explained yet
        """
        return self._to_explain.copy()

    def get_intents_to_topic(self) -> Dict:
        """
        Get the intents_to_topic values.

        Author: Tomas

        Returns
        -------
        Copy of the dictionary that has intents_to_topic
        """
        return self._intents_to_topics.copy()

    def is_older_topic(self, topic: Topic) -> bool:
        """
        Checks if the topic given as parameter has already been explained

        Author: Adrian

        Parameters
        ----------

        topic
            Topic to check if it was explained or not.

        Returns
        -------

        Returns a boolean value to check if the topic was explained or not
        """
        if topic in self._to_explain:
            return False
        else:
            return True

    def restart(self):
        """
        Restarts the conversation flow.

        Author: Tomas
        """
        self._to_explain = [topic for topic in reversed(self._flow)]
        for topic in self._to_explain:
            topic.restart()

    def get_last_topic(self) -> Topic:
        """
        Returns the next topic to the last topic explained(not subtopic)

        Author: Tomas

        Returns
        -------
        Topic with the previous topic in conversation flow.
        """
        i = 1
        while self._to_explain[-i] not in self._flow:
            i += 1
        return self._to_explain[-i]

    def jump_to_topic(self, topic: Topic):
        """
        Jumps to the specified topic

        Author: Tomas

        Parameters
        ----------
        topic
            Topic we want to jump
        """
        # Jumps to the specified topic
        if topic.get_id() in self._intents_to_topics:
            while len(self._to_explain) == 0 or self._to_explain[-1] != topic:
                if len(self._to_explain) > 0:
                    self._to_explain.pop()
                else:
                    self.restart()
            while self._to_explain[-1] not in self._flow:
                self._to_explain.pop()
            self._to_explain[-1].set_explained(True)

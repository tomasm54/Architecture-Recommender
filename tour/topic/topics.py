from typing import Dict, Any, List, Optional, Union


def parse_topic(raw_topic: Dict[str, Any]) -> "Topic":
    topic_type = raw_topic["type"]
    if topic_type == "simple":
        return Topic.from_dict(raw_topic)


class Topic:
    """Topic to explain.

    Author: Bruno.
    """

    def __eq__(self, other):
        return self._id == other._id

    @staticmethod
    def from_dict(raw_topic: Dict[str, Any]) -> "Topic":
        if raw_topic.get("examples") is None:
            examples = []
        else:
            examples = raw_topic.get("examples")
        if raw_topic.get("sub_topics") is None:
            subtopics = []
        else:
            subtopics = [parse_topic(raw_topic) for raw_topic in raw_topic["sub_topics"]]
        if raw_topic.get("questions") is None:
            questions = []
        else:
            questions = raw_topic.get("questions")
        return Topic(raw_topic["topic_id"],
                     raw_topic["utters"],
                     examples,
                     subtopics,
                     questions)

    # noinspection PyTypeChecker
    def __init__(
            self,
            topic_id: str,
            utters_explanations: List[str],
            examples: Optional[List[str]] = None,
            sub_topics: Optional[List["Topic"]] = None,
            questions: Optional[List[str]] = None
    ):
        """
        Constructor.

        Author: Bruno.

        Parameters
        ----------
        topic_id
            Identification for the topic.
        utters_explanations
            Possible explanations for the topic.
        examples
            Examples to give for the topic.
        sub_topics
            Sub topics of the topic.
        questions
            Questions to make to the user.
        """
        self._id = topic_id
        self._utters_explanations = utters_explanations
        # Default detail level is the middle one.
        self._detail_level = int(len(utters_explanations) / 2)
        self.is_explained = False

        self._examples = [] if examples is None else examples
        self._current_example = 0

        self._sub_topics = [] if sub_topics is None else sub_topics
        self._current_sub_topic = 0

        self._questions = [] if questions is None else questions
        self._current_question = 0

    def get(self) -> Dict[str, "Topic"]:
        """
        Get the current topic.

        Author: Tomas

        Returns
        -------
        Dictionary with the current topic's information and
        each subtopic within the main topic.
        """
        topics = {self._id: self}
        for topic in self._sub_topics:
            topics.update(topic.get())
        return topics

    def set_current_example(self, example: int):
        """
        Set the current examples' index.

        Author: Tomas

        Parameters
        ----------

        example
            new examples' index
        """
        self._current_example = example

    def get_current_example(self) -> int:
        """
        Get the current examples' index.

        Author: Tomas

        Returns
        -------
        The index of the current example.
        """
        return self._current_example

    def get_explanation(self, mark_as_explained: bool = True) -> str:
        """Explains the topic. Marks the topic as explained.

        Author: Bruno.

        Returns
        -------
        Utter associated to the explanation with current detail level.
        """
        if mark_as_explained:
            self.is_explained = True
        if self._detail_level >= len(self._utters_explanations):
            self._detail_level = 0
        return self._utters_explanations[self._detail_level]
    

    def get_example(self) -> str:
        """
        Get the utter associated to the next example to give.

        Author: Tomas

        Returns
        -------
        Utter associated to the next example if the topic has any example,
        otherwise it returns a default utter.
        """
        if self._current_example < len(self._examples):
            example = self._examples[self._current_example]
            self._current_example += 1
            return example
        else:
            self._current_example = 0
            return "utter_sin_ejemplos"

    def get_question(self) -> str:
        """
        Get the utter associated to the topic's next question.

        Author: Adrian

        Returns
        -------
        Utter associated to the next question if the topic has any,
        otherwise it returns a default utter.
        """
        if self._current_question < len(self._questions):
            question = self._questions[self._current_question]
            self._current_question += 1
            return question
        else:
            self._current_question = 0
            return "utter_sin_question"

    def next(self) -> Union["Topic", None]:
        """Returns the next topic to explain.

        Author: Bruno.

        Returns
        -------
        Next topic to explain.
        """
        if not self.is_explained:
            return self

        if self._current_sub_topic < len(self._sub_topics):
            topic = self._sub_topics[self._current_sub_topic]
            self._current_sub_topic += 1
            return topic

        return None

    def restart(self):
        """Restarts the topic, so it can be explained again.

        Author: Bruno.
        """
        self.is_explained = False
        self._current_example = 0
        self._current_sub_topic = 0
        for topic in self._sub_topics:
            topic.restart()

    def get_id(self) -> str:
        """
        Get the current topic ID

        Author: Adrian

        Returns
        -------
        Topic's name.
        """
        return self._id

    def set_explained(self, explained: bool):
        """
        Set the current topic as explained or not explained.

        Author: Adrian

        Parameters
        ----------

        explained
            Boolean value to set if the current topic is explained or not.
        """
        self.is_explained = explained

    @property
    def repeat(self) -> str:
        """Repeats the explanation for the topic.

        Author: Bruno.

        Returns
        -------
        Utter associated to the explanation with next detail level if possible.
        Otherwise returns the utter for the maximum detail level.
        """
        self._detail_level += 1

        """Se marca como explicado aunque no esta explicado bien"""
        self.is_explained = True
        if self._detail_level >= len(self._utters_explanations):
            return self._utters_explanations[-1]  # -1 = last element.

        return self._utters_explanations[self._detail_level]

    def get_amount_subtopics(self) -> int:
        """
        Get the amount of subtopics of the current topic.

        Author: Tomas

        Returns
        -------
        Returns the amount of subtopics that the current topic has.
        """
        return self._current_sub_topic

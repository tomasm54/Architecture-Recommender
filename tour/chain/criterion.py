import abc
from rasa.shared.core.trackers import DialogueStateTracker


class Criterion(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def check(self, tracker: DialogueStateTracker) -> bool:
        raise NotImplementedError


class EqualIntent(Criterion):
    """
    Checks if the latest intent is equal to another

    Author: Adrian
    """
    def __init__(self, compare: str) -> None:
        """
        Constructor

        Author: Adrian

        Parameters
        ----------

        compare
            String that is going to be compared to the latest intent in the tracker
        """
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the latest intent is equal to the string given in the constructor

        Author: Adrian

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true or false if the latest intent is equal to the str given by parameter or not.
        """
        return self._compare == tracker.latest_message.intent['name']


class EqualAction(Criterion):
    """
    Checks if the latest action is equal to another

    Author: Tomas
    """
    def __init__(self, compare: str) -> None:
        """
        Constructor

        Author: Tomas

        Parameters
        ----------

        compare
            String that is going to be compared to the latest action in the tracker
        """
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the latest action is equal to the string given in the constructor

        Author: Tomas

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true or false if the latest action is equal to the str given by parameter or not.
        """
        return self._compare == tracker.latest_action_name


class EqualEntity(Criterion):
    """
    Checks if the latest entity with "tema" as entity name is equal to a string

    Author: Adrian
    """
    def __init__(self, compare: str) -> None:
        """
        Constructor

        Author: Adrian

        Parameters
        ----------

        compare
            String that is going to be compared to the latest entity with "tema" as entity name in the tracker
        """
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the latest entity with "tema" as name is equal to the string given in the constructor

        Author: Adrian

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true or false if the latest entity with "tema" as name is equal to the str given by parameter or not.
        """
        return self._compare == next(tracker.get_latest_entity_values("tema"), None)


class EqualPenultimateIntent(Criterion):
    """
    Checks if the penultimate event in the tracker is equal to a String

    Author: Tomas
    """
    def __init__(self, compare: str) -> None:
        """
        Constructor.

        Author: Tomas

        Parameters
        ----------

        compare
            String that is going to be compared to the penultimate event in the tracker
        """
        self._compare = compare

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the penultimate event in the tracker is equal to attribute compare set in constructor.

        Author: Tomas

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true if the penultimate event is equal to the string set in constructor, else returns false.
        """
        if len(tracker.as_dialogue().events) > 5:
            penultimate_intent = str(tracker.as_dialogue().events[-4])
        else:
            penultimate_intent = None
        if penultimate_intent is not None and penultimate_intent.find(self._compare) != -1:
            return True
        else:
            return False


class AndCriterion(Criterion):
    """
    Checks if the AND operation between two criterion.

    Author: Adrian
    """
    def __init__(self, criterion1: Criterion, criterion2: Criterion) -> None:
        """
        Constructor.

        Author: Adrian

        Parameters
        ----------

        criterion1
            Any criterion.
        criterion2
            Other criterion do the AND operation between criterion.
        """
        self._criterion1 = criterion1
        self._criterion2 = criterion2

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the AND operation is true or false

        Author: Adrian

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true if the AND operation is true, else is false.
        """
        return self._criterion1.check(tracker) and self._criterion2.check(tracker)


class NotCriterion(Criterion):
    """
    Checks if the NOT operation between two criterion.

    Author: Adrian
    """
    def __init__(self, criterion1: Criterion) -> None:
        """
        Constructor.

        Author: Adrian

        Parameters
        ----------

        criterion1
            Any criterion.
        """
        self._criterion1 = criterion1

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the NOT operation is true or false

        Author: Adrian

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true if the NOT operation is true, else is false.
        """
        return not self._criterion1.check(tracker)


class OrCriterion(Criterion):
    """
    Checks if the OR operation between two criterion.

    Author: Tomas
    """
    def __init__(self, criterion1: Criterion, criterion2: Criterion) -> None:
        """
        Constructor.

        Author: Tomas

        Parameters
        ----------

        criterion1
            Any criterion.
        criterion2
            Other criterion do the OR operation between criterion.
        """
        self._criterion1 = criterion1
        self._criterion2 = criterion2

    def check(self, tracker: DialogueStateTracker) -> bool:
        """
        Checks if the OR operation is true or false

        Author: Tomas

        Parameters
        ----------

        tracker
            Rasa tracker.

        Returns
        -------

        Returns true if the OR operation is true, else is false.
        """
        return self._criterion1.check(tracker) or self._criterion2.check(tracker)

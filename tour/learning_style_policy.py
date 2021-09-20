import json
import logging
from tour.loading_script import create_iterator, functions_builder, load_learning_styles
from tour.chain.node import Node, DefaultNode, NodeActionListen, NodeAsk, NodeExample, NodeGet, NodeNext, NodeRepeat, NodeReset, NodeResponse
from tour.chain.criterion import AndCriterion, EqualAction, EqualEntity, EqualIntent, EqualPenultimateIntent, NotCriterion, OrCriterion

from typing import Optional, Any, Dict, List, Text

from rasa.shared.core.domain import Domain
from rasa.shared.core import events
from rasa.core.featurizers.tracker_featurizers import (
    TrackerFeaturizer,
)
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.core.policies.policy import Policy, PolicyPrediction, confidence_scores_for
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.generator import TrackerWithCachedStates

from tour.iterator.conversation_flow import ConversationFlow
from tour.topic.topics import parse_topic
from tour.iterator.concrete_iterator import GlobalIterator, SequentialIterator, NeutralIterator

logger = logging.getLogger(__name__)

# temporary constants to support back compatibility
MAX_HISTORY_NOT_SET = -1
OLD_DEFAULT_MAX_HISTORY = 5
BESTY_POLICY_PRIORITY = 10
DEFAULT_LEARNING_STYLE = 'neutral'
LEARNING_STYLE_CONFIDENCE = 3


def count_intents_from_stories(s, story_intents):
    # this function counts the amount of intents in a story and update the ocurrences of
    # an intent in a story
    count_intents = 0
    for t in s.events:
        if isinstance(t, events.UserUttered):
            intent = t.as_dict().get('parse_data').get('intent').get('name')
            story_intents[intent] = story_intents[intent] + 1
            count_intents = count_intents + 1
    return count_intents


def move_to_a_location(response):
    locations = {
        "utter_start_tour": "tour_scrum_assistant_p1",
        "utter_product_backlog": "tour_scrum_assistant_p2",
        "utter_sprint_backlog": "tour_scrum_assistant_p2",
        "utter_scrum_master": "tour_scrum_assistant_p3",
        "utter_scrum_board": "tour_scrum_assistant_p4",
        "utter_development_team": "tour_scrum_assistant_p5",
        "utter_daily_meeting": "tour_scrum_assistant_p6",
        "utter_sprint_review": "tour_scrum_assistant_p6"
    }
    # if locations.get(response) is not None:
    #     publisher.publish("movement",
    #                       {"location": locations.get(response),
    #                        "to": "Cristina"})

class LearningStylePolicy(Policy):
    last_action_timestamp = 0
    answered = False
    _it = ConversationFlow
    learning_style_iterators = load_learning_styles()

    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = BESTY_POLICY_PRIORITY,
            usertype: Optional[dict] = None,
            story_profiles: Optional[dict] = None,
            learning_style: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        super().__init__(featurizer, priority, **kwargs)
        self.story_profiles = story_profiles if story_profiles is not None else {}
        self.usertype = usertype if usertype is not None else {}
        self.learning_style = learning_style if learning_style is not None else DEFAULT_LEARNING_STYLE
        create_iterator(self.learning_style_iterators)
        self._it = self.learning_style_iterators["neutral"]
        self._criterion_learning = AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")),
                                                EqualAction("action_listen"))
        # to do script
        self._functions = functions_builder()

    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any,
    ) -> None:
        # only original stories
        training_trackers = [
            t
            for t in training_trackers
            if not hasattr(t, "is_augmented") or not t.is_augmented
        ]
        stories = {}
        amount_intents = {}
        for s in training_trackers:
            story_name = s.as_dialogue().as_dict().get('name')
            # initialize dict with intents as keys and 0 counts in each history
            if story_name not in stories.keys():
                # if the story does not exist, is added to the dictionary and the ocurrences of intents are updated
                story_intents = dict.fromkeys(domain.intents, 0)
                count_intents = count_intents_from_stories(s, story_intents)
                stories.update({story_name: story_intents})
                amount_intents.update({story_name: count_intents})
                self.usertype.update({story_name: 0.0})
            else:
                # if the story already exists, is updated in the dictionary and the ocurrences of intents are added
                aux_intents = stories.get(story_name)
                count_intents = amount_intents.get(story_name) + count_intents_from_stories(s, aux_intents)
                amount_intents.update({story_name: count_intents})
                stories.update({story_name: aux_intents})

        # here the training calculates the probability of ocurrence of each intent for each learning style
        for story_name in stories:
            for intent in stories.get(story_name):
                stories.get(story_name).update({
                    intent: stories.get(story_name).get(intent) / amount_intents.get(story_name)
                })
        print(self.usertype)
        print(stories)
        print(amount_intents)
        self.story_profiles.update(stories)
        print(self.story_profiles)
        """Trains the policy on given training trackers.

        Args:
            training_trackers:
                the list of the :class:`rasa.core.trackers.DialogueStateTracker`
            domain: the :class:`rasa.shared.core.domain.Domain`
            interpreter: Interpreter which can be used by the polices for featurization.
        """
        pass

    def predict_action_probabilities(
            self,
            tracker: DialogueStateTracker,
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any,
    ) -> PolicyPrediction:
        intent = tracker.latest_message.intent
        if self._criterion_learning.check(tracker):
            for s in self.usertype:
                self.usertype.update({s: self.usertype.get(s) + self.story_profiles.get(s).get(intent["name"])})
            aux_ls = 0.0
            new_ls = ''
            for s in self.usertype:
                if aux_ls < self.usertype.get(s) and self.usertype.get(s) > LEARNING_STYLE_CONFIDENCE:
                    aux_ls = self.usertype.get(s)
                    new_ls = s
            print(self.usertype)
            if new_ls != self.learning_style and new_ls != '':
                self.learning_style = new_ls
                self.learning_style_iterators[new_ls].jump_to_topic(self._it.get_last_topic())
                self._it = self.learning_style_iterators[new_ls]

        return self._prediction(confidence_scores_for(self._functions.next(self._it, tracker), 1.0, domain))

        # return self._prediction(confidence_scores_for("action_listen", 1.0, domain))

    def _metadata(self) -> Dict[Text, Any]:
        return {
            "priority": self.priority,
            "story_profiles": self.story_profiles,
            "usertype": self.usertype
        }

    @classmethod
    def _metadata_filename(cls) -> Text:
        return "test_policy.json"

import json
import logging
from tour.arch_designer import architecture_finder
from tour.loading_script import functions_builder
from tour.chain.node import Node, DefaultNode, NodeActionListen,  NodeNext, NodeRepeat
from tour.chain.criterion import AndCriterion, EqualAction, EqualEntity, EqualIntent, EqualPenultimateIntent, \
    NotCriterion, OrCriterion

from typing import Optional, Any, Dict, List, Sequence, Text

from rasa.shared.core.domain import Domain
from rasa.shared.core import events
from rasa.core.featurizers.tracker_featurizers import (
    TrackerFeaturizer,
)
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.core.policies.policy import Policy, PolicyPrediction, confidence_scores_for
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.generator import TrackerWithCachedStates

from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.topic.topics import parse_topic
from tour.conversation_flow.concrete_learning_styles_flows import Global, Sequential

logger = logging.getLogger(__name__)

# temporary constants to support back compatibility
MAX_HISTORY_NOT_SET = -1
OLD_DEFAULT_MAX_HISTORY = 5
BESTY_POLICY_PRIORITY = 10
#DEFAULT_LEARNING_STYLE = 'neutral'
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
    #_it = ConversationFlow
    #learning_style_flows = load_learning_styles()

    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = BESTY_POLICY_PRIORITY,
            #usertype: Optional[dict] = None,
            #story_profiles: Optional[dict] = None,
            #learning_style: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        super().__init__(featurizer, priority, **kwargs)
        # to do script
        self._functions = functions_builder()
        self._users  = {}

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

        pass

    def predict_action_probabilities(
            self,
            tracker: DialogueStateTracker,
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any,
    ) -> PolicyPrediction:
        id = tracker.current_state()['sender_id']
        if id not in self._users:
            #var = tracker.current_state()["latest_message"]
            #metadata = var["metadata"]
            #personality = metadata["personality"]
            #if personality == "global":
                self._users[id] = Global({},[])
            #else:
            #    self._users[id] = Sequential({},[])

        return self._prediction(confidence_scores_for(self._functions.next(self._users[id], tracker), 1.0, domain))

    def _metadata(self) -> Dict[Text, Any]:
        return {
            "priority": self.priority,
            #"story_profiles": self.story_profiles,
            #"usertype": self.usertype
        }

    @classmethod
    def _metadata_filename(cls) -> Text:
        return "test_policy.json"

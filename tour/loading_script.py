import json
from tour.conversation_flow.concrete_learning_styles_flows import Global, Sequential, Neutral
from tour.topic.topics import parse_topic
from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.chain.node import Node, DefaultNode, NodeActionListen, NodeAsk, NodeExample, NodeGet, NodeNext, NodeRepeat, \
    NodeReset, NodeResponse
from tour.chain.criterion import AndCriterion, EqualAction, EqualEntity, EqualIntent, EqualPenultimateIntent, \
    NotCriterion, OrCriterion

PATH_FLOW = r"info/flow.json"
PATH_INTENTS_TO_TOPICS = r"info/intents_to_topics.json"


def functions_builder() -> Node:
    node1 = DefaultNode(None)
    node1 = NodeActionListen(node1, AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")),
                                                 NotCriterion(EqualAction("action_listen"))))
    node1 = NodeNext(node1, AndCriterion(
        AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")), EqualAction("action_listen")),
        EqualIntent("affirm")))
    node1 = NodeGet(node1, AndCriterion(
        AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")), EqualAction("action_listen")),
        AndCriterion(EqualIntent("explicame_tema"), NotCriterion(EqualEntity(None)))))
    node1 = NodeGet(node1, AndCriterion(
        AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")), EqualAction("action_listen")),
        AndCriterion(EqualIntent("no_entiendo"), NotCriterion(EqualEntity(None)))))
    node1 = NodeRepeat(node1, OrCriterion(EqualAction("utter_ask_bad"), AndCriterion(
        AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")), EqualAction("action_listen")),
        OrCriterion(AndCriterion(EqualIntent("no_entiendo"), EqualEntity(None)), EqualIntent("deny")))))
    node1 = NodeExample(node1, AndCriterion(
        AndCriterion(NotCriterion(EqualPenultimateIntent("utter_cross_examine")), EqualAction("action_listen")),
        EqualIntent("dame_ejemplo")))
    node1 = NodeGet(node1, AndCriterion(
        AndCriterion(EqualPenultimateIntent("utter_cross_examine"),
                     EqualPenultimateIntent("utter_cross_examine_example")),
        EqualIntent("dame_ejemplo")), example=True)
    node1 = NodeGet(node1, AndCriterion(
        AndCriterion(EqualPenultimateIntent("utter_cross_examine"),
                     EqualPenultimateIntent("utter_cross_examine_example")),
        NotCriterion(EqualIntent("dame_ejemplo"))), example=False)
    node1 = NodeGet(node1, AndCriterion(
        AndCriterion(EqualPenultimateIntent("utter_cross_examine"), EqualPenultimateIntent("utter_cross_examine_jump")),
        EqualIntent("change_current_flow")), jump=True)
    node1 = NodeGet(node1, AndCriterion(
        AndCriterion(EqualPenultimateIntent("utter_cross_examine"), EqualPenultimateIntent("utter_cross_examine_jump")),
        NotCriterion(EqualIntent("change_current_flow"))), jump=False)
    node1 = NodeAsk(node1, OrCriterion(EqualAction("utter_ask"), EqualAction("utter_ask_good")))
    node1 = NodeResponse(node1, EqualPenultimateIntent("utter_cross_examine_tema"))
    return node1


def load_learning_styles() -> dict:
    return {"sequential": Sequential, "global": Global, "neutral": Neutral}


def create_learning_style_flows(learning: dict):
    with open(PATH_FLOW) as file:
        flow = [parse_topic(raw_topic) for raw_topic in json.load(file)]
    with open(PATH_INTENTS_TO_TOPICS) as file:
        intents_to_topics = json.load(file)
    print(intents_to_topics)
    print(flow)
    for i in learning:
        learning[i] = learning[i].load(intents_to_topics=intents_to_topics, flow=flow)

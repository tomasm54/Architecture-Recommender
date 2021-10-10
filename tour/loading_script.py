
from tour.conversation_flow.concrete_learning_styles_flows import Global, Sequential, Neutral
from tour.conversation_flow.conversation_flow import ConversationFlow
from tour.chain.node import Node, DefaultNode, NodeActionListen, NodeExample, NodeExplain, NodeExplainArchitecture, NodeGivesRequirement, NodeNext, NodeRepeat, NodeRequirement
from tour.chain.criterion import AndCriterion, EmptyFlow, EqualAction, EqualEntity, EqualIntent, EqualMessage, EqualPenultimateIntent, \
    NotCriterion, OrCriterion

PATH_FLOW = r"info/flow.json"
PATH_INTENTS_TO_TOPICS = r"info/intents_to_topics.json"

FLOWS_PATHS = {"scrum" : r"info/scrum.json", 
                "layers" : r"info/layers.json"}

def functions_builder() -> Node:
    node1 = DefaultNode(None)
    node1 = NodeActionListen(node1,NotCriterion(EqualAction("action_listen")))
    node1 = NodeRequirement(node1, AndCriterion(EqualAction("action_listen"),EmptyFlow()),FLOWS_PATHS)
    node1 = NodeNext(node1, 
        AndCriterion(NotCriterion(EmptyFlow()),AndCriterion(
        AndCriterion(NotCriterion(EqualPenultimateIntent("utter_final")), EqualAction("action_listen")),
        EqualIntent("affirm"))))
    node1 = NodeExplain(node1, AndCriterion(EqualAction("action_listen"),
    OrCriterion(AndCriterion(EqualIntent("explicame_tema"),NotCriterion(EqualEntity(None))), 
    AndCriterion(EqualIntent("no_entiendo"), NotCriterion(EqualEntity(None))))),FLOWS_PATHS)
    node1 = NodeGivesRequirement(node1, OrCriterion(EqualAction("utter_final"),AndCriterion(EqualAction("action_listen"),EqualIntent("dar_requerimientos"))))
    node1 = NodeRepeat(node1, AndCriterion(NotCriterion(EmptyFlow()),AndCriterion(EqualAction("action_listen"),
        OrCriterion(AndCriterion(EqualIntent("no_entiendo"), EqualEntity(None)), EqualIntent("deny")))))
    node1 = NodeExplainArchitecture(node1, AndCriterion(EqualMessage("A R Q U I T E C T U R A"),EqualAction("action_listen")), FLOWS_PATHS)
    return node1




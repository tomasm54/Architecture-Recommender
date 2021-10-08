from typing import Tuple, Dict, List

import es_core_news_lg
import json
import sys
import os

sys.path.append(os.getcwd())

ENTITY_START = "["
ENTITY_END = "]"
MESSAGE_START = "{"
MESSAGE_END = "}"
NUMERATOR_START = "("
NUMERATOR_END = ")"

with open(r"architectures_data/requirements_architectures.json") as reqs_arch:
    data = json.load(reqs_arch)

doclg = es_core_news_lg.load()


def parse_end_of_tagged(token, parsed_phrase: List, end_of_tagged: str):
    token_before_end = False
    splatted_end_ref = token.text.split(end_of_tagged)  # ["",234]
    splatted_end_ref.append(end_of_tagged)  # ["",234,}] or ["",234,]]
    parsed_phrase.extend([splatted_end_ref[1], splatted_end_ref[2], " "])  # add reference number, end symbol and space
    if splatted_end_ref[0] != "":  # bad tagged, space before ] example [hi ]234
        token_before_end = True
    return token_before_end, splatted_end_ref[1]


def parse_phrase_structure(phrase_to_parse: str) -> Tuple[str, Dict, Dict]:
    parsed_phrase = []
    appendable = True
    tag_words_qty = 0
    tagged_entity = {}
    tagged_message = {}
    for token in doclg(phrase_to_parse):
        if appendable:  # out of [], {} or ()
            if token.text in [ENTITY_START, MESSAGE_START]:
                parsed_phrase.append(token.text)  # add [ or {
                appendable = False  # word between [] or {} are not considered
            else:
                parsed_phrase.extend([token.pos_, token.dep_, " "])  # add necessary word info. examples DETdet
                # NOUNnsubj ADPcase
        else:
            """
            spacy tokenize "hi [helicopter]/}1" -> hi, [, helicopter]/}1
            """
            if ENTITY_END in token.text or MESSAGE_END in token.text:
                if MESSAGE_END in token.text:
                    token_before_end, reference_num = parse_end_of_tagged(token, parsed_phrase, "}")
                    if token_before_end:  # bad tagged if space before ] example [hi ]234
                        tag_words_qty += 1
                    tagged_message[reference_num] = tag_words_qty
                else:
                    token_before_end, reference_num = parse_end_of_tagged(token, parsed_phrase, "]")
                    if token_before_end:  # bad tagged if space before ] example [hi ]234
                        tag_words_qty += 1
                    tagged_entity[reference_num] = tag_words_qty
                tag_words_qty = 0
                appendable = True  # do next token appendable
            else:  # common word, only count
                tag_words_qty += 1

    return ''.join(parsed_phrase[:-1]), tagged_message, tagged_entity


for index in data.keys():  # for each arq
    parsed_phrases = []
    requirement_tagged_entity = {}
    requirement_tagged_message = {}
    for req in data[index]["requirements"]["own"]:  # take own reqs (written)
        parsed_req, tagged_req_entities, tagged_req_messages = parse_phrase_structure(req)
        # "hello [word]4" -> "VERBverb[4]",{"4":"1"}
        parsed_phrases.append(parsed_req)
        requirement_tagged_entity.update(tagged_req_entities)
        requirement_tagged_message.update(tagged_req_messages)
    data[index]["requirements"]["own"] = parsed_phrases
    data[index]["requirements"]["tagged_entity"] = requirement_tagged_entity
    data[index]["requirements"]["tagged_message"] = requirement_tagged_message

with open(r'architectures_data/compiled_requirements.json', 'w') as outfile:
    json.dump(data, outfile)

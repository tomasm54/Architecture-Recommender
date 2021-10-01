import es_core_news_lg
import json
import sys
import os

sys.path.append(os.getcwd())

doclg = es_core_news_lg.load()

with open("requirements_architectures.json") as reqs_arch:
    data = json.load(reqs_arch)


def parse_phrase_structure(phrase: str) -> str:
    phrase_sintax = []
    for token in doclg(phrase):
        phrase_sintax.append(token.pos_)
        phrase_sintax.append(token.dep_)
    return ''.join(phrase_sintax)


parsed_phrases = {}

for index in data.keys():
    for phrase in data[index]["requirements"]["own"]:
        parsed_phrase = doclg(phrase)
        parsed_phrases[phrase] = parse_phrase_structure(phrase)

with open('compiled_requirements.json', 'w') as outfile:
    json.dump(parsed_phrases, outfile)



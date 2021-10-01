import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import es_core_news_lg

doclg = es_core_news_lg.load()

requirements_path = r"architectures_data/compiled_requirements.json"
architectures_path = r"architectures_data/requirements_architectures.json"

with open(architectures_path) as architectures_file:
    architectures_data = json.load(architectures_file)

with open(requirements_path) as requirements_file:
    requirements_data = json.load(requirements_file)

user_requirements = []


def compare_str_sintax(str1: str, str2: str) -> bool:
    """
    Compare if two strings are equals sintactically

    FIRST VERSION: two strings are considered equal if they have same:
    - word qty and order and each has same "es_core_news_lg" spacy model pos_ and dep_

    :param str1: string 1 to compare
    :param str2: string 2 to compare
    :return: True if they are equals, False otherwise
    """
    tag1 = doclg(str1)
    tag2 = doclg(str2)
    tag1_sintax = []
    tag2_sintax = []
    for token in tag1:
        tag1_sintax.append(token.pos_)
        tag1_sintax.append(token.dep_)
    for token in tag2:
        tag2_sintax.append(token.pos_)
        tag2_sintax.append(token.dep_)
    return "".join(tag1_sintax) == "".join(tag2_sintax)


# load string requirements
def load_requirements(values: dict) -> list:
    requirements = []
    if "others" in values["requirements"]:
        for other_req in values["requirements"]["others"]:
            requirements.extend(load_requirements(architectures_data[other_req]))
    requirements.extend(values["requirements"]["own"])  # MINIMUM ONE AT THE MOMENT
    return requirements

class ArchitectureDesigner():

    def run(message : str) -> str:
        user_requirements.append(message)  # add last requirement to requirements list
        # for each "case" (requirements set - architecture) check if the reqs have same sintax
        same_sintax_reqs = 0
        for arch in architectures_data.values():
            arch_reqs = load_requirements(arch)
            for requirement in user_requirements:
                for arch_req in arch_reqs:
                    if compare_str_sintax(requirement, arch_req):
                        same_sintax_reqs += 1
            if same_sintax_reqs == len(arch_reqs):
                return arch["architecture"]["type"]
            same_sintax_reqs = 0

        return None


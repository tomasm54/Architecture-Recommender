import json
from typing import Optional, List, Tuple
from architecture import architecture as arch
import es_core_news_lg

doclg = es_core_news_lg.load()

requirements_path = r"architectures_data/compiled_requirements.json"
architectures_path = r"architectures_data/requirements_architectures.json"

with open(architectures_path) as architectures_file:
    architectures_data = json.load(architectures_file)

with open(requirements_path) as requirements_file:
    requirements_data = json.load(requirements_file)

ENTITY_START = "["
ENTITY_END = "]"
MESSAGE_START = "{"
MESSAGE_END = "}"
NUMERATOR_START = "("
NUMERATOR_END = ")"

def compare_req_sintax(arch_req: str, user_req: str) -> bool:
    """
    Compare if two strings are equals syntactically

    FIRST VERSION: two strings are considered equal if they have same:
    - word qty and order and each has same "es_core_news_lg" spacy model pos_ and dep_

    :param arch_req: structure
    :param user_req: string 2 to compare
    :return: True if they are equals, False otherwise
    """
    user_req_tagged = doclg(user_req)
    arch_req_tagged = doclg(arch_req)
    tag1_sintax = []
    tag2_sintax = []
    for token in arch_req_tagged:
        tag1_sintax.append(token.pos_)
        tag1_sintax.append(token.dep_)
    for token in user_req_tagged:
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


class architecture_designer:

    def __init__(self, initial_requirements: Optional[List]):
        self.user_requirements = initial_requirements if initial_requirements else []
        self.architectures = []
        self.simple_architectures = [x for x in architectures_data.values() if
                                     (not x["architecture"]["others"] or len(x["architecture"]["others"]) == 0)]
        self.architecture = arch()

    def add_requirement(self, requirement: str):
        self.user_requirements.append(requirement)

    def clear_architecture(self):
        """
        resets all fields related to architecture
        """
        self.user_requirements.clear()

    def find_architecture(self) -> Tuple[str, str]:
        found_architectures = self.find_simple_architectures()

    def find_simple_architectures(self) ->:
        """
        Returns all recognized simple architecture, when a simple architecture is a one that not have subarchitecture
        """
        same_sintax_reqs = 0
        for simple_arch in self.simple_architectures:
            simple_arch_reqs = simple_arch["requirements"]["own"]  # load string requirements
            for user_requirement in self.user_requirements:  # for each user requirement
                for arch_req in simple_arch_reqs:  # for each requirement of the architecture
                    # check if user requirement match with any arch requirement
                    if compare_req_sintax(user_requirement, arch_req):
                        same_sintax_reqs += 1
            if same_sintax_reqs == len(arch_reqs) and (arch_id not in recognized_architectures):
                recognized_architectures.append(arch_id)
                return arch["architecture"]["type"]
            same_sintax_reqs = 0

    def parse_requirement(self, requirement: str) -> dict:



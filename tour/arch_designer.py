import json
from typing import Optional, List, Tuple
from architecture import architecture as arch
import es_core_news_lg

doclg = es_core_news_lg.load()

architectures_path = r"architectures_data/compiled_architectures.json"

with open(architectures_path) as architectures_file:
    architectures_data = json.load(architectures_file)

ENTITY_START = "["
ENTITY_END = "]"
MESSAGE_START = "{"
MESSAGE_END = "}"


def check_is_tagged(token) -> Tuple[bool, str]:
    for symbol in [MESSAGE_START, MESSAGE_END, ENTITY_START, ENTITY_END]:
        if symbol in token:
            return True, symbol


def compare_req_sintax(arch_req: dict, user_req: str) -> bool:
    """
    Compare if two requirements are equals syntactically
    exact match is considered for no tagged tokens, if they have same:
    same "es_core_news_lg" spacy model pos_ and dep_
    for tagged tokens, only equal if tokens between index of no tagged are less
    or equal to quantity of tokens of original requirement

    :param arch_req: compiled requirement of an architecture
    :param user_req: user requirement
    :return: True if they are considered equals, False otherwise
    """
    user_req_tagged = doclg(user_req)
    splatted_arch_req = arch_req["text"].split(" ")
    subsequences = []
    actual_sub = []
    for idx, token in enumerate(splatted_arch_req):
        is_tagged, symbol = check_is_tagged(token)
        if is_tagged:
            actual_sub[0] =
        else:
            for user_token in user_req_tagged[idx_start_subsequence:]:
                if not user_token.pos_+user_token.dep_ == token:






    return True


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
                                     "others" not in x["requirements"] or
                                     len(x["requirements"]["others"]) == 0]
        self.architecture = arch()

    def add_requirement(self, requirement: str):
        self.user_requirements.append(requirement)

    def clear_architecture(self):
        """
        resets all fields related to architecture
        """
        self.user_requirements.clear()
        self.architecture = arch()

    def find_architecture(self):
        self.find_simple_architectures()

    def find_simple_architectures(self):
        """
        Returns all recognized simple architecture, when a simple architecture is a one that not have subarchitecture
        """
        for simple_arch in self.simple_architectures:
            req_coincidence = False
            same_sintax_reqs = 0
            partial_reqs = []
            simple_arch_reqs = simple_arch["requirements"]["own"]  # load string requirements
            for arch_req in simple_arch_reqs:  # for each requirement of the architecture
                req_idx = 0
                while not req_coincidence and req_idx in self.user_requirements:  # user requirement until match or end
                    user_requirement = self.user_requirements[req_idx]
                    # check if user requirement match with arch requirement
                    if compare_req_sintax(user_requirement, arch_req):
                        same_sintax_reqs += 1
                        # remove the req to avoid comparision with next reqs
                        partial_reqs.append(self.user_requirements.pop(req_idx))
                    req_coincidence = True
                    req_idx += 1
            if same_sintax_reqs == len(simple_arch_reqs):
                print(simple_arch["architecture"]["type"])
                print(partial_reqs)
                exit(1)


des = architecture_designer(["Los datos del cerebro son procesados por la unidad de procesamiento de senales",
                             "Los datos procesados se envian a action management para determinar que accion "
                             "ejecutar en el habitante"])
des.add_requirement("La respuesta es convertida a senales electricas y enviadas al cerebro")
des.find_architecture()

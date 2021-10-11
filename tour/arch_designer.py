import itertools
import json
from typing import Optional, List
import requests

NLU_URL = "http://localhost:5001/model/parse"


class architecture:
    def __init__(self, name: str, requirements: List[str]):
        self.name = name
        self.requirements = requirements

    def get_name(self):
        return self.name

    def get_requirements(self):
        return self.requirements


class architecture_finder:
    def __init__(self, requirements=None):
        self.found_architectures = {}
        self.user_requirements = requirements if requirements else []

    def add_requirement(self, requirement: str):
        self.user_requirements.append(requirement)

    def find_architecture(self) -> Optional[str]:
        found_arch_name = ""
        found_arch_reqs = []
        arch_confidence = 0
        if len(self.user_requirements) > 2:
            for r in range(3, len(self.user_requirements) + 1):
                for reqs_combination in list(itertools.combinations(self.user_requirements, r)):
                    text = ""
                    for req in reqs_combination:
                        text += req + ", "
                    response = requests.post(NLU_URL, data=json.dumps({"text": text})).json()
                    if response["intent"]["confidence"] > arch_confidence or \
                            (response["intent"]["confidence"] == arch_confidence and
                             len(found_arch_reqs) < len(reqs_combination)):
                        found_arch_name = response["intent"]["name"]
                        found_arch_reqs = reqs_combination
                        arch_confidence = response["intent"]["confidence"]

        else:
            return None
        self.found_architectures[len(self.found_architectures.keys()) + 1] = {"name": found_arch_name,
                                                                              "requirements": list(found_arch_reqs)}
        for req in found_arch_reqs:
            self.user_requirements.remove(req)
        return found_arch_name

    def clear_requirements(self):
        self.user_requirements.clear()
        self.found_architectures.clear()

    def get_last_architecture(self) -> Optional[str]:
        return self.found_architectures[len(self.found_architectures.keys())]["name"] if len(self.found_architectures.keys()) > 0 else None


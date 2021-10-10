import itertools
import json
from typing import Optional, List
import requests

NLU_URL = "http://localhost:5001/model/parse"


class architecture_finder:
    def __init__(self, requirements: Optional[List]):
        self.user_requirements = requirements if requirements else []

    def add_requirement(self, requirement: str):
        self.user_requirements.append(requirement)

    def find_architecture(self) -> str:
        arch = ""
        reqs = []
        arch_confidence = 0
        text = ""
        for r in range(2, len(self.user_requirements) + 1):
            for reqs_combination in list(itertools.combinations(self.user_requirements, r)):
                for req in reqs_combination:
                    text += req+", "
                response = requests.post(NLU_URL, data=json.dumps({"text": text})).json()
                if response["intent"]["confidence"] > arch_confidence or \
                    (response["intent"]["confidence"] == arch_confidence and len(reqs) < len(reqs_combination)):
                    arch = response["intent"]["name"]
                    reqs = reqs_combination
                    req_confidence = response["intent"]["confidence"]
                text = ""
        return arch

    def clear_requirements(self):
        self.user_requirements.clear()
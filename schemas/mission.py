from typing import List
from typing_extensions import TypedDict


class MissionStatement(TypedDict):
    mission: str
    real_decision: str
    key_tension: str
    success_criteria: List[str]

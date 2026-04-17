from typing import List
from typing_extensions import TypedDict


class FeasibilityAssessment(TypedDict):
    option_id: str
    complexity_score: int  # 1-10
    resources_needed: List[str]
    bottlenecks: List[str]
    estimated_time: str
    verdict: str  # "viable" | "viable_con_condiciones" | "no_viable"
    notes: str

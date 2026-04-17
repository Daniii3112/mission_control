from typing import List
from typing_extensions import TypedDict


class FinalDecision(TypedDict):
    recommended_option_id: str
    recommended_option_name: str
    synthesis: str
    rationale: List[str]
    what_not_to_ignore: List[str]
    next_moves: List[str]
    confidence: str  # "alta" | "media" | "baja"

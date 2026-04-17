from typing import Dict, List
from typing_extensions import TypedDict


class CriticalReview(TypedDict):
    weak_assumptions: List[str]
    hidden_risks: List[str]
    uncomfortable_questions: List[str]
    per_option_verdict: Dict[str, str]
    overall_verdict: str  # "solido" | "fragil" | "enganosamente_atractivo"
    summary: str

from typing import List
from typing_extensions import TypedDict


class BrandEvaluation(TypedDict):
    option_id: str
    brand_fit_score: int  # 1-10
    strengths: List[str]
    risks: List[str]
    verdict: str  # "potencia_marca" | "neutro" | "diluye_marca"
    recommendation: str

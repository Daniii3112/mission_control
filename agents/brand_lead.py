import json
from typing import List

from agents.base_agent import BaseAgent
from core.llm_client import BaseLLMClient
from schemas import BrandEvaluation, ProductOption
from utils.json_parser import extract_json


class BrandLeadAgent(BaseAgent):

    def __init__(self, llm: BaseLLMClient):
        super().__init__("Brand Lead", "brand_lead.txt", llm)

    def evaluate_options(self, options: List[ProductOption]) -> List[BrandEvaluation]:
        """Evaluate brand fit for each product option (score 1-10 + verdict)."""
        user_prompt = f"""Opciones de producto propuestas por el Product Lead:
{json.dumps(options, ensure_ascii=False, indent=2)}

Evalúa el encaje de cada opción con la identidad y valores de la marca Pymmys.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "evaluations": [
    {{
      "option_id": "option_X",
      "brand_fit_score": 8,
      "strengths": ["fortaleza de marca 1", "fortaleza de marca 2"],
      "risks": ["riesgo de marca 1", "riesgo de marca 2"],
      "verdict": "potencia_marca",
      "recommendation": "qué hacer con esta opción desde el punto de vista de marca"
    }}
  ]
}}
Los valores posibles para verdict son: "potencia_marca", "neutro", "diluye_marca"."""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "evaluations" in data:
            return data["evaluations"]
        raise ValueError(
            f"BrandLeadAgent.evaluate_options — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

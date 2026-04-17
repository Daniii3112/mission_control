import json
from typing import List

from agents.base_agent import BaseAgent
from core.llm_client import BaseLLMClient
from schemas import MarketingAngle, ProductOption
from utils.json_parser import extract_json


class MarketingLeadAgent(BaseAgent):

    def __init__(self, llm: BaseLLMClient):
        super().__init__("Marketing Lead", "marketing_lead.txt", llm)

    def create_launch_angles(self, options: List[ProductOption]) -> List[MarketingAngle]:
        """Create a marketing hook and launch concept for each product option."""
        user_prompt = f"""Opciones de producto a trabajar:
{json.dumps(options, ensure_ascii=False, indent=2)}

Crea un ángulo de lanzamiento y hook de comunicación para cada opción.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "angles": [
    {{
      "option_id": "option_X",
      "hook": "frase gancho en 1 línea que engancha al instante",
      "main_message": "mensaje principal de la campaña en 1-2 frases",
      "target_channels": ["canal 1", "canal 2", "canal 3"],
      "campaign_concept": "concepto de campaña de lanzamiento en 2-3 frases",
      "communication_risk": "principal riesgo de comunicación a vigilar"
    }}
  ]
}}"""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "angles" in data:
            return data["angles"]
        raise ValueError(
            f"MarketingLeadAgent.create_launch_angles — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

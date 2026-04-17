import json
from typing import List

from agents.base_agent import BaseAgent
from core.llm_client import BaseLLMClient
from schemas import MissionStatement, ProductOption
from utils.json_parser import extract_json


class ProductLeadAgent(BaseAgent):

    def __init__(self, llm: BaseLLMClient):
        super().__init__("Product Lead", "product_lead.txt", llm)

    def propose_options(self, mission: MissionStatement) -> List[ProductOption]:
        """Propose 3 concrete, differentiated product options based on the mission."""
        user_prompt = f"""Misión recibida del Director:
{json.dumps(mission, ensure_ascii=False, indent=2)}

Propón exactamente 3 opciones de producto concretas, diferenciadas y realistas para Pymmys.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "options": [
    {{
      "id": "option_1",
      "name": "nombre del producto",
      "description": "descripción concisa en 1-2 frases",
      "target_audience": "audiencia objetivo específica",
      "price_range": "rango de precio estimado en euros",
      "time_to_market": "tiempo estimado para lanzar",
      "key_differentiator": "qué lo hace único o memorable"
    }}
  ]
}}"""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "options" in data:
            return data["options"]
        raise ValueError(
            f"ProductLeadAgent.propose_options — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

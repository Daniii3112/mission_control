import json
from typing import List

from agents.base_agent import BaseAgent
from core.llm_client import BaseLLMClient
from schemas import FeasibilityAssessment, ProductOption
from utils.json_parser import extract_json


class OperationsLeadAgent(BaseAgent):

    def __init__(self, llm: BaseLLMClient):
        super().__init__("Operations Lead", "operations_lead.txt", llm)

    def assess_feasibility(self, options: List[ProductOption]) -> List[FeasibilityAssessment]:
        """Assess operational complexity and feasibility for each product option."""
        user_prompt = f"""Opciones de producto a evaluar operativamente:
{json.dumps(options, ensure_ascii=False, indent=2)}

Evalúa la viabilidad operativa real de cada opción.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "assessments": [
    {{
      "option_id": "option_X",
      "complexity_score": 6,
      "resources_needed": ["recurso o perfil 1", "recurso o perfil 2"],
      "bottlenecks": ["cuello de botella principal", "dependencia crítica"],
      "estimated_time": "X semanas",
      "verdict": "viable",
      "notes": "nota operativa importante sobre esta opción"
    }}
  ]
}}
Los valores posibles para verdict son: "viable", "viable_con_condiciones", "no_viable"."""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "assessments" in data:
            return data["assessments"]
        raise ValueError(
            f"OperationsLeadAgent.assess_feasibility — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

import json
from typing import Any, Dict

from agents.base_agent import BaseAgent
from core.llm_client import BaseLLMClient
from schemas import CriticalReview
from utils.json_parser import extract_json


class CriticalReviewerAgent(BaseAgent):

    def __init__(self, llm: BaseLLMClient):
        super().__init__("Critical Reviewer", "critical_reviewer.txt", llm)

    def attack_plan(self, all_outputs: Dict[str, Any]) -> CriticalReview:
        """Attack weak assumptions and surface hidden risks across all agent outputs."""
        context = json.dumps(all_outputs, ensure_ascii=False, indent=2)
        user_prompt = f"""Outputs completos del equipo hasta ahora:
{context}

Destruye los supuestos débiles, detecta riesgos ocultos y haz las preguntas incómodas.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "weak_assumptions": ["supuesto débil 1", "supuesto débil 2", "supuesto débil 3"],
  "hidden_risks": ["riesgo oculto 1", "riesgo oculto 2"],
  "uncomfortable_questions": ["pregunta incómoda 1", "pregunta incómoda 2", "pregunta incómoda 3"],
  "per_option_verdict": {{
    "option_1": "veredicto breve y directo",
    "option_2": "veredicto breve y directo",
    "option_3": "veredicto breve y directo"
  }},
  "overall_verdict": "fragil",
  "summary": "resumen crítico del conjunto en 2-3 frases"
}}
Los valores posibles para overall_verdict son: "solido", "fragil", "enganosamente_atractivo"."""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "overall_verdict" in data:
            return data
        raise ValueError(
            f"CriticalReviewerAgent.attack_plan — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

import json
from typing import Any, Dict

from agents.base_agent import BaseAgent
from core.llm_client import BaseLLMClient
from schemas import FinalDecision, MissionStatement
from utils.json_parser import extract_json


class DirectorAgent(BaseAgent):

    def __init__(self, llm: BaseLLMClient):
        super().__init__("Director", "director.txt", llm)

    def define_mission(self, case_input: str) -> MissionStatement:
        """Transform raw user input into a structured mission statement."""
        user_prompt = f"""Caso recibido del usuario:
{case_input}

Transforma este input en una misión clara y accionable para el equipo.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "mission": "descripción de la misión en una frase clara",
  "real_decision": "cuál es la decisión real que hay que tomar",
  "key_tension": "la tensión o dilema principal entre las opciones",
  "success_criteria": ["criterio 1", "criterio 2", "criterio 3"]
}}"""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "mission" in data:
            return data
        raise ValueError(
            f"DirectorAgent.define_mission — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

    def make_decision(
        self, mission: MissionStatement, all_outputs: Dict[str, Any]
    ) -> FinalDecision:
        """Synthesize all agent outputs into a final structured decision."""
        context = json.dumps(all_outputs, ensure_ascii=False, indent=2)
        user_prompt = f"""Misión original:
{json.dumps(mission, ensure_ascii=False, indent=2)}

Outputs completos del equipo:
{context}

Con todo lo anterior, toma la decisión final como Director.
Responde ÚNICAMENTE con JSON válido con esta estructura exacta:
{{
  "recommended_option_id": "option_X",
  "recommended_option_name": "nombre completo de la opción elegida",
  "synthesis": "síntesis de la decisión en 2-3 frases claras",
  "rationale": ["razón 1", "razón 2", "razón 3"],
  "what_not_to_ignore": ["punto crítico 1", "punto crítico 2"],
  "next_moves": ["acción concreta 1", "acción concreta 2", "acción concreta 3"],
  "confidence": "alta"
}}"""
        raw = self.llm.generate(self.system_prompt, user_prompt)
        data = extract_json(raw)
        if data and "recommended_option_id" in data:
            return data
        raise ValueError(
            f"DirectorAgent.make_decision — no se pudo parsear la respuesta.\n{raw[:400]}"
        )

import logging
from datetime import datetime
from typing import Any, Dict

from agents.brand_lead import BrandLeadAgent
from agents.creative_director import CreativeDirectorAgent
from agents.critical_reviewer import CriticalReviewerAgent
from agents.director import DirectorAgent
from agents.marketing_lead import MarketingLeadAgent
from agents.operations_lead import OperationsLeadAgent
from agents.product_lead import ProductLeadAgent
from core.llm_client import BaseLLMClient, get_default_client
from core.memory import CaseMemory

logger = logging.getLogger(__name__)

STEPS = [
    "Director define misión",
    "Product Lead propone opciones",
    "Brand Lead evalúa encaje de marca",
    "Marketing Lead crea ángulos de lanzamiento",
    "Operations Lead evalúa viabilidad",
    "Critical Reviewer ataca el plan",
    "Director toma decisión final",
]


class MissionControl:
    """Central orchestrator for Pymmys Mission Control V2."""

    def __init__(self, llm: BaseLLMClient = None, memory_path: str = "cases.json"):
        self.llm = llm or get_default_client()
        self.memory = CaseMemory(memory_path)

        self.director = DirectorAgent(self.llm)
        self.product_lead = ProductLeadAgent(self.llm)
        self.brand_lead = BrandLeadAgent(self.llm)
        self.marketing_lead = MarketingLeadAgent(self.llm)
        self.operations_lead = OperationsLeadAgent(self.llm)
        self.critical_reviewer = CriticalReviewerAgent(self.llm)
        self.creative_director = CreativeDirectorAgent(self.llm)

    def run_case(self, case_input: str) -> Dict[str, Any]:
        case_id = datetime.now().strftime("%Y%m%d%H%M%S")
        logger.info("[%s] Starting workflow for: %s", case_id, case_input[:80])

        self._step(1, "Director define misión")
        mission = self.director.define_mission(case_input)

        self._step(2, "Product Lead propone opciones")
        product_options = self.product_lead.propose_options(mission)

        self._step(3, "Brand Lead evalúa encaje de marca")
        brand_evaluations = self.brand_lead.evaluate_options(product_options)

        self._step(4, "Marketing Lead crea ángulos de lanzamiento")
        marketing_angles = self.marketing_lead.create_launch_angles(product_options)

        self._step(5, "Operations Lead evalúa viabilidad")
        feasibility_assessments = self.operations_lead.assess_feasibility(product_options)

        self._step(6, "Critical Reviewer ataca el plan")
        team_outputs: Dict[str, Any] = {
            "mission": mission,
            "product_options": product_options,
            "brand_evaluations": brand_evaluations,
            "marketing_angles": marketing_angles,
            "feasibility_assessments": feasibility_assessments,
        }
        critical_review = self.critical_reviewer.attack_plan(team_outputs)

        self._step(7, "Director toma decisión final")
        all_outputs = {**team_outputs, "critical_review": critical_review}
        final_decision = self.director.make_decision(mission, all_outputs)

        case: Dict[str, Any] = {
            "id": case_id,
            "created_at": datetime.now().isoformat(),
            "case_input": case_input,
            **all_outputs,
            "final_decision": final_decision,
            "case_type": "strategic",
        }

        self.memory.save_case(case)
        logger.info("[%s] Workflow complete. Decision: %s", case_id, final_decision.get("recommended_option_name"))
        return case

    def run_video_case(self, case_input: str) -> Dict[str, Any]:
        case_id = datetime.now().strftime("%Y%m%d%H%M%S")
        logger.info("[%s] Starting video workflow for: %s", case_id, case_input[:80])

        self._step(1, "Director define misión del vídeo")
        mission = self.director.define_mission(
            f"Quiero crear un vídeo teaser corto para Pymmys. Objetivo: {case_input}"
        )

        self._step(2, "Creative Director crea concepto audiovisual")
        creative_concept = self.creative_director.create_video_concept(mission)

        self._step(3, "Marketing Lead define hook y mensaje")
        marketing_angle = self.marketing_lead.create_launch_angles(
            [
                {
                    "id": "video_teaser_1",
                    "name": "Video teaser Pymmys",
                    "description": str(creative_concept),
                }
            ]
        )

        self._step(4, "Brand Lead revisa encaje de marca")
        brand_check = self.brand_lead.evaluate_options(
            [
                {
                    "id": "video_teaser_1",
                    "name": "Video teaser Pymmys",
                    "description": str(creative_concept),
                }
            ]
        )

        self._step(5, "Critical Reviewer ataca la propuesta")
        critical_review = self.critical_reviewer.attack_plan(
            {
                "mission": mission,
                "creative_concept": creative_concept,
                "marketing_angle": marketing_angle,
                "brand_check": brand_check,
            }
        )

        self._step(6, "Director construye video plan final")
        video_plan = self.llm.generate(
            system_prompt=(
                "Actúas como Director final de Pymmys Mission Control. "
                "Debes construir un video_plan final en JSON."
            ),
            user_prompt=f"""
Construye un video_plan final a partir de este material.

MISSION:
{mission}

CREATIVE_CONCEPT:
{creative_concept}

MARKETING_ANGLE:
{marketing_angle}

BRAND_CHECK:
{brand_check}

CRITICAL_REVIEW:
{critical_review}

Devuelve JSON con:
- title
- objective
- recommended_duration
- scenes (lista de 4 escenas con time, visual, text)
- visual_prompts
- music_direction
- final_note
""".strip(),
        )

        import json
        video_plan = json.loads(video_plan)

        case = {
            "id": case_id,
            "created_at": datetime.now().isoformat(),
            "case_input": case_input,
            "mission": mission,
            "creative_concept": creative_concept,
            "marketing_angle": marketing_angle,
            "brand_check": brand_check,
            "critical_review": critical_review,
            "video_plan": video_plan,
            "case_type": "video_teaser",
        }

        self.memory.save_case(case)
        logger.info("[%s] Video workflow complete.", case_id)
        return case

    @staticmethod
    def _step(number: int, description: str) -> None:
        print(f"  [{number}] {description}...")
from typing import Any, Dict

from agents.base_agent import BaseAgent


class CreativeDirectorAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__("Creative Director", "creative_director.txt", llm)

    def create_video_concept(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
Actúas como Creative Director de Pymmys.

Tu trabajo es transformar esta misión en un concepto de vídeo teaser corto, con hype, tensión, identidad e intriga.

MISIÓN:
{mission}

Devuelve una estructura clara con:
- concept_title
- core_idea
- emotional_tone
- visual_style
- atmosphere
- pacing
- suggested_duration
- closing_feeling

No hagas un anuncio explicativo.
No vendas demasiado.
No seas genérico.
Haz que se sienta premium, intrigante y memorable.
""".strip()

        return self.ask_json(prompt)
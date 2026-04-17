import json
from pathlib import Path
from typing import Any

from core.llm_client import BaseLLMClient

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class BaseAgent:
    """Base class for all Pymmys Mission Control agents.

    Each agent loads its persona from a prompts/*.txt file and exposes
    domain-specific methods that return structured outputs (dicts / lists of dicts).
    """

    def __init__(self, name: str, prompt_file: str, llm: BaseLLMClient):
        self.name = name
        self.llm = llm
        self.system_prompt = self._load_prompt(prompt_file)

    def _load_prompt(self, filename: str) -> str:
        path = PROMPTS_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8").strip()

    def ask(self, user_prompt: str) -> str:
        return self.llm.generate(self.system_prompt, user_prompt)

    def ask_json(self, user_prompt: str) -> Any:
        raw = self.ask(user_prompt)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"{self.name} devolvió una respuesta no válida como JSON.\n\nRespuesta:\n{raw}"
            ) from e
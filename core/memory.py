import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CaseMemory:
    """Persistent JSON storage for Pymmys Mission Control cases.

    Each case is a fully structured dict with all agent outputs and the final decision.
    """

    def __init__(self, path: str = "cases.json"):
        self.path = Path(path)

    def load_cases(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            logger.warning("Could not load cases from %s: %s", self.path, e)
            return []

    def save_case(self, case: Dict[str, Any]) -> None:
        cases = self.load_cases()
        case_id = case.get("id")
        # Replace existing case with the same ID, or append as new
        updated = False
        for i, existing in enumerate(cases):
            if existing.get("id") == case_id:
                cases[i] = case
                updated = True
                break
        if not updated:
            cases.append(case)
        self.path.write_text(
            json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        logger.info("Case %s saved to %s", case_id, self.path)

    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        for case in self.load_cases():
            if case.get("id") == case_id:
                return case
        return None

    def list_cases(self) -> List[Dict[str, str]]:
        """Return a lightweight summary list (id, date, input preview) for all cases."""
        return [
            {
                "id": c.get("id", ""),
                "created_at": c.get("created_at", ""),
                "preview": c.get("case_input", "")[:80],
            }
            for c in self.load_cases()
        ]

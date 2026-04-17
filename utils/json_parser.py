import json
import re
from typing import Any, Optional


def extract_json(text: str) -> Optional[Any]:
    """Extract and parse JSON from an LLM response.

    Handles: raw JSON, ```json blocks, ``` blocks, and embedded JSON objects/arrays.
    Returns None if no valid JSON can be found.
    """
    text = text.strip()

    # 1. Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Try ```json ... ``` block
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. Try ``` ... ``` block (no language tag)
    match = re.search(r"```\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 4. Find the largest embedded JSON object or array
    for pattern in [r"\{[\s\S]*\}", r"\[[\s\S]*\]"]:
        candidates = re.findall(pattern, text)
        for candidate in sorted(candidates, key=len, reverse=True):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue

    return None

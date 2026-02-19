import json
import re

def extract_json(text: str) -> dict:
    """
    Extract the FIRST valid JSON object from LLM output.
    Safely ignores extra text or multiple JSON blocks.
    """
    if not text or not text.strip():
        raise ValueError("Empty response from agent")

    # Find all JSON-like blocks (non-greedy)
    matches = re.findall(r"\{[\s\S]*?\}", text)

    if not matches:
        raise ValueError(f"No JSON object found in response:\n{text}")

    # Try parsing each block until one works
    for block in matches:
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            continue

    # If none are valid JSON
    raise ValueError(f"Found JSON-like text but could not parse it:\n{text}")

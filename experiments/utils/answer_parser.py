import re


def extract_final_answer(text: str) -> str | None:
    """Extract Final Answer line (case-insensitive); returns stripped content or None."""
    match = re.search(r"Final Answer\s*:\s*(.*)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
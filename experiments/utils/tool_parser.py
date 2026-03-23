import re

from utils.answer_parser import extract_final_answer

# Re-export for callers that expect parse_final_answer from tool_parser
parse_final_answer = extract_final_answer


def parse_action(text: str) -> tuple[str | None, str | None]:
    """Extract Action: tool_name(argument); returns (tool, argument) or (None, None)."""
    action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", text)
    if action_match:
        return action_match.group(1), action_match.group(2)
    return None, None
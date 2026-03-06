import re


def extract_final_answer(text):

    match = re.search(r"Final Answer\s*:\s*(.*)", text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None
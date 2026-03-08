import re

def parse_action(text):

    action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", text)

    if action_match:
        tool = action_match.group(1)
        argument = action_match.group(2)
        return tool, argument

    return None, None


def parse_final_answer(text):

    match = re.search(r"Final Answer:\s*(.*)", text)

    if match:
        return match.group(1)

    return None
import json
import os

from openai import OpenAI
from tools.tool_registry import TOOLS
from utils.tool_parser import parse_action, parse_final_answer
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("LLM_MODEL")


def load_prompt():

    with open("../prompts/react_prompt.txt") as f:
        return f.read()


def load_problems():

    with open("../tests/tool_problems.json") as f:
        return json.load(f)


def ask_llm(messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


def run_agent(question):

    prompt_template = load_prompt()

    system_prompt = prompt_template.replace("{question}", question)

    messages = [{"role": "user", "content": system_prompt}]

    for step in range(5):

        output = ask_llm(messages)

        print("\nLLM Output:\n", output)

        final_answer = parse_final_answer(output)

        if final_answer:
            return final_answer

        tool, argument = parse_action(output)

        if tool and tool in TOOLS:

            observation = TOOLS[tool](argument)

            observation_text = f"Observation: {observation}"

            messages.append({"role": "assistant", "content": output})
            messages.append({"role": "user", "content": observation_text})

        else:
            return "No tool used"


def main():

    problems = load_problems()

    for p in problems:

        print("\n=====================")
        print("Question:", p["question"])

        answer = run_agent(p["question"])

        print("\nFinal Answer:", answer)


if __name__ == "__main__":
    main()
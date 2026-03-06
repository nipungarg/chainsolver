import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("LLM_MODEL")


def load_prompt():
    with open("../prompts/baseline_reasoning.txt") as f:
        return f.read()


def load_problems():
    with open("../tests/reasoning_problems.json") as f:
        return json.load(f)


def ask_llm(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


def main():

    prompt_template = load_prompt()
    problems = load_problems()

    results = []

    for p in problems:

        prompt = prompt_template.replace("{question}", p["question"])

        output = ask_llm(prompt)

        print("\nProblem:", p["question"])
        print(output)

        results.append({
            "question": p["question"],
            "output": output
        })

    with open("../experiments/results_single.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
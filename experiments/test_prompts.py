import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("LLM_MODEL")


def load_prompt(path):
    with open(path, "r") as f:
        return f.read()


def load_problems():
    with open("../tests/reasoning_problems.json") as f:
        return json.load(f)


def run_prompt(prompt_template, question):
    prompt = prompt_template.replace("{question}", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content


def evaluate(prompt_name, prompt_path):

    prompt_template = load_prompt(prompt_path)
    problems = load_problems()

    results = []

    for p in problems:

        print(f"\n--- Problem {p['id']} ---")

        output = run_prompt(prompt_template, p["question"])

        print(output)

        results.append({
            "problem_id": p["id"],
            "question": p["question"],
            "output": output
        })

    save_path = f"../experiments/results_{prompt_name}.json"

    with open(save_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved results → {save_path}")


if __name__ == "__main__":

    prompts = {
        "freeform": "../prompts/cot_freeform.txt",
        "numbered": "../prompts/cot_numbered.txt",
        "schema": "../prompts/cot_schema.txt"
    }

    for name, path in prompts.items():

        print("\n============================")
        print(f"Running experiment: {name}")
        print("============================")

        evaluate(name, path)
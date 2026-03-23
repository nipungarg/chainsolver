"""Evaluate multiple CoT prompt variants on reasoning problems."""
from config import ROOT, load_env, get_client, get_model
from utils.io import load_prompt, load_json, save_json
from utils.llm import call_llm_single

load_env()
client = get_client()
MODEL = get_model()

PROMPTS = {
    "freeform": "prompts/cot_freeform.txt",
    "numbered": "prompts/cot_numbered.txt",
    "schema": "prompts/baseline_reasoning.txt",
}


def run_prompt(prompt_template: str, question: str) -> str:
    prompt = prompt_template.replace("{question}", question)
    return call_llm_single(client, MODEL, prompt)


def evaluate(prompt_name: str, prompt_path: str):
    prompt_template = load_prompt(ROOT, *prompt_path.split("/"))
    problems = load_json(ROOT, "tests", "reasoning_problems.json")
    results = []

    for p in problems:
        print(f"\n--- Problem {p['id']} ---")
        output = run_prompt(prompt_template, p["question"])
        print(output)
        results.append({
            "problem_id": p["id"],
            "question": p["question"],
            "output": output,
        })

    save_path = f"experiments/results_{prompt_name}.json"
    save_json(ROOT, results, *save_path.split("/"))
    print(f"\nSaved results → {save_path}")


def main():
    for name, path in PROMPTS.items():
        print("\n============================")
        print(f"Running experiment: {name}")
        print("============================")
        evaluate(name, path)


if __name__ == "__main__":
    main()

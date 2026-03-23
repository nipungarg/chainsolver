"""Single-call baseline: one LLM response per question."""
from config import ROOT, load_env, get_client, get_model
from utils.io import load_prompt, load_json, save_json
from utils.llm import call_llm_single

load_env()
client = get_client()
MODEL = get_model()


def main():
    prompt_template = load_prompt(ROOT, "prompts", "baseline_reasoning.txt")
    problems = load_json(ROOT, "tests", "reasoning_problems.json")
    results = []

    for p in problems:
        prompt = prompt_template.replace("{question}", p["question"])
        output = call_llm_single(client, MODEL, prompt)
        print("\nProblem:", p["question"])
        print(output)
        results.append({"question": p["question"], "output": output})

    save_json(ROOT, results, "experiments", "results_single.json")


if __name__ == "__main__":
    main()

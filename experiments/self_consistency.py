"""Self-consistency: multiple samples and majority vote on final answer."""
from collections import Counter

from config import ROOT, load_env, get_client, get_model
from utils.answer_parser import extract_final_answer
from utils.io import load_prompt, load_json, save_json
from utils.llm import call_llm_single

load_env()
client = get_client()
MODEL = get_model()
NUM_SAMPLES = 5


def majority_vote(answers: list) -> str | None:
    if not answers:
        return None
    return Counter(answers).most_common(1)[0][0]


def solve_with_self_consistency(prompt: str) -> dict:
    reasoning_paths = []
    answers = []
    for _ in range(NUM_SAMPLES):
        output = call_llm_single(client, MODEL, prompt, temperature=0.7)
        reasoning_paths.append(output)
        answer = extract_final_answer(output)
        if answer:
            answers.append(answer)
    return {
        "reasoning_paths": reasoning_paths,
        "answers": answers,
        "final_answer": majority_vote(answers),
    }


def main():
    prompt_template = load_prompt(ROOT, "prompts", "baseline_reasoning.txt")
    problems = load_json(ROOT, "tests", "reasoning_problems.json")
    all_results = []

    for p in problems:
        print("\n==============================")
        print("Problem:", p["question"])
        prompt = prompt_template.replace("{question}", p["question"])
        result = solve_with_self_consistency(prompt)
        print("Answers:", result["answers"])
        print("Majority Answer:", result["final_answer"])
        all_results.append({
            "question": p["question"],
            "answers": result["answers"],
            "majority_answer": result["final_answer"],
            "reasoning_paths": result["reasoning_paths"],
        })

    save_json(ROOT, all_results, "experiments", "results_self_consistency.json")


if __name__ == "__main__":
    main()

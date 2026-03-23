"""Reflection: generate reasoning, then critique and refine."""
from config import ROOT, load_env, get_client, get_model
from utils.answer_parser import extract_final_answer
from utils.io import load_prompt, load_json, save_json
from utils.llm import call_llm_single

load_env()
client = get_client()
MODEL = get_model()


def generate_reasoning(question: str, prompt_template: str, temperature: float = 0) -> str:
    prompt = prompt_template.replace("{question}", question)
    return call_llm_single(client, MODEL, prompt, temperature=temperature)


def critique_reasoning(question: str, reasoning: str, critique_template: str) -> str:
    prompt = critique_template.replace("{question}", question).replace("{reasoning}", reasoning)
    return call_llm_single(client, MODEL, prompt)


def solve_with_reflection(question: str, reasoning_template: str, critique_template: str) -> dict:
    initial = generate_reasoning(question, reasoning_template)
    critique = critique_reasoning(question, initial, critique_template)
    return {
        "initial_reasoning": initial,
        "critique": critique,
        "initial_answer": extract_final_answer(initial),
        "final_answer": extract_final_answer(critique),
    }


def main():
    problems = load_json(ROOT, "tests", "reasoning_problems.json")
    reasoning_prompt = load_prompt(ROOT, "prompts", "baseline_reasoning.txt")
    critique_prompt = load_prompt(ROOT, "prompts", "critique_prompt.txt")
    results = []

    for p in problems:
        print("\n======================")
        print("Problem:", p["question"])
        result = solve_with_reflection(p["question"], reasoning_prompt, critique_prompt)
        print("Initial Answer:", result["initial_answer"])
        print("Final Answer:", result["final_answer"])
        results.append(result)

    save_json(ROOT, results, "experiments", "results_reflection.json")


if __name__ == "__main__":
    main()

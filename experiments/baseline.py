"""Minimal baseline: single problem, no prompt file (for quick sanity checks)."""
from config import ROOT, load_env, get_client, get_model
from utils.io import save_json
from utils.llm import call_llm_single

load_env()
client = get_client()
MODEL = get_model()

PROBLEM = (
    "Sally has 3 brothers. Each brother has 2 sisters. "
    "How many sisters does Sally have? Give only the final answer."
)


def run_baseline():
    answer = call_llm_single(client, MODEL, PROBLEM)
    result = {"problem": PROBLEM, "answer": answer}
    save_json(ROOT, result, "experiments", "results", "baseline.json")
    print("Baseline answer:\n", answer)


if __name__ == "__main__":
    run_baseline()

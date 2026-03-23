"""Minimal chain-of-thought: single problem with system prompt."""
from config import ROOT, load_env, get_client, get_model
from utils.io import save_json
from utils.llm import call_llm

load_env()
client = get_client()
MODEL = get_model()

PROBLEM = (
    "Sally has 3 brothers. Each brother has 2 sisters. "
    "How many sisters does Sally have?"
)
SYSTEM = "Solve the problem step by step. Show all reasoning before giving the final answer."


def run_cot():
    answer = call_llm(
        client,
        MODEL,
        [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROBLEM},
        ],
    )
    result = {
        "problem": PROBLEM,
        "cot_output": answer,
    }
    save_json(ROOT, result, "experiments", "results", "cot_basic.json")
    print("Chain-of-thought output:\n", answer)


if __name__ == "__main__":
    run_cot()

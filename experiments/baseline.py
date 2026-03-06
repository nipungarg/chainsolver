import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("LLM_MODEL")

PROBLEM = """
A store sells pencils in packs of 12.
If a school buys 17 packs and distributes them equally
among 8 classrooms, how many pencils does each classroom get,
and how many remain undistributed?
Give only the final answer.
"""

PROBLEM2 = """
Sally has 3 brothers. Each brother has 2 sisters. How many sisters does Sally have?
"""

def run_baseline():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Answer the question."},
            {"role": "user", "content": PROBLEM2}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    result = {
        "timestamp": str(datetime.now()),
        "problem": PROBLEM2,
        "answer": answer
    }

    os.makedirs("experiments/results", exist_ok=True)

    with open("experiments/results/baseline.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Baseline answer:\n")
    print(answer)

if __name__ == "__main__":
    run_baseline()
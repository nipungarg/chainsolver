import json
import os
from collections import Counter
from openai import OpenAI
from utils.answer_parser import extract_final_answer
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("LLM_MODEL")
NUM_SAMPLES = 5


def load_prompt():
    with open("../prompts/baseline_reasoning.txt") as f:
        return f.read()


def load_problems():
    with open("../tests/reasoning_problems.json") as f:
        return json.load(f)


def sample_reasoning(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def majority_vote(answers):

    counter = Counter(answers)

    most_common = counter.most_common(1)

    if most_common:
        return most_common[0][0]

    return None


def solve_with_self_consistency(prompt):

    reasoning_paths = []
    answers = []

    for _ in range(NUM_SAMPLES):

        output = sample_reasoning(prompt)

        reasoning_paths.append(output)

        answer = extract_final_answer(output)

        if answer:
            answers.append(answer)

    final_answer = majority_vote(answers)

    return {
        "reasoning_paths": reasoning_paths,
        "answers": answers,
        "final_answer": final_answer
    }


def main():

    prompt_template = load_prompt()
    problems = load_problems()

    all_results = []

    for p in problems:

        print("\n==============================")
        print("Problem:", p["question"])

        prompt = prompt_template.replace("{question}", p["question"])

        result = solve_with_self_consistency(prompt)

        print("\nAnswers:", result["answers"])
        print("Majority Answer:", result["final_answer"])

        all_results.append({
            "question": p["question"],
            "answers": result["answers"],
            "majority_answer": result["final_answer"],
            "reasoning_paths": result["reasoning_paths"]
        })

    with open("../experiments/results_self_consistency.json", "w") as f:
        json.dump(all_results, f, indent=2)


if __name__ == "__main__":
    main()
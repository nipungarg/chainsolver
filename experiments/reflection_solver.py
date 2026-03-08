import json
import os
from openai import OpenAI
from utils.answer_parser import extract_final_answer
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("LLM_MODEL")


def load_prompt(path):
    with open(path) as f:
        return f.read()


def load_problems():
    with open("../tests/reasoning_problems.json") as f:
        return json.load(f)


def ask_llm(prompt, temperature=0):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content


def generate_initial_reasoning(question, prompt_template):

    prompt = prompt_template.replace("{question}", question)

    return ask_llm(prompt)


def critique_reasoning(question, reasoning, critique_template):

    critique_prompt = critique_template.replace("{question}", question)

    critique_prompt = critique_prompt.replace("{reasoning}", reasoning)

    return ask_llm(critique_prompt)


def solve_with_reflection(question, reasoning_prompt, critique_prompt):

    initial_reasoning = generate_initial_reasoning(
        question,
        reasoning_prompt
    )

    critique = critique_reasoning(
        question,
        initial_reasoning,
        critique_prompt
    )

    return {
        "initial_reasoning": initial_reasoning,
        "critique": critique,
        "initial_answer": extract_final_answer(initial_reasoning),
        "final_answer": extract_final_answer(critique)
    }


def main():

    problems = load_problems()

    reasoning_prompt = load_prompt("../prompts/baseline_reasoning.txt")

    critique_prompt = load_prompt("../prompts/critique_prompt.txt")

    results = []

    for p in problems:

        print("\n======================")
        print("Problem:", p["question"])

        result = solve_with_reflection(
            p["question"],
            reasoning_prompt,
            critique_prompt
        )

        print("\nInitial Answer:", result["initial_answer"])
        print("Final Answer:", result["final_answer"])

        results.append(result)

    with open("../experiments/results_reflection.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
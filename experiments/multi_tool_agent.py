"""Multi-tool agent: Thought / Action / Observation loop."""
from config import ROOT, load_env, get_client, get_model, get_max_steps
from tools.tool_registry import TOOLS
from utils.io import load_prompt, load_json
from utils.llm import call_llm
from utils.tool_parser import parse_action, parse_final_answer

load_env()
client = get_client()
MODEL = get_model()
MAX_STEPS = get_max_steps()


def run_agent(question: str) -> str:
    prompt_template = load_prompt(ROOT, "prompts", "multi_tool_prompt.txt")
    initial_prompt = prompt_template.replace("{question}", question)
    messages = [{"role": "user", "content": initial_prompt}]

    for _ in range(MAX_STEPS):
        output = call_llm(client, MODEL, messages)
        print("\nLLM Output:\n", output)

        final_answer = parse_final_answer(output)
        if final_answer:
            return final_answer

        tool, argument = parse_action(output)
        if tool and tool in TOOLS:
            print(f"\nExecuting tool: {tool}({argument})")
            observation = TOOLS[tool](argument)
            print("Tool Result:", observation)
            messages.append({"role": "assistant", "content": output})
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            return "Agent stopped: no valid tool used."

    return "Agent stopped: max steps reached."


def main():
    problems = load_json(ROOT, "tests", "multi_tool_problems.json")
    for p in problems:
        print("\n============================")
        print("Question:", p["question"])
        answer = run_agent(p["question"])
        print("\nFinal Answer:", answer)


if __name__ == "__main__":
    main()

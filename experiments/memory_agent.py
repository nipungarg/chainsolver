"""Agent with conversation memory (multi-turn context)."""
from config import ROOT, load_env, get_client, get_model, get_max_steps
from memory.conversation_memory import ConversationMemory
from tools.tool_registry import TOOLS
from utils.io import load_prompt, load_json
from utils.llm import call_llm
from utils.tool_parser import parse_action, parse_final_answer

load_env()
client = get_client()
MODEL = get_model()
MAX_STEPS = get_max_steps()
memory = ConversationMemory()


def run_agent(question: str) -> str:
    prompt_template = load_prompt(ROOT, "prompts", "memory_agent_prompt.txt")
    prompt = prompt_template.replace("{question}", question)
    memory.add("user", prompt)

    for _ in range(MAX_STEPS):
        messages = memory.get_context()
        output = call_llm(client, MODEL, messages)
        print("\nLLM Output:\n", output)
        memory.add("assistant", output)

        final_answer = parse_final_answer(output)
        if final_answer:
            return final_answer

        tool, argument = parse_action(output)
        if tool and tool in TOOLS:
            observation = TOOLS[tool](argument)
            print("Tool Result:", observation)
            memory.add("user", f"Observation: {observation}")
        else:
            return "Agent stopped: no valid tool."

    return "Agent stopped: max steps reached."


def main():
    problems = load_json(ROOT, "tests", "memory_problems.json")
    for p in problems:
        print("\n========================")
        print("Question:", p["question"])
        answer = run_agent(p["question"])
        print("\nFinal Answer:", answer)


if __name__ == "__main__":
    main()

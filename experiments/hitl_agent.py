"""
Human-in-the-loop agent: pause after each reasoning step for approval or feedback.
Run from project root: streamlit run experiments/hitl_agent.py
"""
import re

import streamlit as st

from config import ROOT, load_env, get_client, get_model, get_max_steps
from tools.tool_registry import TOOLS
from utils.io import load_prompt, load_json
from utils.llm import call_llm
from utils.tool_parser import parse_action, parse_final_answer

load_env()
client = get_client()
MODEL = get_model()
MAX_STEPS = get_max_steps()


def run_tool(tool_name: str, argument: str) -> str:
    if tool_name not in TOOLS:
        return f"Error: unknown tool '{tool_name}'"
    try:
        return str(TOOLS[tool_name](argument))
    except Exception as e:
        return f"Error: {e}"


def parse_override(text: str):
    """Parse user override like 'lookup(population of france)' -> ('lookup', 'population of france')."""
    text = text.strip()
    m = re.match(r"\s*(\w+)\s*\((.*)\)\s*", text, re.DOTALL)
    if m:
        return m.group(1), m.group(2).strip()
    return None, None


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question" not in st.session_state:
    st.session_state.question = ""
if "step_count" not in st.session_state:
    st.session_state.step_count = 0
if "pending_output" not in st.session_state:
    st.session_state.pending_output = None
if "final_answer" not in st.session_state:
    st.session_state.final_answer = None


st.set_page_config(page_title="Agent HITL", layout="wide")
st.title("Human-in-the-loop agent")

problems = load_json(ROOT, "tests", "multi_tool_problems.json")
problem_options = [p["question"] for p in problems]

# Question selection
with st.sidebar:
    st.subheader("Question")
    choice = st.radio(
        "Choose a question",
        ["Custom"] + problem_options,
        format_func=lambda x: "Enter below" if x == "Custom" else (x[:60] + "..." if len(x) > 60 else x),
    )
    if choice == "Custom":
        question = st.text_area("Your question", height=100, key="custom_q")
    else:
        question = choice
        st.session_state.question = question

    if question:
        st.session_state.question = question

    if st.button("New run", type="primary"):
        st.session_state.messages = []
        st.session_state.step_count = 0
        st.session_state.pending_output = None
        st.session_state.final_answer = None
        st.rerun()

question = st.session_state.question

if not question:
    st.info("Select or enter a question in the sidebar and click **New run**.")
    st.stop()

# Show conversation so far
st.subheader("Reasoning steps")
if not st.session_state.messages and st.session_state.pending_output is None:
    st.caption("Click **Run next step** below. When the agent suggests a tool use, you'll see **Execute** / **Send feedback** / **Override** / **Reject** for that step.")
for i, msg in enumerate(st.session_state.messages):
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        if content.startswith("Observation:"):
            st.markdown(f"**Observation:** `{content.replace('Observation: ', '')}`")
        else:
            st.markdown(f"**User:** {content[:200]}...")
    else:
        st.markdown(f"**Assistant:**")
        st.text(content)
    st.divider()

# Final answer
if st.session_state.final_answer is not None:
    st.success(f"**Final answer:** {st.session_state.final_answer}")
    st.stop()

# Pending step: show LLM output and ask for approval/feedback/override
pending = st.session_state.pending_output
if pending is not None:
    st.subheader("Pending step (approve or give feedback)")
    st.text(pending)
    tool, argument = parse_action(pending)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Execute tool"):
            if tool and tool in TOOLS:
                obs = run_tool(tool, argument)
                obs_text = f"Observation: {obs}"
                st.session_state.messages.append({"role": "assistant", "content": pending})
                st.session_state.messages.append({"role": "user", "content": obs_text})
                st.session_state.pending_output = None
                st.session_state.step_count += 1
                st.rerun()
            else:
                st.error("Could not parse a valid tool from the output.")
    with col2:
        feedback = st.text_area("Feedback (e.g. 'Use lookup first')", key="fb")
        if st.button("Send feedback and continue"):
            if feedback.strip():
                human_msg = f"Human feedback: {feedback.strip()}\n\nPlease adjust and continue (use the same format: Thought / Action / Observation or Final Answer)."
                st.session_state.messages.append({"role": "assistant", "content": pending})
                st.session_state.messages.append({"role": "user", "content": human_msg})
                st.session_state.pending_output = None
                st.rerun()
    with col3:
        override = st.text_input("Override action (e.g. lookup(population of france))", key="ov")
        if st.button("Run override"):
            t, a = parse_override(override)
            if t and t in TOOLS:
                obs = run_tool(t, a)
                obs_text = f"Observation: {obs}"
                fake_output = f"Thought: Human override.\nAction: {t}({a})"
                st.session_state.messages.append({"role": "assistant", "content": fake_output})
                st.session_state.messages.append({"role": "user", "content": obs_text})
                st.session_state.pending_output = None
                st.session_state.step_count += 1
                st.rerun()
            else:
                st.error("Override must be like: tool_name(argument)")

    if st.button("Reject and get new step"):
        st.session_state.messages.append({"role": "assistant", "content": pending})
        st.session_state.messages.append({"role": "user", "content": "Human: Reject that action. Try a different thought and action."})
        st.session_state.pending_output = None
        st.rerun()
    st.stop()

# No pending step: run next LLM step
if st.session_state.step_count >= MAX_STEPS:
    st.warning("Max steps reached.")
    st.stop()

# Always-visible feedback on reasoning (when there are steps to comment on)
if st.session_state.messages:
    st.subheader("Feedback on reasoning (optional)")
    st.caption("Add a message for the agent (e.g. \"Use lookup first\" or \"Reconsider your approach\"). It will see this when you click **Run next step**.")
    feedback_text = st.text_area("Human feedback", key="reasoning_feedback", placeholder="e.g. Use lookup before searching the web")
    if st.button("Add feedback and continue"):
        if feedback_text.strip():
            human_msg = f"Human feedback: {feedback_text.strip()}\n\nPlease take this into account and continue (use Thought / Action / Observation or Final Answer)."
            st.session_state.messages.append({"role": "user", "content": human_msg})
            st.rerun()
    st.divider()

if st.button("Run next step"):
    prompt_template = load_prompt(ROOT, "prompts", "multi_tool_prompt.txt")
    initial_prompt = prompt_template.replace("{question}", question)
    messages = [{"role": "user", "content": initial_prompt}] + st.session_state.messages

    with st.spinner("Calling LLM..."):
        output = call_llm(client, MODEL, messages)

    final = parse_final_answer(output)
    if final:
        st.session_state.final_answer = final
        st.session_state.messages.append({"role": "assistant", "content": output})
        st.rerun()

    tool, _ = parse_action(output)
    if tool and tool in TOOLS:
        st.session_state.pending_output = output
        st.rerun()
    else:
        st.session_state.messages.append({"role": "assistant", "content": output})
        st.session_state.messages.append({"role": "user", "content": "Observation: No valid tool was used. Please try again or give your Final Answer."})
        st.session_state.step_count += 1
        st.rerun()

st.caption("Click **Run next step** to run the next agent step, then approve or give feedback.")

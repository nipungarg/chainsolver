# ChainSolver

Reasoning experiments: baselines, chain-of-thought, self-consistency, reflection, and tool-using agents (ReAct, multi-tool, memory, human-in-the-loop).

---

## Directory layout

```
chainsolver/
├── experiments/           # Scripts and shared code
│   ├── config.py          # ROOT, load_env, get_client, get_model, get_max_steps
│   ├── utils/
│   │   ├── io.py          # load_prompt, load_json, save_json (paths under ROOT)
│   │   ├── llm.py         # call_llm, call_llm_single
│   │   ├── tool_parser.py # parse_action, parse_final_answer
│   │   └── answer_parser.py  # extract_final_answer (from CoT output)
│   ├── tools/
│   │   ├── tool_registry.py   # TOOLS map (calculator, lookup, search)
│   │   ├── calculator.py      # eval math expression
│   │   ├── knowledge_lookup.py # in-memory facts (e.g. population)
│   │   └── web_search.py      # DuckDuckGo API
│   ├── memory/
│   │   └── conversation_memory.py  # In-session conversation history
│   ├── baseline.py        # Single hardcoded problem, one response
│   ├── baseline_single.py  # One LLM call per question (reasoning_problems)
│   ├── cot_basic.py        # One CoT problem with system prompt
│   ├── test_prompts.py     # Run freeform/numbered/schema CoT prompts on reasoning_problems
│   ├── self_consistency.py # Multiple samples + majority vote on final answer
│   ├── reflection_solver.py # Generate reasoning → critique → refined answer
│   ├── multi_tool_agent.py # Thought/Action/Observation loop (multi_tool_prompt)
│   ├── react_agent.py      # ReAct-style tool loop (react_prompt, tool_problems)
│   ├── memory_agent.py     # Tool agent with conversation memory (memory_problems)
│   └── hitl_agent.py       # Streamlit UI: approve/feedback/override each tool step
├── prompts/               # Prompt templates ({question} placeholder)
│   ├── baseline_reasoning.txt   # structured CoT (steps 1–4); used by baseline, self_consistency, reflection, test_prompts (schema)
│   ├── cot_freeform.txt, cot_numbered.txt
│   ├── critique_prompt.txt
│   ├── react_prompt.txt, multi_tool_prompt.txt
│   └── memory_agent_prompt.txt
├── tests/                 # Problem sets (JSON)
│   ├── reasoning_problems.json
│   ├── tool_problems.json, multi_tool_problems.json
│   └── memory_problems.json
├── .env                   # OPENAI_API_KEY, LLM_MODEL, MAX_STEPS (not committed)
└── requirements.txt
```

Results are written under `experiments/` (e.g. `results_single.json`, `results_self_consistency.json`, `results/`).

---

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
MAX_STEPS=10
```

---

## How to run

From the **project root**:

| Script | Command |
|--------|--------|
| Baseline (one problem) | `python experiments/baseline.py` |
| Baseline (all reasoning problems) | `python experiments/baseline_single.py` |
| CoT basic (one problem) | `python experiments/cot_basic.py` |
| Test CoT prompt variants | `python experiments/test_prompts.py` |
| Self-consistency | `python experiments/self_consistency.py` |
| Reflection (reason + critique) | `python experiments/reflection_solver.py` |
| Multi-tool agent | `python experiments/multi_tool_agent.py` |
| ReAct agent | `python experiments/react_agent.py` |
| Memory agent | `python experiments/memory_agent.py` |
| Human-in-the-loop (Streamlit) | `streamlit run experiments/hitl_agent.py` |

---
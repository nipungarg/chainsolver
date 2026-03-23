"""LLM helpers: single prompt or message list."""
from openai import OpenAI


def call_llm(
    client: OpenAI,
    model: str,
    messages: list,
    temperature: float = 0,
) -> str:
    """Chat completion; returns assistant message content."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def call_llm_single(
    client: OpenAI,
    model: str,
    prompt: str,
    temperature: float = 0,
) -> str:
    """Single user message; returns assistant content."""
    return call_llm(
        client,
        model,
        [{"role": "user", "content": prompt}],
        temperature=temperature,
    )

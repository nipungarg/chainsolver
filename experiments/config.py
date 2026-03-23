"""Shared config: project root, env loading, and OpenAI client."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


def load_env() -> None:
    """Load .env from project root. Call once at app/script entry."""
    load_dotenv(ROOT / ".env")


def get_client():
    """Return OpenAI client (requires load_env() to have been called)."""
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    """Default model name."""
    return os.getenv("LLM_MODEL", "gpt-4o-mini")


def get_max_steps() -> int:
    """Max agent steps (for tool-using agents)."""
    return int(os.getenv("MAX_STEPS", "10"))

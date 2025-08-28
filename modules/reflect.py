"""Generate a brief reflection about a user's message using a local LLM."""

from .llm import LocalLLM


def reflect(user: str, message: str, llm: LocalLLM) -> str:
    """Return a short reflection about why the user asked something."""
    prompt = (
        f"Consider why user '{user}' said: '{message}'. "
        "Respond succinctly in ~30 tokens."
    )
    return llm.generate(prompt)

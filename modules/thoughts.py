"""Generate summary thoughts using a local LLM."""

from .llm import LocalLLM

def summarize(username: str, intent: str, emotions: str, llm: LocalLLM) -> str:
    """Return a short summary of the interaction."""
    prompt = f"User {username} with intent {intent} and emotions {emotions}. Provide summary."
    return llm.generate(prompt)

"""Generate a brief reflection about a user's message using a local LLM."""

from .llm import LocalLLM

try:
    import requests
except Exception:  # pragma: no cover - requests may be missing at runtime
    requests = None


REFLECT_URL = "http://localhost:5150/api/v1/generate"


def _query_service(prompt: str) -> str:
    """Query the external reflection service if available."""
    if not requests:
        return ""
    try:
        resp = requests.post(
            REFLECT_URL,
            json={"prompt": prompt, "max_tokens": 64},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("text") or data.get("response") or ""
    except Exception as e:  # pragma: no cover - network issues
        print(f"Reflection service error: {e}")
        return ""


def reflect(user: str, message: str, llm: LocalLLM) -> str:
    """Return a short reflection about why the user asked something."""
    prompt = (
        f"Consider why user '{user}' said: '{message}'. "
        "Respond succinctly in ~30 tokens."
    )
    response = _query_service(prompt)
    if response:
        return response
    return llm.generate(prompt)

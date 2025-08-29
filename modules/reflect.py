"""Generate a brief reflection about a user's message using a local LLM."""

from .llm import LocalLLM

try:
    import requests
except Exception:  # pragma: no cover - requests may be missing at runtime
    requests = None


def _query_service(prompt: str, cfg: dict) -> str:
    """Query the external reflection service if available."""
    if not requests or "url" not in cfg:
        return ""
    try:
        resp = requests.post(
            cfg["url"],
            json={"prompt": prompt, "max_tokens": cfg.get("max_tokens", 64)},
            timeout=cfg.get("timeout", 5),
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("text") or data.get("response") or ""
    except Exception as e:  # pragma: no cover - network issues
        print(f"Reflection service error: {e}")
        return ""


def reflect(user: str, message: str, llm: LocalLLM, cfg: dict) -> str:
    """Return a short reflection about why the user asked something."""
    prompt = (
        f"Consider why user '{user}' said: '{message}'. "
        "Respond succinctly in ~30 tokens."
    )
    response = _query_service(prompt, cfg)
    if response:
        return response
    return llm.generate(prompt)

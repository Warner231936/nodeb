"""Module for determining user intent."""

def analyze_intent(text: str) -> str:
    """Return a simple intent based on text."""
    if not text:
        return "unknown"
    text = text.lower()
    if "help" in text:
        return "help"
    if "hello" in text:
        return "greeting"
    return "statement"

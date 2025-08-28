"""Module for detecting emotional tone."""

def analyze_emotion(text: str) -> str:
    """Return a basic emotion classification."""
    if not text:
        return "neutral"
    text = text.lower()
    if any(word in text for word in ("happy", "joy", "glad")):
        return "positive"
    if any(word in text for word in ("sad", "angry", "mad")):
        return "negative"
    return "neutral"

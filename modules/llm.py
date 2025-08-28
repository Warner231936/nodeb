"""Module for launching and controlling a local LLM."""

class LocalLLM:
    """Placeholder local LLM controller."""

    def __init__(self):
        self.running = False

    def start(self):
        """Start the LLM."""
        self.running = True
        print("LLM started")

    def generate(self, prompt: str) -> str:
        """Return a canned response."""
        if not self.running:
            return ""
        return f"LLM response to: {prompt}"

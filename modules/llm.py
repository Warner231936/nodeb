"""Module for launching and controlling a local LLM."""

from typing import Optional


class LocalLLM:
    """Placeholder local LLM controller."""

    def __init__(self, model_path: Optional[str]):
        self.model_path = model_path or ""
        self.running = False

    def start(self):
        """Start the LLM."""
        self.running = True
        print(f"LLM started with model {self.model_path}")

    def generate(self, prompt: str) -> str:
        """Return a canned response."""
        if not self.running:
            return ""
        return f"LLM response to: {prompt}"

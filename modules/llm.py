"""Module for launching and controlling a local LLM."""

from pathlib import Path
from typing import Optional


class LocalLLM:
    """Placeholder local LLM controller with basic fallback behaviour."""

    def __init__(self, model_path: Optional[str], offline_response: str = ""):
        self.model_path = model_path or ""
        self.offline_response = offline_response
        self.running = False

    def start(self) -> None:
        """Start the LLM if the model is available.

        When the model path is missing or startup fails the instance switches to
        an offline mode and ``generate`` will return the configured fallback
        response instead of raising errors.
        """

        try:
            if self.model_path and not Path(self.model_path).exists():
                print(f"LLM model not found at {self.model_path}; using offline mode.")
                return
            self.running = True
            print(f"LLM started with model {self.model_path}")
        except Exception as e:  # pragma: no cover - unforeseen startup errors
            print(f"LLM start failed ({e}); using offline mode.")

    def generate(self, prompt: str) -> str:
        """Return a canned response or the offline fallback when stopped."""

        if not self.running:
            return self.offline_response
        try:
            return f"LLM response to: {prompt}"
        except Exception as e:  # pragma: no cover - generation errors
            print(f"LLM generation error ({e}); returning offline response.")
            return self.offline_response

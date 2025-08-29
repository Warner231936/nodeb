"""Short-term memory cache module.

This module keeps a simple key-value store and a queue of recent
messages.  The queue is used by the GUI to show how many messages are
waiting to be processed and to display recent activity.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class CatchMemory:
    """In-memory storage for short-lived data."""

    def __init__(self, capacity: int):
        self.store: Dict[str, Any] = {}
        self.queue: List[Dict[str, Any]] = []
        self.capacity = capacity
        self.gui: Optional[Any] = None

    # ------------------------------------------------------------------
    # Key/value helpers
    def remember(self, key: str, value: Any) -> None:
        self.store[key] = value
        if self.gui:
            self.gui.log_event(f"remember:{key}")

    def recall(self, key: str) -> Any:
        return self.store.get(key)

    # ------------------------------------------------------------------
    # Message queue helpers
    def enqueue(self, user: str, message: str, intent: str, emotion: str) -> None:
        """Add a message to the queue, respecting the capacity."""
        entry = {
            "user": user,
            "message": message,
            "intent": intent,
            "emotion": emotion,
        }
        if len(self.queue) >= self.capacity:
            self.queue.pop(0)
        self.queue.append(entry)
        if self.gui:
            self.gui.display_message(entry)
            self.gui.log_event(f"enqueue:{user}")

    def bind_gui(self, gui: Any) -> None:
        """Attach a GUI instance to receive updates."""
        self.gui = gui

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self.queue)

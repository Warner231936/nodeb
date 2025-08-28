"""Decide whether to engage with a user and log interactions."""

from datetime import datetime

from .database import Database
from .self_state import is_available

def should_respond(user: str, message: str, intent: str, tone: str) -> bool:
    """Return whether the system should answer a user message.

    The decision currently checks a placeholder self-state indicator and
    ignores empty messages.  The :mod:`self_state` module can be expanded
    in the future to provide nuanced behaviour.
    """
    if not message.strip():
        return False
    return is_available()

def log_interaction(db: Database, user: str, message: str, intent: str, tone: str):
    record = {
        "user": user,
        "message": message,
        "intent": intent,
        "tone": tone,
        "timestamp": datetime.utcnow(),
    }
    db.log(record)

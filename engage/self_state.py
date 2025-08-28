"""Lightweight system self‑awareness checks."""

from __future__ import annotations

import json
from pathlib import Path

import psutil

_CPU_LIMIT = 90  # percent
_MEM_LIMIT = 90  # percent
_CONFIG = Path("config.json")


def _maintenance_mode() -> bool:
    if not _CONFIG.exists():
        return False
    try:
        with _CONFIG.open() as fh:
            cfg = json.load(fh)
        return bool(cfg.get("maintenance"))
    except Exception:
        return False


def is_available() -> bool:
    """Return whether the system is in a state to respond.

    The check currently considers a configurable maintenance flag as well as
    CPU and memory utilisation thresholds.
    """

    if _maintenance_mode():
        return False
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return cpu < _CPU_LIMIT and mem < _MEM_LIMIT


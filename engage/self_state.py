
"""Lightweight system self‑awareness checks."""

from __future__ import annotations

import json
from pathlib import Path

import psutil

_DEFAULT_CPU_LIMIT = 90  # percent
_DEFAULT_MEM_LIMIT = 90  # percent
_CONFIG = Path("config.json")


def _load_limits():
    if not _CONFIG.exists():
        return _DEFAULT_CPU_LIMIT, _DEFAULT_MEM_LIMIT
    try:
        with _CONFIG.open() as fh:
            cfg = json.load(fh)
        limits = cfg.get("self_state", {})
        return (
            limits.get("cpu_limit", _DEFAULT_CPU_LIMIT),
            limits.get("mem_limit", _DEFAULT_MEM_LIMIT),
        )
    except Exception:
        return _DEFAULT_CPU_LIMIT, _DEFAULT_MEM_LIMIT


_CPU_LIMIT, _MEM_LIMIT = _load_limits()


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
    """Return whether the system is in a state to respond."""

    if _maintenance_mode():
        return False
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return cpu < _CPU_LIMIT and mem < _MEM_LIMIT

"""Minimal placeholder for Steamworks integration."""
from __future__ import annotations

_initialised = False


def init() -> None:
    global _initialised
    # Placeholder for Steam API initialisation
    _initialised = True


def record_highscore(score: int) -> None:
    if _initialised:
        # In a real implementation, submit the score to Steam here
        pass

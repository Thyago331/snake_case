"""High score persistence utilities."""
from __future__ import annotations
from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "snake_case"


def highscore_path() -> Path:
    return Path(user_data_dir(APP_NAME)) / "highscore.txt"


def _legacy_path() -> Path:
    # fallback for older versions that stored highscore beside the executable
    return Path(__file__).resolve().parents[2] / "highscore.txt"


def load_highscore() -> int:
    for path in (highscore_path(), _legacy_path()):
        try:
            return int(path.read_text())
        except Exception:
            continue
    return 0


def save_highscore(score: int) -> None:
    path = highscore_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(score))

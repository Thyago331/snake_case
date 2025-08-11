import pytest
from snake_case.persistence import highscore


def test_load_save_highscore(monkeypatch, tmp_path):
    user_file = tmp_path / "hs.txt"
    monkeypatch.setattr(highscore, "highscore_path", lambda: user_file)
    highscore.save_highscore(42)
    assert user_file.read_text() == "42"
    assert highscore.load_highscore() == 42


def test_legacy_fallback(monkeypatch, tmp_path):
    user_file = tmp_path / "user" / "hs.txt"
    legacy_file = tmp_path / "legacy" / "hs.txt"
    monkeypatch.setattr(highscore, "highscore_path", lambda: user_file)
    monkeypatch.setattr(highscore, "_legacy_path", lambda: legacy_file)
    legacy_file.parent.mkdir(parents=True)
    legacy_file.write_text("99")
    assert highscore.load_highscore() == 99

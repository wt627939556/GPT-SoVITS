"""Voice preset loading from voices.yaml."""

from pathlib import Path

import yaml


class VoiceNotFoundError(Exception):
    pass


_voices: dict[str, dict] = {}


def load_voices(path: str | Path, defaults: dict | None = None) -> dict[str, dict]:
    global _voices
    with open(path) as f:
        _voices = yaml.safe_load(f) or {}
    if defaults:
        for voice in _voices.values():
            for k, v in defaults.items():
                voice.setdefault(k, v)
    return _voices


def get_voice(name: str) -> dict:
    if name not in _voices:
        raise VoiceNotFoundError(f"voice '{name}' not found")
    return dict(_voices[name])

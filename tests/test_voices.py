"""Tests for voice preset loading from voices.yaml."""

import os
import tempfile

import yaml
import pytest

from openai_tts_proxy.voices import load_voices, get_voice, VoiceNotFoundError


SAMPLE_VOICES = {
    "elysia": {
        "ref_audio_path": "/data/reference_audio/elysia.wav",
        "prompt_text": "我是罗浮云骑将军景元",
        "prompt_lang": "zh",
        "text_lang": "zh",
        "text_split_method": "cut5",
        "speed_factor": 1.0,
    },
    "echo": {
        "ref_audio_path": "/data/reference_audio/echo.wav",
        "prompt_text": "Hello, I am Echo.",
        "prompt_lang": "en",
        "text_lang": "en",
        "text_split_method": "cut0",
        "speed_factor": 1.0,
    },
}


@pytest.fixture
def voices_yaml_path():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(SAMPLE_VOICES, f, default_flow_style=False, allow_unicode=True)
    yield f.name
    os.unlink(f.name)


def test_load_voices_returns_dict(voices_yaml_path):
    voices = load_voices(voices_yaml_path)
    assert isinstance(voices, dict)
    assert "elysia" in voices
    assert "echo" in voices


def test_get_voice_returns_preset(voices_yaml_path):
    load_voices(voices_yaml_path)
    preset = get_voice("elysia")
    assert preset["ref_audio_path"] == "/data/reference_audio/elysia.wav"
    assert preset["prompt_lang"] == "zh"


def test_get_voice_unknown_raises(voices_yaml_path):
    load_voices(voices_yaml_path)
    with pytest.raises(VoiceNotFoundError) as exc:
        get_voice("nonexistent")
    assert "nonexistent" in str(exc.value)


def test_load_voices_merges_defaults(voices_yaml_path):
    voices = load_voices(voices_yaml_path, defaults={"batch_size": 1})
    assert voices["elysia"]["batch_size"] == 1
    assert voices["elysia"]["ref_audio_path"] == "/data/reference_audio/elysia.wav"

"""Tests for OpenAI TTS proxy FastAPI endpoints."""

import os
import tempfile
from unittest.mock import patch, AsyncMock, MagicMock

import yaml
import pytest
from fastapi.testclient import TestClient


SAMPLE_VOICES = {
    "elysia": {
        "ref_audio_path": "/data/reference_audio/elysia.wav",
        "prompt_text": "我是景元",
        "prompt_lang": "zh",
        "text_lang": "zh",
        "text_split_method": "cut5",
    },
}

VALID_REQUEST = {
    "model": "tts-1",
    "input": "你好世界",
    "voice": "elysia",
    "response_format": "wav",
    "speed": 1.0,
}


@pytest.fixture
def voices_yaml_path():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(SAMPLE_VOICES, f, default_flow_style=False, allow_unicode=True)
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def client(voices_yaml_path):
    with patch("openai_tts_proxy.app.httpx") as mock_httpx:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake-wav-data"
        mock_response.headers = {"content-type": "audio/wav"}
        mock_client = MagicMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_httpx.AsyncClient.return_value.__aenter__.return_value = mock_client

        from openai_tts_proxy.app import create_app

        app = create_app(voices_path=voices_yaml_path)
        with TestClient(app) as tc:
            yield tc


def test_v1_audio_speech_returns_audio(client):
    resp = client.post("/v1/audio/speech", json=VALID_REQUEST)
    assert resp.status_code == 200
    assert resp.content == b"fake-wav-data"


def test_audio_speech_alias_works(client):
    resp = client.post("/audio/speech", json=VALID_REQUEST)
    assert resp.status_code == 200


def test_rejects_unsupported_format(client):
    req = {**VALID_REQUEST, "response_format": "mp3"}
    resp = client.post("/v1/audio/speech", json=req)
    assert resp.status_code == 400
    body = resp.json()
    assert "error" in body
    assert "mp3" in str(body["error"]["message"])


def test_rejects_unknown_voice(client):
    req = {**VALID_REQUEST, "voice": "unknown_voice"}
    resp = client.post("/v1/audio/speech", json=req)
    assert resp.status_code == 400
    body = resp.json()
    assert "error" in body
    assert "unknown_voice" in str(body["error"]["message"])


def test_sanitizes_input_before_forwarding(client):
    req = {**VALID_REQUEST, "input": "[tts:text]你好世界[/tts:text]]"}
    resp = client.post("/v1/audio/speech", json=req)
    assert resp.status_code == 200


def test_rejects_non_numeric_speed(client):
    req = {**VALID_REQUEST, "speed": "fast"}
    resp = client.post("/v1/audio/speech", json=req)
    assert resp.status_code == 400
    body = resp.json()
    assert "error" in body
    assert "speed" in str(body["error"]["message"]).lower()


def test_rejects_input_that_becomes_empty_after_sanitization(client):
    req = {**VALID_REQUEST, "input": "[/tts:text]]"}
    resp = client.post("/v1/audio/speech", json=req)
    assert resp.status_code == 400
    assert "input" in str(resp.json()["error"]["message"]).lower()


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

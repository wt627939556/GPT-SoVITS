"""Tests for OpenAI-to-GPT-SoVITS field mapping."""

import pytest

from openai_tts_proxy.mapper import (
    map_openai_to_tts,
    SUPPORTED_FORMATS,
    UnsupportedFormatError,
)


def test_maps_basic_fields():
    preset = {
        "ref_audio_path": "/data/reference_audio/elysia.wav",
        "prompt_text": "我是景元",
        "prompt_lang": "zh",
        "text_lang": "zh",
        "text_split_method": "cut5",
    }
    result = map_openai_to_tts(
        model="tts-1",
        input_text="你好世界",
        voice_preset=preset,
        response_format="wav",
        speed=1.0,
    )
    assert result["text"] == "你好世界"
    assert result["text_lang"] == "zh"
    assert result["ref_audio_path"] == "/data/reference_audio/elysia.wav"
    assert result["prompt_text"] == "我是景元"
    assert result["prompt_lang"] == "zh"
    assert result["text_split_method"] == "cut5"
    assert result["media_type"] == "wav"
    assert result["speed_factor"] == 1.0


def test_maps_pcm_format():
    preset = {
        "ref_audio_path": "/data/ref.wav",
        "prompt_lang": "zh",
        "text_lang": "zh",
    }
    result = map_openai_to_tts(
        model="tts-1-hd",
        input_text="test",
        voice_preset=preset,
        response_format="pcm",
        speed=1.0,
    )
    assert result["media_type"] == "raw"


def test_speed_scales_speed_factor():
    preset = {
        "ref_audio_path": "/data/ref.wav",
        "prompt_lang": "zh",
        "text_lang": "zh",
    }
    result = map_openai_to_tts(
        model="tts-1",
        input_text="test",
        voice_preset=preset,
        response_format="wav",
        speed=2.0,
    )
    assert result["speed_factor"] == 2.0


def test_rejects_mp3_format():
    preset = {
        "ref_audio_path": "/data/ref.wav",
        "prompt_lang": "zh",
        "text_lang": "zh",
    }
    with pytest.raises(UnsupportedFormatError) as exc:
        map_openai_to_tts(
            model="tts-1",
            input_text="test",
            voice_preset=preset,
            response_format="mp3",
            speed=1.0,
        )
    assert "mp3" in str(exc.value)


def test_rejects_opus_format():
    preset = {
        "ref_audio_path": "/data/ref.wav",
        "prompt_lang": "zh",
        "text_lang": "zh",
    }
    with pytest.raises(UnsupportedFormatError):
        map_openai_to_tts(
            model="tts-1",
            input_text="test",
            voice_preset=preset,
            response_format="opus",
            speed=1.0,
        )


def test_preset_overrides_are_preserved():
    preset = {
        "ref_audio_path": "/data/ref.wav",
        "prompt_lang": "zh",
        "text_lang": "zh",
        "batch_size": 4,
        "top_k": 20,
        "streaming_mode": 1,
    }
    result = map_openai_to_tts(
        model="tts-1",
        input_text="test",
        voice_preset=preset,
        response_format="wav",
        speed=1.0,
    )
    assert result["batch_size"] == 4
    assert result["top_k"] == 20
    assert result["streaming_mode"] == 1


def test_supported_formats_list():
    assert "wav" in SUPPORTED_FORMATS
    assert "pcm" in SUPPORTED_FORMATS
    assert "mp3" not in SUPPORTED_FORMATS

"""Tests for OpenClaw-style TTS tag sanitization."""

from openai_tts_proxy.sanitizer import sanitize_text


def test_passthrough_clean_text():
    """Clean text without tags passes through unchanged."""
    assert sanitize_text("你好世界") == "你好世界"


def test_strips_tts_text_tag():
    """[tts:text]...[/tts:text] tags are removed, content preserved."""
    result = sanitize_text("[tts:text]你好世界[/tts:text]")
    assert result == "你好世界"


def test_strips_bracket_bracket_suffix():
    """Trailing [/tts:text]] double-bracket variant is cleaned."""
    result = sanitize_text("[tts:text]你好世界[/tts:text]]")
    assert result == "你好世界"


def test_strips_multiline_content():
    """Multiline text with tags is cleaned correctly."""
    result = sanitize_text("[tts:text]第一行\n第二行[/tts:text]")
    assert result == "第一行\n第二行"


def test_handles_empty_input():
    """Empty string returns empty string."""
    assert sanitize_text("") == ""

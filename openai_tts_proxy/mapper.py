"""Map OpenAI TTS fields to GPT-SoVITS /tts fields."""

SUPPORTED_FORMATS = {"wav", "pcm"}

_FORMAT_MAP = {"wav": "wav", "pcm": "raw"}


class UnsupportedFormatError(Exception):
    pass


def map_openai_to_tts(
    *,
    model: str,
    input_text: str,
    voice_preset: dict,
    response_format: str,
    speed: float,
) -> dict:
    fmt = response_format.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(
            f"response_format '{response_format}' is not supported; "
            f"supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )

    tts_request = {
        "text": input_text,
        "media_type": _FORMAT_MAP[fmt],
        "speed_factor": speed,
        **voice_preset,
    }

    return tts_request

"""OpenAI-compatible TTS proxy that forwards to GPT-SoVITS /tts."""

import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from .mapper import map_openai_to_tts, UnsupportedFormatError
from .sanitizer import sanitize_text
from .voices import load_voices, get_voice, VoiceNotFoundError


GPT_SOVITS_API_URL = "GPT_SOVITS_API_URL"


def create_app(voices_path: str | None = None) -> FastAPI:
    app = FastAPI(title="OpenAI TTS Proxy")

    vpath = voices_path or os.environ.get("VOICES_CONFIG", "voices.yaml")
    load_voices(vpath)

    @app.post("/v1/audio/speech")
    @app.post("/audio/speech")
    async def audio_speech(request: Request):
        try:
            body = await request.json()
        except Exception:
            return _openai_error("invalid_request_error", "invalid JSON body", 400)

        model = body.get("model", "tts-1")
        input_text = body.get("input", "")
        voice_name = body.get("voice", "")
        response_format = body.get("response_format", "wav")
        speed = float(body.get("speed", 1.0))

        if not input_text:
            return _openai_error("invalid_request_error", "input is required", 400)

        try:
            preset = get_voice(voice_name)
        except VoiceNotFoundError:
            return _openai_error(
                "invalid_request_error",
                f"voice '{voice_name}' is not supported",
                400,
            )

        cleaned = sanitize_text(input_text)

        try:
            tts_params = map_openai_to_tts(
                model=model,
                input_text=cleaned,
                voice_preset=preset,
                response_format=response_format,
                speed=speed,
            )
        except UnsupportedFormatError as e:
            return _openai_error("invalid_request_error", str(e), 400)

        api_url = os.environ.get(GPT_SOVITS_API_URL, "http://localhost:9880")
        async with httpx.AsyncClient(timeout=120) as client:
            upstream = await client.post(f"{api_url}/tts", params=tts_params)

        if upstream.status_code != 200:
            return _openai_error(
                "api_error",
                f"upstream TTS failed: {upstream.status_code}",
                502,
            )

        content_type = upstream.headers.get("content-type", "audio/wav")
        return Response(content=upstream.content, media_type=content_type)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


def _openai_error(error_type: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "type": error_type,
                "param": None,
                "code": None,
            }
        },
    )

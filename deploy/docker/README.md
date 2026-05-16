# Docker Deployment Additions

This fork keeps the upstream GPT-SoVITS source code intact and adds a small deployment layer for inference-focused Docker usage.

## What This Fork Adds

- A CPU-default GPT-SoVITS API image in `deploy/docker/Dockerfile`.
- A CUDA-capable build path through `CUDA_VERSION` and the `gpu` Compose profile.
- Runtime generation of `GPT_SoVITS/configs/tts_infer.yaml` from environment variables.
- Volume layout for pretrained models, G2PW, custom weights, reference audio, cache, output, and temp files under `/data`.
- An optional WebUI image in `deploy/docker/Dockerfile.webui` that pins FastAPI/Starlette versions known to work with Gradio 4.
- A separate OpenAI-compatible TTS proxy under `openai_tts_proxy/`.

The proxy exposes:

- `POST /v1/audio/speech`
- `POST /audio/speech`

It accepts common OpenAI TTS fields: `model`, `input`, `voice`, `response_format`, and `speed`. The proxy forwards to the official GPT-SoVITS `/tts` endpoint instead of reimplementing synthesis.

Supported response formats are `wav`, `pcm`, and `mp3`. MP3 is implemented by requesting WAV from GPT-SoVITS and transcoding it in the proxy with `ffmpeg`.

## Data Layout

Set `DATA_ROOT` to a host directory containing:

```text
pretrained_models/
G2PWModel/
asr_models/
uvr5_weights/
custom_weights/
reference_audio/
cache/
output/
temp/
```

Custom model weights can be selected at container startup:

```text
GPT_SOVITS_CUSTOM_T2S_PATH=/data/custom_weights/path/to/model.ckpt
GPT_SOVITS_CUSTOM_VITS_PATH=/data/custom_weights/path/to/model.pth
```

Voice presets for the OpenAI proxy are configured with a `voices.yaml` file. See `openai_tts_proxy/voices.yaml.example`.

## Basic Startup

From the repository root:

```bash
docker compose -f deploy/docker/docker-compose.yaml up -d gpt-sovits-api openai-tts-proxy
```

Optional WebUI:

```bash
docker compose -f deploy/docker/docker-compose.yaml --profile webui up -d gpt-sovits-webui
```

Optional GPU API:

```bash
docker compose -f deploy/docker/docker-compose.yaml --profile gpu up -d gpt-sovits-api-gpu
```

## OpenAI-Compatible TTS Example

```bash
curl -o speech.wav http://127.0.0.1:8000/v1/audio/speech \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "tts-1",
    "input": "你好，欢迎使用 GPT-SoVITS。",
    "voice": "elysia",
    "response_format": "wav",
    "speed": 1.0
  }'
```

The example voice name is only a preset key. Replace it with entries from your own `voices.yaml`.

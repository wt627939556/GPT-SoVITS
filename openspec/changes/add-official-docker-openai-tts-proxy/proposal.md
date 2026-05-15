## Why

The current working GPT-SoVITS deployment is based on a third-party inference snapshot and carries local source patches for the OpenAI-compatible TTS endpoint. Moving to the official upstream fork should make future updates, training, and model-version support easier while keeping local OpenAI compatibility isolated from upstream source files.

## What Changes

- Add a non-invasive Docker deployment layer for the official GPT-SoVITS repository.
- Add a CPU-first GPT-SoVITS API service that runs official `api_v2.py` without modifying upstream source files.
- Add optional GPU-profile GPT-SoVITS services for future CUDA hardware.
- Add a separate OpenAI-compatible TTS proxy service that exposes `/audio/speech` and `/v1/audio/speech`.
- Configure the proxy to translate OpenAI TTS fields into official GPT-SoVITS `/tts` requests.
- Use a `voices.yaml` mapping for one loaded model with multiple reference-audio voice presets; first preset is `elysia`.
- Keep local runtime `.env` and absolute persistence paths outside the repository.
- Do not modify official source files such as `api_v2.py`, `requirements.txt`, or `GPT_SoVITS/*`.

## Capabilities

### New Capabilities

- `official-docker-deployment`: CPU-default and GPU-profile Docker deployment for official GPT-SoVITS without source patches.
- `openai-tts-proxy`: OpenAI-compatible TTS proxy that forwards to the official GPT-SoVITS `/tts` API.

### Modified Capabilities

- None.

## Impact

- Adds repository-local deployment files under `deploy/docker/`.
- Adds repository-local proxy code under `openai_tts_proxy/`.
- Adds repository-local compose template that avoids user-specific absolute paths.
- Adds local runtime compose/env under `~/docker/gpt-sovits-official/` outside the repository.
- Requires a new persistence root at `/stockroom/docker_container_data/gpt-sovits-official` for this machine.

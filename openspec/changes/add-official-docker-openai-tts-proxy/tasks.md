## 1. Deployment Layer

- [x] 1.1 Add `deploy/docker/Dockerfile` for official GPT-SoVITS with CPU default and CUDA build args.
- [x] 1.2 Add `deploy/docker/start.sh` to render runtime config, link persistence directories, and start official `api_v2.py` or WebUI.
- [x] 1.3 Add `deploy/docker/render_tts_config.py` to generate `tts_infer.yaml` from environment variables.
- [x] 1.4 Add repository compose template under `deploy/docker/docker-compose.yaml` without user-specific absolute paths.

## 2. OpenAI TTS Proxy

- [ ] 2.1 Add `openai_tts_proxy/app.py` with `/audio/speech` and `/v1/audio/speech`.
- [x] 2.2 Add `openai_tts_proxy/voices.yaml.example` with an `elysia` preset.
- [ ] 2.3 Add `openai_tts_proxy/requirements.txt` and `openai_tts_proxy/Dockerfile`.
- [x] 2.4 Map OpenAI fields `model`, `input`, `voice`, `response_format`, and `speed` to official `/tts`.
- [x] 2.5 Sanitize OpenClaw-style TTS tags before forwarding text.
- [ ] 2.6 Return OpenAI-shaped JSON errors for unsupported voice, model, input, or format.

## 3. Local Runtime Setup

- [ ] 3.1 Create `~/docker/gpt-sovits-official/docker-compose.yaml` for local operation.
- [ ] 3.2 Create `~/docker/gpt-sovits-official/.env` with local paths and current Elysia model settings.
- [ ] 3.3 Create expected persistence directories under `/stockroom/docker_container_data/gpt-sovits-official`.
- [ ] 3.4 Provide commands or notes to migrate pretrained models, G2PW, custom Elysia weights, and reference audio from the old persistence root.

## 4. Verification

- [ ] 4.1 Run proxy unit tests for request mapping and input sanitization.
- [ ] 4.2 Validate compose config for CPU default services.
- [ ] 4.3 Build the CPU GPT-SoVITS image and proxy image.
- [ ] 4.4 Start CPU API plus proxy and verify health endpoints.
- [ ] 4.5 Generate a WAV through `/v1/audio/speech` using the known Elysia test sentence and record the output path.
- [ ] 4.6 Confirm official source files remain unmodified.

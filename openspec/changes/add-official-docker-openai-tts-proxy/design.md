## Context

The current service works, but it is based on `AI-Hobbyist/GPT-SoVITS-Inference` and includes local patches to `api_v2.py` for OpenAI-compatible TTS. The new repository is a fork of official `RVC-Boss/GPT-SoVITS`, so future upstream updates should be easier if custom behavior is kept outside official source files.

Official GPT-SoVITS already exposes `/tts` through `api_v2.py`. It does not expose OpenAI-compatible `/audio/speech`. The desired design is therefore a small adapter service that owns OpenAI compatibility and forwards to official `/tts`.

## Goals / Non-Goals

**Goals:**

- Keep official GPT-SoVITS source files unmodified.
- Provide CPU-default Docker deployment for the official API.
- Include GPU profile services for future CUDA hardware.
- Provide OpenAI-compatible `/audio/speech` and `/v1/audio/speech` through a separate proxy.
- Support the current Elysia scenario with a `voices.yaml` preset.
- Keep local absolute paths and secrets out of the repository.

**Non-Goals:**

- Do not implement GPT-SoVITS training automation in this change.
- Do not implement dynamic model switching per voice in the first version.
- Do not make the proxy a generic multi-backend TTS gateway.
- Do not modify official `api_v2.py`, `requirements.txt`, or model code.

## Decisions

1. Use FastAPI for the proxy.

FastAPI matches the official API stack and keeps request/response handling simple. Flask would also work, but FastAPI avoids mixing frameworks and gives typed request models with little code.

2. Keep model selection in GPT-SoVITS service startup, not in the proxy.

The first version assumes one loaded GPT/SoVITS weight pair. `voices.yaml` maps voice names to reference audio, prompt text, language, split method, and inference parameters. This avoids runtime `/set_gpt_weights` calls that would make concurrency and latency fragile.

3. Use `voices.yaml` for voice presets.

The first file will contain `elysia`, but the schema supports more presets that share the currently loaded model. This keeps future fine-tuned reference presets out of code.

4. Proxy forwards `wav` and `pcm` only in the first version.

Official `/tts` supports `wav`, `raw`, `ogg`, and `aac`, but not `mp3`. To keep the first version small, `mp3` should return a clear OpenAI-shaped 400 error. MP3 transcoding can be added later if a caller actually needs it.

5. Repository compose is generic; local compose/env is machine-specific.

The repository compose template should use relative paths and variables. The local runtime copy under `~/docker/gpt-sovits-official` can set `/stockroom/docker_container_data/gpt-sovits-official`.

## Risks / Trade-offs

- Official dependency drift may break the custom CPU image. Mitigation: keep Dockerfile small and close to official requirements, then verify by building CPU first.
- Proxy and official API can disagree on supported `/tts` fields after upstream updates. Mitigation: keep proxy mapping thin and test against `/tts`.
- Multiple voice presets using different model weights are not supported in v1. Mitigation: document this explicitly and add dynamic model switching or multi-container routing only when needed.
- GPU profile cannot be verified on the current machine. Mitigation: include it as a compose profile and keep CPU as the default path.

## Migration Plan

1. Add Docker/proxy files in the official fork without changing upstream source files.
2. Create local runtime directory `~/docker/gpt-sovits-official`.
3. Use persistence root `/stockroom/docker_container_data/gpt-sovits-official`.
4. Copy or manually migrate required pretrained models, G2PW files, Elysia weights, and reference audio from the old persistence root.
5. Build and start CPU GPT-SoVITS API plus proxy.
6. Test official `/tts`, then test proxy `/v1/audio/speech` with the known Elysia sentence.
7. Keep the old service available until the new service is verified.

## Open Questions

- Whether to copy existing persistence data or use temporary symlinks during migration.
- Whether OpenClaw/Hermes needs `mp3` response format later.
- Whether the first GPU target will be Tesla P4 or NVIDIA A2, which affects the best CUDA image and `is_half` default.

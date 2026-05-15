## ADDED Requirements

### Requirement: OpenAI-compatible speech endpoint

The proxy SHALL expose `POST /audio/speech` and `POST /v1/audio/speech` compatible with common OpenAI TTS request fields.

#### Scenario: Generate speech

- **WHEN** a client posts `model`, `input`, `voice`, `response_format`, and `speed` to `/v1/audio/speech`
- **THEN** the proxy forwards an equivalent request to the official GPT-SoVITS `/tts` endpoint
- **AND** the proxy returns the audio response to the client

### Requirement: Voice preset mapping

The proxy SHALL load voice presets from a YAML file and use the selected voice to populate GPT-SoVITS reference audio, prompt text, language, split method, and inference defaults.

#### Scenario: Resolve Elysia voice

- **WHEN** a request uses `voice=elysia`
- **THEN** the proxy loads the `elysia` preset from `voices.yaml`
- **AND** the forwarded `/tts` request includes that preset's reference audio and prompt settings

### Requirement: One loaded model in first version

The proxy SHALL assume one GPT-SoVITS model pair is already loaded by the upstream service and SHALL NOT switch GPT or SoVITS weights per voice in the first version.

#### Scenario: Voice request does not switch model weights

- **WHEN** a voice preset is selected
- **THEN** the proxy forwards only `/tts` synthesis parameters
- **AND** the proxy does not call `/set_gpt_weights` or `/set_sovits_weights`

### Requirement: Input sanitization

The proxy SHALL remove OpenClaw-style TTS control tags before forwarding text to GPT-SoVITS.

#### Scenario: Clean tagged input

- **WHEN** input contains tags such as `[tts:text]` or `[/tts:text]]`
- **THEN** the forwarded text excludes those tags while preserving the spoken text

### Requirement: Response format support

The proxy SHALL support `wav` and `pcm` response formats in the first version and SHALL reject unsupported formats with an OpenAI-shaped error.

#### Scenario: Reject mp3 format

- **WHEN** a request uses `response_format=mp3`
- **THEN** the proxy returns HTTP 400 with an OpenAI-shaped error body

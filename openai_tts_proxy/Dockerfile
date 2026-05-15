FROM python:3.12-slim

LABEL org.opencontainers.image.title="GPT-SoVITS OpenAI TTS Proxy"
LABEL org.opencontainers.image.description="OpenAI-compatible TTS proxy for GPT-SoVITS"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY openai_tts_proxy/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY openai_tts_proxy/ /app/openai_tts_proxy/

ENV PYTHONPATH=/app
ENV VOICES_CONFIG=/app/voices.yaml

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s \
    CMD curl --max-time 5 --fail --silent --output /dev/null http://localhost:8000/health

USER appuser

CMD ["python", "-m", "uvicorn", "openai_tts_proxy.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

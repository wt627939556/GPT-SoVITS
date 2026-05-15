ARG CUDA_VERSION=
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

LABEL org.opencontainers.image.title="GPT-SoVITS"
LABEL org.opencontainers.image.description="Official GPT-SoVITS API service (CPU default, CUDA optional)"

ARG CUDA_VERSION
ENV CUDA_VERSION=${CUDA_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    ffmpeg \
    libsndfile1 \
    libopenblas-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY requirements.txt extra-req.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ -z "$CUDA_VERSION" ]; then \
      pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu; \
    else \
      pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cu${CUDA_VERSION/./}; \
    fi && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r extra-req.txt

COPY . /app

RUN mkdir -p /data/pretrained_models \
    /data/G2PWModel \
    /data/asr_models \
    /data/uvr5_weights \
    /data/custom_weights \
    /data/reference_audio \
    /data/cache \
    /data/output \
    /data/temp && \
    chown -R appuser:appuser /app /data

COPY deploy/docker/start.sh deploy/docker/render_tts_config.py /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

ENV PYTHONPATH="/app"
ENV GPT_SOVITS_DATA_ROOT=/data
ENV GPT_SOVITS_DEVICE=cpu
ENV GPT_SOVITS_IS_HALF=false
ENV GPT_SOVITS_VERSION=v2

EXPOSE 9880

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=180s \
    CMD curl --max-time 5 --fail --silent --output /dev/null http://localhost:9880/openapi.json

USER appuser:appuser

CMD ["/usr/local/bin/start.sh"]

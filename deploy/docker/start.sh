#!/usr/bin/env bash
set -euo pipefail

DATA_ROOT="${GPT_SOVITS_DATA_ROOT:-/data}"
CONFIG_OUTPUT="${GPT_SOVITS_CONFIG_OUTPUT:-GPT_SoVITS/configs/tts_infer.yaml}"
API_HOST="${GPT_SOVITS_API_HOST:-0.0.0.0}"
API_PORT="${GPT_SOVITS_API_PORT:-9880}"

echo "==> Linking persistence directories from ${DATA_ROOT}"

link_dir() {
    local src="$1"
    local dst="$2"
    if [ -d "$src" ]; then
        rm -rf "$dst"
        ln -sfn "$src" "$dst"
        echo "    ${dst} -> ${src}"
    else
        echo "    WARNING: source ${src} not found, skipping"
    fi
}

link_dir "${DATA_ROOT}/pretrained_models"  GPT_SoVITS/pretrained_models
link_dir "${DATA_ROOT}/G2PWModel"          GPT_SoVITS/text/G2PWModel
link_dir "${DATA_ROOT}/asr_models"         tools/asr/models
link_dir "${DATA_ROOT}/uvr5_weights"       tools/uvr5/uvr5_weights

echo "==> Rendering tts_infer.yaml"
python deploy/docker/render_tts_config.py

echo "==> Starting GPT-SoVITS API on ${API_HOST}:${API_PORT}"
exec python api_v2.py -a "$API_HOST" -p "$API_PORT" -c "$CONFIG_OUTPUT"

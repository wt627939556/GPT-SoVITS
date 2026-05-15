#!/usr/bin/env python3
"""Render tts_infer.yaml from environment variables.

Environment:
    GPT_SOVITS_CONFIG_OUTPUT: path to write the generated YAML file
    GPT_SOVITS_DATA_ROOT:     root for model persistence paths (default /data)
    GPT_SOVITS_DEVICE:        cpu or cuda (default cpu)
    GPT_SOVITS_IS_HALF:       true or false (default false)
    GPT_SOVITS_VERSION:       v1|v2|v3|v4|v2Pro|v2ProPlus (default v2)
"""

import os
import sys

import yaml

VERSION_CONFIG = {
    "v1": {
        "t2s_weights_path": "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
        "vits_weights_path": "GPT_SoVITS/pretrained_models/s2G488k.pth",
    },
    "v2": {
        "t2s_weights_path": "GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt",
        "vits_weights_path": "GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
    },
    "v3": {
        "t2s_weights_path": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
        "vits_weights_path": "GPT_SoVITS/pretrained_models/s2Gv3.pth",
    },
    "v4": {
        "t2s_weights_path": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
        "vits_weights_path": "GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth",
    },
    "v2Pro": {
        "t2s_weights_path": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
        "vits_weights_path": "GPT_SoVITS/pretrained_models/v2Pro/s2Gv2Pro.pth",
    },
    "v2ProPlus": {
        "t2s_weights_path": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
        "vits_weights_path": "GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth",
    },
}

BERT_BASE = "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large"
CNHUBERT_BASE = "GPT_SoVITS/pretrained_models/chinese-hubert-base"


def _bool_env(name: str, default: bool = False) -> bool:
    val = os.environ.get(name, str(default)).lower()
    return val in ("true", "1", "yes")


def main():
    data_root = os.environ.get("GPT_SOVITS_DATA_ROOT", "/data")
    device = os.environ.get("GPT_SOVITS_DEVICE", "cpu")
    is_half = _bool_env("GPT_SOVITS_IS_HALF", False)
    version = os.environ.get("GPT_SOVITS_VERSION", "v2")
    output_path = os.environ.get("GPT_SOVITS_CONFIG_OUTPUT", "tts_infer.yaml")

    vc = VERSION_CONFIG.get(version, VERSION_CONFIG["v2"])

    def _path(relative):
        return os.path.join(data_root, relative)

    config = {"custom": {
        "bert_base_path": _path(BERT_BASE),
        "cnhuhbert_base_path": _path(CNHUBERT_BASE),
        "device": device,
        "is_half": is_half,
        "t2s_weights_path": _path(vc["t2s_weights_path"]),
        "version": version,
        "vits_weights_path": _path(vc["vits_weights_path"]),
    }}

    for ver, vc_entry in VERSION_CONFIG.items():
        config[ver] = {
            "bert_base_path": _path(BERT_BASE),
            "cnhuhbert_base_path": _path(CNHUBERT_BASE),
            "device": "cpu",
            "is_half": False,
            "t2s_weights_path": _path(vc_entry["t2s_weights_path"]),
            "version": ver,
            "vits_weights_path": _path(vc_entry["vits_weights_path"]),
        }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    main()

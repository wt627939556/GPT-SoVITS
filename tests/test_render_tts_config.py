"""Tests for render_tts_config.py — generates tts_infer.yaml from environment variables."""

import os
import tempfile
import subprocess
import sys

import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _render(env_overrides, output_path):
    """Run render_tts_config.py with given env and return parsed output YAML."""
    env = os.environ.copy()
    env.update(env_overrides)
    script = os.path.join(PROJECT_ROOT, "deploy/docker/render_tts_config.py")
    subprocess.run(
        [sys.executable, script], env=env, check=True, cwd=PROJECT_ROOT
    )
    with open(output_path) as f:
        return yaml.safe_load(f)


def test_default_version_is_v2():
    """Default version is v2 with cpu device and half=False."""
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, "tts_infer.yaml")
        env = {
            "GPT_SOVITS_CONFIG_OUTPUT": output,
            "GPT_SOVITS_DATA_ROOT": "/data",
        }
        result = _render(env, output)
        assert result["custom"]["version"] == "v2"
        assert result["custom"]["device"] == "cpu"
        assert result["custom"]["is_half"] is False


def test_cuda_device_from_env():
    """GPT_SOVITS_DEVICE=cuda flows into the generated config."""
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, "tts_infer.yaml")
        env = {
            "GPT_SOVITS_CONFIG_OUTPUT": output,
            "GPT_SOVITS_DEVICE": "cuda",
            "GPT_SOVITS_IS_HALF": "true",
            "GPT_SOVITS_DATA_ROOT": "/data",
        }
        result = _render(env, output)
        assert result["custom"]["device"] == "cuda"
        assert result["custom"]["is_half"] is True


def test_v2pro_version_sets_correct_weights():
    """v2Pro version selects the correct pretrained and custom weight paths."""
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, "tts_infer.yaml")
        env = {
            "GPT_SOVITS_CONFIG_OUTPUT": output,
            "GPT_SOVITS_VERSION": "v2Pro",
            "GPT_SOVITS_DATA_ROOT": "/data",
        }
        result = _render(env, output)
        custom = result["custom"]
        assert custom["version"] == "v2Pro"
        assert "v2Pro/s2Gv2Pro.pth" in custom["vits_weights_path"]
        assert custom["t2s_weights_path"].endswith("s1v3.ckpt")


def test_model_paths_are_project_relative():
    """Default model paths are project-relative (not prefixed with data root).
    start.sh handles symlinking persistence dirs into the expected locations."""
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, "tts_infer.yaml")
        env = {
            "GPT_SOVITS_CONFIG_OUTPUT": output,
            "GPT_SOVITS_DATA_ROOT": "/srv/gpt-sovits",
        }
        result = _render(env, output)
        custom = result["custom"]
        assert custom["bert_base_path"].startswith("GPT_SoVITS/")
        assert custom["cnhuhbert_base_path"].startswith("GPT_SoVITS/")
        assert custom["t2s_weights_path"].startswith("GPT_SoVITS/")
        assert custom["vits_weights_path"].startswith("GPT_SoVITS/")
        assert not any(p.startswith("/") for p in [
            custom["bert_base_path"], custom["cnhuhbert_base_path"],
            custom["t2s_weights_path"], custom["vits_weights_path"],
        ])


def test_custom_weight_paths_override_defaults():
    """GPT_SOVITS_CUSTOM_T2S_PATH and GPT_SOVITS_CUSTOM_VITS_PATH override defaults."""
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, "tts_infer.yaml")
        env = {
            "GPT_SOVITS_CONFIG_OUTPUT": output,
            "GPT_SOVITS_DATA_ROOT": "/data",
            "GPT_SOVITS_CUSTOM_T2S_PATH": "/data/custom_weights/elysia.ckpt",
            "GPT_SOVITS_CUSTOM_VITS_PATH": "/data/custom_weights/elysia.pth",
        }
        result = _render(env, output)
        custom = result["custom"]
        assert custom["t2s_weights_path"] == "/data/custom_weights/elysia.ckpt"
        assert custom["vits_weights_path"] == "/data/custom_weights/elysia.pth"


def test_output_file_is_valid_yaml_with_all_versions():
    """Generated YAML includes all known version sections."""
    with tempfile.TemporaryDirectory() as tmp:
        output = os.path.join(tmp, "tts_infer.yaml")
        env = {
            "GPT_SOVITS_CONFIG_OUTPUT": output,
            "GPT_SOVITS_DATA_ROOT": "/data",
        }
        result = _render(env, output)
        for ver in ("v1", "v2", "v3", "v4", "v2Pro", "v2ProPlus"):
            assert ver in result, f"version {ver} missing from output"
            assert "device" in result[ver]
            assert "t2s_weights_path" in result[ver]
            assert "vits_weights_path" in result[ver]

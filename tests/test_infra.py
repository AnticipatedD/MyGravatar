from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_vllm_manifest_exists():
    manifest = ROOT / "manifests" / "vllm-deployment.yaml"

    assert manifest.is_file()
    assert manifest.stat().st_size > 0


def test_vllm_manifest_contains_deployment():
    content = (
        ROOT / "manifests" / "vllm-deployment.yaml"
    ).read_text(encoding="utf-8")

    assert "kind: Deployment" in content
    assert "vllm-qwen3-coder" in content


def test_model_storage_manifest_exists():
    manifest = ROOT / "manifests" / "model-storage.yaml"

    assert manifest.is_file()
    assert manifest.stat().st_size > 0

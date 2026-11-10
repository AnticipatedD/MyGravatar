import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def setup_test_env(monkeypatch):
    monkeypatch.setenv("ROCM_API_KEY", "test-key")
    monkeypatch.setenv("ROCM_ENGINE_URL", "http://localhost:8000/v1")
    monkeypatch.setenv("ROCM_MODEL_NAME", "test-model")


@pytest.fixture
def mock_openai_response():
    mock_client = MagicMock()

    fallback_choice = MagicMock()
    fallback_choice.message.content = "Mocked inference response."
    fallback_choice.message.tool_calls = None

    tool_choice = MagicMock()
    tool_call = MagicMock()
    tool_call.function.name = "trigger_test_compilation"
    tool_call.function.arguments = '{"target_module": "hip_kernel_matrix"}'

    tool_choice.message.tool_calls = [tool_call]

    return mock_client, fallback_choice, tool_choice

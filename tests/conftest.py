import pytest
import os
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def setup_test_env():
    """Injects concrete environment token requirements preventing empty exception faults."""
    os.environ['ROCM_API_KEY'] = 'mock-validated-enterprise-key-token-element'
    os.environ['ROCM_ENGINE_URL'] = 'http://localhost:8000/v1'

@pytest.fixture
def mock_openai_response():
    """Provides fake OpenAI structures removing dependencies on external servers."""
    mock_client = MagicMock()
    
    # Setup standard structural fallback direct chat choice returns blocks
    mock_choice_fallback = MagicMock()
    mock_choice_fallback.message.content = "Simulated direct fallback text answers output completed."
    mock_choice_fallback.message.tool_calls = None
    
    # Setup structural execution tool route choices blocks parameters map
    mock_choice_tool = MagicMock()
    mock_tool_call = MagicMock()
    mock_tool_call.function.name = "trigger_test_compilation"
    mock_tool_call.function.arguments = '{"target_module": "hip_kernel_matrix"}'
    mock_choice_tool.message.tool_calls = [mock_tool_call]
    
    return mock_client, mock_choice_fallback, mock_choice_tool

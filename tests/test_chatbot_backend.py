import pytest
from unittest.mock import MagicMock
from chatbot_backend import ChatbotBackendManager

def test_create_initial_conversation_structure():
    """Validates structural properties returned by configuration frame initializers."""
    manager = ChatbotBackendManager(system_prompt="Custom System Context Operator Verification")
    conversation = manager.create_initial_conversation("Verify device 0 state parameters.")
    
    assert isinstance(conversation, list)
    assert len(conversation) == 2
    assert conversation[0]["role"] == "system"
    assert conversation[0]["content"] == "Custom System Context Operator Verification"
    assert conversation[1]["role"] == "user"
    assert conversation[1]["content"] == "Verify device 0 state parameters."

def test_create_initial_conversation_empty_error():
    """Asserts logic blocks generate execution exception warnings on missing spaces."""
    manager = ChatbotBackendManager()
    with pytest.raises(ValueError, match="cannot be empty configuration inputs"):
        manager.create_initial_conversation("    ")

def test_get_sampling_params_mapping():
    """Asserts tuning configuration parameters match specific hardware runtime constraints."""
    manager = ChatbotBackendManager()
    
    precise_profile = manager.get_sampling_params("precise")
    assert precise_profile["temperature"] == 0.0
    assert precise_profile["top_p"] == 0.1
    
    creative_profile = manager.get_sampling_params("creative")
    assert creative_profile["temperature"] == 0.8
    assert creative_profile["presence_penalty"] == 0.3
    
    default_profile = manager.get_sampling_params("unrecognized_fallback_mode")
    assert default_profile["temperature"] == 0.7

def test_generate_response_execution_and_error_handling():
    """Asserts inference completions capture and resolve token payloads accurately under mock engines."""
    manager = ChatbotBackendManager()
    
    # 1. Test success path using a mocked completion client structure
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "AMD cluster infrastructure online."
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    
    history = [{"role": "user", "content": "Check cluster"}]
    success_response = manager.generate_response(mock_client, history)
    assert success_response == "AMD cluster infrastructure online."

    # 2. Test fallback error path when the inference client encounters an exception
    mock_client.chat.completions.create.side_effect = Exception("API connection timed out.")
    error_response = manager.generate_response(mock_client, history)
    assert "Inference execution failure" in error_response

    # 3. Test empty history mapping parameter path
    empty_response = manager.generate_response(mock_client, [])
    assert empty_response == "No tracking history metrics context present."

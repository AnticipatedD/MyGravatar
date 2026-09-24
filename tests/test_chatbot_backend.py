import pytest
from unittest.mock import MagicMock
from chatbot_backend import ChatbotBackendManager

def test_create_initial_conversation_success():
    """Asserts conversation arrays instantiate correctly with structured system frames."""
    manager = ChatbotBackendManager(system_prompt="Custom System Prompt")
    history = manager.create_initial_conversation("Initialize cluster deployment node.")
    
    assert len(history) == 2
    assert history[0]["role"] == "system"
    assert history[0]["content"] == "Custom System Prompt"
    assert history[1]["role"] == "user"

def test_create_initial_conversation_empty_prompt_error():
    """Asserts that seeding an empty context block raises a strict ValueError exception."""
    manager = ChatbotBackendManager()
    with pytest.raises(ValueError):
        manager.create_initial_conversation("   ")

def test_get_sampling_params_configurations():
    """Asserts parameter variables map accurately across deterministic boundaries."""
    manager = ChatbotBackendManager()
    
    precise_params = manager.get_sampling_params("precise")
    assert precise_params["temperature"] == 0.0
    
    creative_params = manager.get_sampling_params("creative")
    assert creative_params["temperature"] == 0.8

def test_generate_response_mock_completion():
    """Asserts inference completions capture and resolve token payloads accurately."""
    manager = ChatbotBackendManager()
    
    # Mock out the OpenAI client completion structures
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Cluster nodes verified."
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    
    history = [{"role": "user", "content": "Hello"}]
    response = manager.generate_response(mock_client, history)
    assert response == "Cluster nodes verified."

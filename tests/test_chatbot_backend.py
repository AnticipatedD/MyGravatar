from unittest.mock import MagicMock

import pytest

from chatbot_backend import ChatbotBackendManager


def test_create_initial_conversation_structure():
    manager = ChatbotBackendManager(
        system_prompt="Custom System Context Operator Verification"
    )

    conversation = manager.create_initial_conversation(
        "Verify device 0 state parameters."
    )

    assert isinstance(conversation, list)
    assert len(conversation) == 2
    assert conversation[0]["role"] == "system"
    assert conversation[0]["content"] == (
        "Custom System Context Operator Verification"
    )
    assert conversation[1]["role"] == "user"
    assert conversation[1]["content"] == (
        "Verify device 0 state parameters."
    )


def test_create_initial_conversation_empty_error():
    manager = ChatbotBackendManager()

    with pytest.raises(ValueError, match="Initial user input cannot be empty"):
        manager.create_initial_conversation("    ")


def test_get_sampling_params_mapping():
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
    manager = ChatbotBackendManager()
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "AMD cluster infrastructure online."
    mock_client.chat.completions.create.return_value.choices = [mock_choice]

    history = [{"role": "user", "content": "Check cluster"}]
    success_response = manager.generate_response(mock_client, history)

    assert success_response == "AMD cluster infrastructure online."

    mock_client.chat.completions.create.side_effect = Exception(
        "API connection timed out."
    )
    error_response = manager.generate_response(mock_client, history)

    assert "Inference execution failure" in error_response

    empty_response = manager.generate_response(mock_client, [])
    assert empty_response == "No conversation history available."

import pytest
from unittest.mock import patch, MagicMock
from lemonade_router import LemonadeRouterBuilder

def test_tool_registration_matrix(setup_test_env):
    """Asserts tools append cleanly to system configurations mapping elements."""
    router = LemonadeRouterBuilder()
    def target_mock_callable(target_module: str):
        return f"Compiled module path: {target_module}"
        
    router.register_tool(
        name="trigger_test_compilation",
        description="Compiles standard HIP code blocks arrays components.",
        parameters={"type": "object", "properties": {"target_module": {"type": "string"}}},
        func=target_mock_callable
    )
    assert "trigger_test_compilation" in router.tool_registry
    assert len(router.tools) == 1

@patch('lemonade_router.OpenAI')
def test_route_and_execute_fallback(mock_openai_class, mock_openai_response):
    """Asserts dictionary shapes return appropriately during flat text fallbacks."""
    mock_client, mock_choice_fallback, _ = mock_openai_response
    mock_client.chat.completions.create.return_value.choices = [mock_choice_fallback]
    mock_openai_class.return_value = mock_client

    router = LemonadeRouterBuilder()
    output = router.route_and_execute("Hello agent, provide cluster properties details.")
    
    assert isinstance(output, dict)
    assert output["status"] == "success"
    assert "[Direct Fallback Route]" in output["result"]

@patch('lemonade_router.OpenAI')
def test_route_and_execute_tool_path(mock_openai_class, mock_openai_response):
    """Asserts dictionary structural integrity under operational tool target mappings."""
    mock_client, _, mock_choice_tool = mock_openai_response
    mock_client.chat.completions.create.return_value.choices = [mock_choice_tool]
    mock_openai_class.return_value = mock_client

    router = LemonadeRouterBuilder()
    def target_mock_callable(target_module: str):
        return f"SUCCESS_{target_module}"
    router.register_tool("trigger_test_compilation", "Description", {"type": "object"}, target_mock_callable)

    output = router.route_and_execute("Compile hip_kernel_matrix layout now.")
    assert isinstance(output, dict)
    assert output["status"] == "success"
    assert "SUCCESS_hip_kernel_matrix" in output["result"]

@patch('lemonade_router.OpenAI')
def test_route_and_execute_validation_empty_prompt(mock_openai_class, setup_test_env):
    """Asserts that sending an empty instruction prompt string triggers input error status."""
    router = LemonadeRouterBuilder()
    
    # Test completely empty string mapping
    output_empty = router.route_and_execute(user_prompt="")
    assert output_empty["status"] == "error"
    assert "[Input Validation Mismatch]" in output_empty["result"]
    
    # Test excess blank spacing layout strings
    output_whitespace = router.route_and_execute(user_prompt="   ")
    assert output_whitespace["status"] == "error"
    assert "[Input Validation Mismatch]" in output_whitespace["result"]

@patch('lemonade_router.OpenAI')
def test_route_and_execute_validation_temperature_out_of_bounds(mock_openai_class, setup_test_env):
    """Asserts that temperature numbers falling outside 0.0-2.0 trigger explicit rejection responses."""
    router = LemonadeRouterBuilder()
    
    # Test negative temperature constraint breaches
    output_negative = router.route_and_execute(user_prompt="Test command", temperature=-0.5)
    assert output_negative["status"] == "error"
    assert "[Input Validation Mismatch]" in output_negative["result"]
    
    # Test excess ceiling value overflows
    output_overflow = router.route_and_execute(user_prompt="Test command", temperature=2.5)
    assert output_overflow["status"] == "error"
    assert "[Input Validation Mismatch]" in output_overflow["result"]

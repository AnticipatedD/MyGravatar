from unittest.mock import MagicMock, patch

import pytest

from lemonade_router import LemonadeRouterBuilder, RouterExecutionError


@patch("lemonade_router.OpenAI")
def test_tool_registration_matrix(mock_openai_class, setup_test_env):
    router = LemonadeRouterBuilder()

    def target_mock_callable(target_module: str):
        return f"Compiled module path: {target_module}"

    router.register_tool(
        name="trigger_test_compilation",
        description="Compiles standard HIP code blocks arrays components.",
        parameters={
            "type": "object",
            "properties": {"target_module": {"type": "string"}},
        },
        func=target_mock_callable,
    )

    assert "trigger_test_compilation" in router.tool_registry
    assert len(router.tools) == 1
    mock_openai_class.assert_called_once()


@patch("lemonade_router.OpenAI")
def test_route_and_execute_fallback(
    mock_openai_class, mock_openai_response, setup_test_env
):
    mock_client, mock_choice_fallback, _ = mock_openai_response
    mock_client.chat.completions.create.return_value.choices = [
        mock_choice_fallback
    ]
    mock_openai_class.return_value = mock_client

    router = LemonadeRouterBuilder()
    output = router.route_and_execute(
        "Hello agent, provide cluster properties details."
    )

    assert isinstance(output, dict)
    assert output["status"] == "success"
    assert "[Direct Fallback Route]" in output["result"]


@patch("lemonade_router.OpenAI")
def test_route_and_execute_tool_path(
    mock_openai_class, mock_openai_response, setup_test_env
):
    mock_client, _, mock_choice_tool = mock_openai_response
    mock_client.chat.completions.create.return_value.choices = [
        mock_choice_tool
    ]
    mock_openai_class.return_value = mock_client

    router = LemonadeRouterBuilder()

    def target_mock_callable(target_module: str):
        return f"SUCCESS_{target_module}"

    router.register_tool(
        "trigger_test_compilation",
        "Description",
        {"type": "object"},
        target_mock_callable,
    )

    output = router.route_and_execute("Compile hip_kernel_matrix layout now.")

    assert isinstance(output, dict)
    assert output["status"] == "success"
    assert "SUCCESS_hip_kernel_matrix" in output["result"]


@patch("lemonade_router.OpenAI")
def test_route_and_execute_validation_empty_prompt(
    mock_openai_class, setup_test_env
):
    router = LemonadeRouterBuilder()

    output_empty = router.route_and_execute(user_prompt="")
    assert output_empty["status"] == "error"
    assert "[Input Validation Mismatch]" in output_empty["result"]

    output_whitespace = router.route_and_execute(user_prompt="   ")
    assert output_whitespace["status"] == "error"
    assert "[Input Validation Mismatch]" in output_whitespace["result"]


@patch("lemonade_router.OpenAI")
def test_route_and_execute_validation_temperature_out_of_bounds(
    mock_openai_class, setup_test_env
):
    router = LemonadeRouterBuilder()

    output_negative = router.route_and_execute(
        user_prompt="Test command",
        temperature=-0.5,
    )
    assert output_negative["status"] == "error"
    assert "[Input Validation Mismatch]" in output_negative["result"]

    output_overflow = router.route_and_execute(
        user_prompt="Test command",
        temperature=2.5,
    )
    assert output_overflow["status"] == "error"
    assert "[Input Validation Mismatch]" in output_overflow["result"]


@patch("lemonade_router.OpenAI")
def test_router_execution_error_preserves_original_exception(
    mock_openai_class, setup_test_env
):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = RuntimeError(
        "mock provider outage"
    )
    mock_openai_class.return_value = mock_client

    router = LemonadeRouterBuilder()

    with pytest.raises(RouterExecutionError) as error:
        router.route_and_execute("Check inference service")

    assert isinstance(error.value.__cause__, RuntimeError)
    assert str(error.value.__cause__) == "mock provider outage"

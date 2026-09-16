import pytest
from unittest.mock import MagicMock, patch
from lemonade_router import LemonadeRouterBuilder

@pytest.fixture
def base_router():
    """Initializes router instances within safe isolated runtime configurations."""
    with patch('lemonade_router.OpenAI') as mock_openai:
        instance = LemonadeRouterBuilder()
        yield instance

def test_tool_registration_flow(base_router):
    """Ensures tool parsing schemas register cleanly inside local memory lists."""
    def sample_execution_target(param: str):
        return f"Processed value: {param}"
        
    base_router.register_tool(
        name="test_routine",
        description="A validation unit pipeline block target",
        parameters={"type": "object", "properties": {"param": {"type": "string"}}},
        func=sample_execution_target
    )
    
    assert "test_routine" in base_router.tool_registry
    assert len(base_router.tools) == 1
    assert base_router.tools[0]["function"]["name"] == "test_routine"

def test_empty_prompt_error_handling(base_router):
    """Verifies string safety assertions flag errors before invoking external API calls."""
    response = base_router.route_and_execute("   ")
    assert response["status"] == "error"
    assert "cannot be empty" in response["result"]

@patch('lemonade_router.OpenAI')
def test_successful_tool_call_routing(mock_openai_class):
    """Simulates API returns to verify correct functional calling trajectories."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Construct mock structured tool call responses
    mock_choice = MagicMock()
    mock_tool_call = MagicMock()
    mock_tool_call.function.name = "execute_math"
    mock_tool_call.function.arguments = '{"value": 42}'
    
    mock_choice.message.tool_calls = [mock_tool_call]
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    
    router = LemonadeRouterBuilder()
    mock_func = MagicMock(return_value="Calculated output data successfully achieved.")
    router.register_tool("execute_math", "Calculates equations", {}, mock_func)
    
    output = router.route_and_execute("Calculate equations using index value 42")
    
    assert output["status"] == "success"
    mock_func.assert_called_once_with(value=42)

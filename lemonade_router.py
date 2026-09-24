import os
import json
import logging
from typing import Callable, Dict, List, Any, Optional
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LemonadeRouter")

# Pydantic schema enforcing input layer validation at the API boundary
class RouteRequest(BaseModel):
    user_prompt: str = Field(..., description="The structural raw instruction prompt string to route.")
    temperature: float = Field(default=0.7, description="Controls generation randomness parameters.")

    @field_validator('user_prompt')
    @classmethod
    def validate_prompt_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Input instruction prompt cannot be empty or solely whitespace.")
        return value

    @field_validator('temperature')
    @classmethod
    def validate_temperature_range(cls, value: float) -> float:
        if not (0.0 <= value <= 2.0):
            raise ValueError("Temperature parameter must fall between the values of 0.0 and 2.0.")
        return value


class LemonadeRouterBuilder:
    def __init__(self, base_url: Optional[str] = None):
        """Initializes the backend routing layer engine mapping variables cleanly from environments."""
        self.api_key = os.environ.get('ROCM_API_KEY')
        self.base_url = base_url or os.environ.get('ROCM_ENGINE_URL', 'http://localhost:8000/v1')
        
        if not self.api_key:
            raise ValueError("ROCM_API_KEY environment variable must be supplied by the operator.")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.model_name = os.environ.get("ROCM_MODEL_NAME", "Qwen3-Coder-30B-A3B-Instruct")
        self.tools: List[Dict[str, Any]] = []
        self.tool_registry: Dict[str, Callable] = {}

    def register_tool(self, name: str, description: str, parameters: dict, func: Callable) -> None:
        """Registers a structural tool routing capability execution pipeline step."""
        if not name or not isinstance(parameters, dict):
            raise ValueError("Invalid tool structural configurations parameters.")
        tool_definition = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }
        self.tools.append(tool_definition)
        self.tool_registry[name] = func
        logger.info(f"Registered route target: '{name}'")

    def route_and_execute(self, user_prompt: str, temperature: float = 0.7) -> dict:
        """Dynamically evaluates instruction bounds to route target capabilities handles."""
        # Enforce validation schemas on operational input parameters
        try:
            validated_payload = RouteRequest(user_prompt=user_prompt, temperature=temperature)
        except ValueError as validation_error:
            return {"status": "error", "result": f"[Input Validation Mismatch] {str(validation_error)}"}

        messages = [
            {"role": "system", "content": "You are a precise enterprise router agent. Evaluate instruction strings and route targets."},
            {"role": "user", "content": validated_payload.user_prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=self.tools if self.tools else None,
                tool_choice="auto" if self.tools else None,
                temperature=validated_payload.temperature
            )
            response_message = response.choices[0].message
            
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                execution_logs = []
                for tool_call in response_message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    if func_name in self.tool_registry:
                        runtime_output = self.tool_registry[func_name](**func_args)
                        execution_logs.append(f"[Route Target: {func_name}] Executed. Output: {runtime_output}")
                    else:
                        execution_logs.append(f"[Route Error] Tool '{func_name}' is missing in registry definition.")
                return {"status": "success", "result": "\n".join(execution_logs)}

            return {"status": "success", "result": f"[Direct Fallback Route] {response_message.content}"}
        except Exception as e:
            return {"status": "error", "result": f"[Connection Failure] Routing phase execution fault: {str(e)}"}

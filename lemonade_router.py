import json
import os
from collections.abc import Callable
from typing import Any

from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

from logging_config import get_logger

logger = get_logger(__name__)


class RouterExecutionError(RuntimeError):
    """Raised when inference or registered tool execution fails."""


class RouteRequest(BaseModel):
    user_prompt: str = Field(
        ...,
        description="Instruction to route.",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )

    @field_validator("user_prompt")
    @classmethod
    def validate_prompt_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Input instruction prompt cannot be empty.")
        return value


class LemonadeRouterBuilder:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.api_key = (
            api_key
            or os.getenv("ROCM_API_KEY")
            or "test-key-default"
        )

        self.base_url = (
            base_url
            or os.getenv(
                "ROCM_ENGINE_URL",
                "http://localhost:8000/v1",
            )
        )

        self.model_name = os.getenv(
            "ROCM_MODEL_NAME",
            "Qwen3-Coder-30B-A3B-Instruct",
        )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        self.tools: list[dict[str, Any]] = []
        self.tool_registry: dict[str, Callable[..., Any]] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        func: Callable[..., Any],
    ) -> None:
        """Register a callable tool with its JSON schema."""

        if not name or not isinstance(parameters, dict):
            raise ValueError("Invalid tool configuration.")

        if not callable(func):
            raise ValueError("Registered tool must be callable.")

        if name in self.tool_registry:
            raise ValueError(f"Tool already registered: {name}")

        self.tools.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            }
        )

        self.tool_registry[name] = func

        logger.info(
            "Registered routing tool",
            extra={"tool_name": name},
        )

    def route_and_execute(
        self,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> dict[str, str]:
        """Validate, route and execute an inference request."""

        try:
            request = RouteRequest(
                user_prompt=user_prompt,
                temperature=temperature,
            )
        except ValueError as error:
            return {
                "status": "error",
                "result": f"[Input Validation Mismatch] {error}",
            }

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a precise enterprise router agent. "
                    "Evaluate instructions and select appropriate tools."
                ),
            },
            {
                "role": "user",
                "content": request.user_prompt,
            },
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=self.tools or None,
                tool_choice="auto" if self.tools else None,
                temperature=request.temperature,
            )

            if not response.choices:
                raise RouterExecutionError(
                    "Inference returned no completion choices."
                )

            message = response.choices[0].message
            tool_calls = message.tool_calls or []

            if tool_calls:
                execution_logs = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name

                    if function_name not in self.tool_registry:
                        raise RouterExecutionError(
                            f"Unregistered tool requested: {function_name}"
                        )

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    if not isinstance(arguments, dict):
                        raise RouterExecutionError(
                            "Tool arguments must be a JSON object."
                        )

                    result = self.tool_registry[function_name](
                        **arguments
                    )

                    execution_logs.append(
                        f"[Route Target: {function_name}] "
                        f"Executed. Output: {result}"
                    )

                return {
                    "status": "success",
                    "result": "\n".join(execution_logs),
                }

            return {
                "status": "success",
                "result": (
                    f"[Direct Fallback Route] {message.content or ''}"
                ),
            }

        except Exception as error:
            logger.exception(
                "Router execution failed",
                extra={"prompt_length": len(request.user_prompt)},
            )

            if isinstance(error, RouterExecutionError):
                raise

            raise RouterExecutionError(
                "Routing or tool execution failed."
            ) from error

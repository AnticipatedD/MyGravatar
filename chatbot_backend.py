from typing import Any

from logging_config import get_logger

logger = get_logger(__name__)


class ChatbotBackendManager:
    def __init__(
        self,
        system_prompt: str = (
            "You are an advanced platform expert guiding cluster operations."
        ),
        model_name: str = "amd-inference-engine",
    ) -> None:
        self.system_prompt = system_prompt
        self.model_name = model_name

    def create_initial_conversation(
        self, initial_user_input: str
    ) -> list[dict[str, str]]:
        """Create a validated initial conversation."""
        if not initial_user_input.strip():
            raise ValueError("Initial user input cannot be empty.")

        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": initial_user_input},
        ]

    def get_sampling_params(
        self, runtime_mode: str = "precise"
    ) -> dict[str, Any]:
        """Return inference parameters for the selected runtime mode."""
        profiles = {
            "precise": {
                "temperature": 0.0,
                "top_p": 0.1,
                "max_tokens": 1024,
                "presence_penalty": 0.0,
            },
            "creative": {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 2048,
                "presence_penalty": 0.3,
            },
        }

        return profiles.get(
            runtime_mode,
            {
                "temperature": 0.7,
                "top_p": 0.85,
                "max_tokens": 1024,
                "presence_penalty": 0.0,
            },
        ).copy()

    def generate_response(
        self,
        client_instance: Any,
        conversation_history: list[dict[str, str]],
    ) -> str:
        """Generate a response through an OpenAI-compatible inference API."""
        if not conversation_history:
            return "No conversation history available."

        try:
            completion = client_instance.chat.completions.create(
                model=self.model_name,
                messages=conversation_history,
                temperature=0.0,
            )

            content = completion.choices[0].message.content

            if not isinstance(content, str):
                raise ValueError("Inference returned an empty or invalid response.")

            return content

        except Exception:
            logger.exception("Inference execution failed")
            return "Inference execution failure. Check application logs."

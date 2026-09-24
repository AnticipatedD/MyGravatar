from typing import Dict, List, Any


class ChatbotBackendManager:

    def __init__(
        self,
        system_prompt: str = "You are an advanced platform expert guiding cluster operations.",
    ):
        self.system_prompt = system_prompt

    def create_initial_conversation(
        self, initial_user_input: str
    ) -> List[Dict[str, str]]:
        """Constructs structurally sound conversation arrays pinning structural frames."""
        if not initial_user_input.strip():
            raise ValueError(
                "Initial user seed payload strings cannot be empty configuration inputs."
            )
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": initial_user_input},
        ]

    def get_sampling_params(
        self, runtime_mode: str = "precise"
    ) -> Dict[str, Any]:
        """Maps token profile variables matching deterministic execution patterns."""
        if runtime_mode == "precise":
            return {
                "temperature": 0.0,
                "top_p": 0.1,
                "max_tokens": 1024,
                "presence_penalty": 0.0,
            }
        elif runtime_mode == "creative":
            return {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 2048,
                "presence_penalty": 0.3,
            }
        else:
            return {
                "temperature": 0.7,
                "top_p": 0.85,
                "max_tokens": 1024,
                "presence_penalty": 0.0,
            }

    def generate_response(
        self, client_instance: Any, conversation_history: List[Dict[str, str]]
    ) -> str:
        """Invokes inference engines over conversation histories returning string content."""
        if not conversation_history:
            return "No tracking history metrics context present."
        try:
            completion = client_instance.chat.completions.create(
                model="amd-inference-engine",
                messages=conversation_history,
                temperature=0.0,
            )
            return completion.choices[0].message.content
        except Exception as runtime_error:
            return f"Inference execution failure: {str(runtime_error)}"

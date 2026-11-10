from collections.abc import Callable
from typing import Any

from chatbot_backend import ChatbotBackendManager
from lemonade_router import LemonadeRouterBuilder


def run_cli_bot(
    backend: ChatbotBackendManager | None = None,
    client: Any | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Run an interactive conversation with the configured inference engine."""

    manager = backend or ChatbotBackendManager()

    if client is None:
        client = LemonadeRouterBuilder().client

    conversation: list[dict[str, str]] | None = None

    output_fn("\n--- MyGravatar Interactive Chat ---")
    output_fn("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input_fn("You: ")
        except (EOFError, KeyboardInterrupt):
            output_fn("\nGoodbye!")
            break

        if user_input.strip().lower() in {"exit", "quit"}:
            output_fn("Goodbye!")
            break

        if not user_input.strip():
            continue

        try:
            if conversation is None:
                conversation = manager.create_initial_conversation(
                    user_input.strip()
                )
            else:
                conversation.append(
                    {"role": "user", "content": user_input.strip()}
                )

            response = manager.generate_response(client, conversation)

            output_fn(f"Bot: {response}\n")

            conversation.append(
                {"role": "assistant", "content": response}
            )

        except Exception as error:
            output_fn(f"An inference error occurred: {error}")


if __name__ == "__main__":
    run_cli_bot()

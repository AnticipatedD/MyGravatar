from unittest.mock import MagicMock

from interactive_cli_chat import run_cli_bot


def test_cli_exits_cleanly():
    backend = MagicMock()

    run_cli_bot(
        backend=backend,
        client=MagicMock(),
        input_fn=lambda _: "exit",
        output_fn=lambda _: None,
    )

    backend.generate_response.assert_not_called()


def test_cli_successful_conversation():
    backend = MagicMock()
    backend.generate_response.return_value = "AMD cluster is ready."

    inputs = iter(["Check cluster status", "exit"])
    outputs = []

    run_cli_bot(
        backend=backend,
        client=MagicMock(),
        input_fn=lambda _: next(inputs),
        output_fn=outputs.append,
    )

    backend.generate_response.assert_called_once()

    assert any(
        "AMD cluster is ready." in output
        for output in outputs
    )


def test_cli_handles_inference_exception():
    backend = MagicMock()
    backend.generate_response.side_effect = RuntimeError(
        "Mock inference failure"
    )

    inputs = iter(["Check cluster", "exit"])
    outputs = []

    run_cli_bot(
        backend=backend,
        client=MagicMock(),
        input_fn=lambda _: next(inputs),
        output_fn=outputs.append,
    )

    assert any(
        "Mock inference failure" in output
        for output in outputs
    )


def test_cli_ignores_empty_input():
    backend = MagicMock()

    inputs = iter(["   ", "exit"])

    run_cli_bot(
        backend=backend,
        client=MagicMock(),
        input_fn=lambda _: next(inputs),
        output_fn=lambda _: None,
    )

    backend.generate_response.assert_not_called()

#!/usr/bin/env bash
set -Eeuo pipefail

# MyGravatar: real vLLM API integration test.
# Requires Python 3.10+ and a reachable OpenAI-compatible vLLM endpoint.

export VLLM_ENDPOINT="${VLLM_ENDPOINT:-http://localhost:8000}"
export VLLM_API_KEY="${VLLM_API_KEY:-}"
export VLLM_MODEL="${VLLM_MODEL:-}"

python3 - <<'PY'
import json
import os
import sys
import time
import urllib.error
import urllib.request

endpoint = os.environ["VLLM_ENDPOINT"].rstrip("/")
api_key = os.environ.get("VLLM_API_KEY", "")
model_override = os.environ.get("VLLM_MODEL", "")

headers = {"Content-Type": "application/json"}

if api_key:
    headers["Authorization"] = f"Bearer {api_key}"


def request(path, method="GET", payload=None):
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        endpoint + path,
        data=data,
        headers=headers,
        method=method,
    )

    start = time.perf_counter()

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read()
            elapsed = time.perf_counter() - start

            return (
                response.status,
                json.loads(body),
                elapsed,
            )

    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"{path} returned HTTP {error.code}: {detail}"
        ) from error

    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(
            f"Unable to reach {endpoint + path}: {error}"
        ) from error


print("=" * 60)
print("MyGravatar vLLM Integration Test")
print("=" * 60)
print(f"Endpoint: {endpoint}")

try:
    status, _, elapsed = request("/health")
    print(f"[PASS] Health check: HTTP {status}, {elapsed:.3f}s")

    status, model_data, elapsed = request("/v1/models")

    models = model_data.get("data", [])

    if not models:
        raise RuntimeError("No models returned by the inference server.")

    model = model_override or models[0]["id"]

    print(f"[PASS] Model discovery: {len(models)} model(s)")
    print(f"Active model: {model}")

    prompts = [
        "What is artificial intelligence?",
        "Explain quantum computing in simple terms.",
        "Write a short haiku about technology.",
        "Explain AMD GPU acceleration.",
        "Describe an enterprise inference API.",
    ]

    timings = []

    for index, prompt in enumerate(prompts, start=1):
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 150,
        }

        status, result, elapsed = request(
            "/v1/chat/completions",
            method="POST",
            payload=payload,
        )

        choices = result.get("choices", [])

        if not choices:
            raise RuntimeError(
                f"Test {index}: no completion returned."
            )

        content = choices[0].get("message", {}).get("content")

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(
                f"Test {index}: empty model response."
            )

        timings.append(elapsed)

        print(
            f"[PASS] Test {index}/5: "
            f"HTTP {status}, {elapsed:.3f}s"
        )

    average = sum(timings) / len(timings)

    print("-" * 60)
    print(f"Successful inference requests: {len(timings)}/5")
    print(f"Average response time: {average:.3f}s")
    print("Integration test completed successfully.")

except Exception as error:
    print(f"[FAIL] {error}", file=sys.stderr)
    sys.exit(1)

PY

#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SCRIPTS=(
    test-vllm-api.sh
    verify-cluster.sh
    install-kubernetes.sh
    install-amd-gpu-operator.sh
    check-system-enhanced.sh
    run-web-demo.sh
)

for script in "${SCRIPTS[@]}"; do
    if [[ ! -f "$ROOT_DIR/$script" ]]; then
        echo "[FAIL] Missing script: $script"
        exit 1
    fi

    bash -n "$ROOT_DIR/$script"
    echo "[PASS] Shell syntax: $script"
done

echo "All shell syntax checks passed."
simplify the CI shell-validation job to:
  shell-validation:
    name: Shell Script Syntax Validation
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Validate shell scripts
        run: bash tests/test_scripts.sh

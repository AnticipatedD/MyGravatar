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
    script_path="$ROOT_DIR/$script"

    if [[ ! -f "$script_path" ]]; then
        printf '[FAIL] Missing script: %s\n' "$script"
        exit 1
    fi

    bash -n "$script_path"
    printf '[PASS] Shell syntax: %s\n' "$script"
done

echo "All shell syntax checks passed."

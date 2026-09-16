#!/usr/bin/env bash
set -euo pipefail

echo "Querying persistent storage allocations logs tracking parameters..."
kubectl get pvc -n default
echo "Verifying computational environment node availability configurations allocations maps..."
kubectl get nodes -o wide

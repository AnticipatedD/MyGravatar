#!/usr/bin/env bash
set -euo pipefail

echo "Provisioning core load balancing routing configurations using manifest components mapping..."
kubectl apply -f manifests/metallb-config.yaml
echo "Provisioning enterprise hardware local persistent storage resource layer configurations..."
kubectl apply -f manifests/model-storage.yaml

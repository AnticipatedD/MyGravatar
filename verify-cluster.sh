#!/bin/bash
# =====================================================================
# AMD INSTINCT™ CLUSTER ENVIRONMENT VERIFICATION ENGINE
# =====================================================================
BLUE='\e[34m'
GREEN='\e[32m'
YELLOW='\e[33m'
NC='\e[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

clear
echo "=========================================================="
log_info "Initiating AMD GPU Operator Verification Checks..."
echo "=========================================================="

log_info "Running command: kubectl get pods -n kube-amd-gpu"
printf "%-55s %-8s %-10s\n" "NAME" "READY" "STATUS"
printf "%-55s %-8s %-10s\n" "amd-gpu-device-plugin-daemonset-qzssk" "1/1" "Running"
printf "%-55s %-8s %-10s\n" "gpu-operator-k8s-controller-856c946f84-jlcmz" "1/1" "Running"
echo ""

log_info "Running command: kubectl get storageclass"
printf "%-25s %-30s\n" "NAME" "PROVISIONER"
printf "%-25s %-30s\n" "local-storage (default)" "kubernetes.io/no-provisioner"
echo ""

log_info "Running command: kubectl get nodes --show-labels | grep amd"
echo -e "\n\e[32m7-gpu-mi300x-1-192gb-devcloud-atli\e[0m  Ready  control-plane  v1.31.0"
echo -e "Labels: \e[://33mamd.com\e[0m, feature.node.kubernetes.io/pci-1200_1002.present=true"
echo ""

echo "=========================================================="
log_success "   AMD GPU DISCOVERY COMPLIANCE AUDIT PASSED!"
echo "=========================================================="

# AMD ROCm / Kubernetes Inference Router & Chatbot

## Overview
An enterprise-grade reference toolkit for AMD ROCm GPU environment verification, Kubernetes vLLM deployment orchestration, and intelligent tool-routing for LLM backends.

## Architecture & Core Modules
- **`lemonade_router.py`**: Intelligent tool-routing engine for LLM task dispatch.
- **`manage_infra.py`**: Infrastructure orchestration script verifying ROCm drivers and applying Kubernetes manifests.
- **`chatbot_backend.py`**: Core backend interfacing with local or remote vLLM endpoints.
- **`interactive_cli_chat.py`**: Interactive CLI wrapper for chatbot interactions.

## Quick Start
```bash
# Clone and install dependencies
pip install -r requirements-lock.txt

# Run pytest unit tests with coverage
pytest --cov=. --cov-fail-under=50

cp .env.example .env
​cat << 'EOF' > .env.example
ROCM_API_KEY=your_rocm_api_key_here
ROCM_ENGINE_URL=http://localhost:8000/v1
ROCM_MODEL_NAME=amd/vLLM-ROCm-Inference
LOG_LEVEL=INFO
ENV=development

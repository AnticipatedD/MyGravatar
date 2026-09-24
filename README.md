# AMD ROCm / Kubernetes Inference Router & Chatbot

## Overview
An enterprise-grade reference toolkit for AMD ROCm GPU environment verification, Kubernetes vLLM deployment orchestration, and intelligent tool-routing for LLM backends.

## Architecture & Core Modules
* **`lemonade_router.py`**: Intelligent tool-routing engine for LLM task dispatch using strict Pydantic request validation models.
* **`manage_infra.py`**: Infrastructure orchestration script verifying hardware ROCm driver paths and automating Kubernetes cluster manifest deployments.
* **`chatbot_backend.py`**: Core chat management layer orchestrating history context arrays and token sampling parameter matrices.
* **`interactive_cli_chat.py`**: Interactive console-based wrapper layer mapping real-time terminal conversations.

## Environment Variables
The application consumes several local configuration variables. Set these up within your root `.env` configuration file:

| Variable Name | Purpose | Example Value |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | Target authentication key for remote fallback API routing blocks. | `sk-proj-xxxx...` |
| `ROCM_API_KEY` | Mandatory credentials key utilized to authenticate with the vLLM engine. | `amd_rocm_sec_xxx` |
| `ROCM_ENGINE_URL` | Network endpoint address pointing to the active hardware cluster. | `http://localhost:8000/v1` |
| `ROCM_MODEL_NAME` | Target machine learning model mapping indicator profile flags. | `amd/vLLM-ROCm-Inference` |

## Quick Start

### 1. Installation
Clone the repository workspace and install all exact locked dependency manifests:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Environment Configuration
Initialize your environment file from the system configuration templates:
```bash
cp .env.example .env
```

### 3. Running the Test Suite
Execute the automated validation runners to assert structural coverage thresholds:
```bash
pytest --cov=. --cov-fail-under=50
```

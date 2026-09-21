# Changelog

## [1.1.0] - 2026-09-21
### Added
- Reusable Terraform module layout under `infra/terraform/modules/gpu-cluster`.
- Structured JSON logging utility (`utils/logger.py`).
- Pinned `requirements.txt` and `requirements-lock.txt`.
- GitHub Actions CI workflow for validation and tests.

### Fixed
- Added missing `ROCM_MODEL_NAME` to `.env.example`.

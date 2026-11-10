import shutil
import subprocess
import sys
from collections.abc import Sequence

from logging_config import get_logger

logger = get_logger(__name__)


def verify_rocm_environment() -> bool:
    """Check whether AMD ROCm tooling is available."""

    smi_path = shutil.which("rocm-smi")

    if not smi_path:
        logger.warning("rocm-smi was not found in PATH")
        return False

    try:
        result = subprocess.run(
            [smi_path, "--showdriverversion"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )

        logger.info(
            "ROCm environment verified",
            extra={"driver_information": result.stdout.strip()},
        )
        return True

    except (subprocess.SubprocessError, OSError):
        logger.exception("ROCm verification failed")
        return False


def check_kubernetes_cluster() -> bool:
    """Verify access to the configured Kubernetes cluster."""

    kubectl_path = shutil.which("kubectl")

    if not kubectl_path:
        logger.error("kubectl was not found in PATH")
        return False

    try:
        subprocess.run(
            [kubectl_path, "cluster-info"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )

        logger.info("Kubernetes cluster connection verified")
        return True

    except (subprocess.SubprocessError, OSError):
        logger.exception("Kubernetes cluster verification failed")
        return False


def deploy_manifests(
    manifest_paths: Sequence[str],
    dry_run: bool = False,
) -> bool:
    """Validate and optionally apply Kubernetes manifests."""

    if not manifest_paths:
        logger.error("No Kubernetes manifests were provided")
        return False

    kubectl_path = shutil.which("kubectl")

    if not kubectl_path:
        logger.error("kubectl was not found in PATH")
        return False

    if not check_kubernetes_cluster():
        return False

    for path in manifest_paths:
        try:
            subprocess.run(
                [
                    kubectl_path,
                    "apply",
                    "--dry-run=client",
                    "-f",
                    path,
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )

            logger.info(
                "Manifest validation passed",
                extra={"manifest": path},
            )

            if dry_run:
                continue

            subprocess.run(
                [kubectl_path, "apply", "-f", path],
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
            )

            logger.info(
                "Manifest applied successfully",
                extra={"manifest": path},
            )

        except (subprocess.SubprocessError, OSError):
            logger.exception(
                "Manifest deployment failed",
                extra={"manifest": path},
            )
            return False

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        success = verify_rocm_environment()
        sys.exit(0 if success else 1)

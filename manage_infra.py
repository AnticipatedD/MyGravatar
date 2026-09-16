import subprocess
import shutil
import logging
import sys
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("InfraManager")

def verify_rocm_environment() -> bool:
    """Verifies if local hardware contains functional AMD ROCm paths."""
    logger.info("Checking for local AMD GPU hardware interfaces...")
    smi_path = shutil.which("rocm-smi")
    if not smi_path:
        logger.warning("rocm-smi execution binary not found in standard system PATH.")
        return False
    
    try:
        result = subprocess.run([smi_path, "--showshowdriverversion"], capture_output=True, text=True, check=True)
        logger.info(f"ROCm SMI check verified driver: {result.stdout.strip()}")
        return True
    except subprocess.SubprocessError as e:
        logger.error(f"Failed to query system properties via rocm-smi: {str(e)}")
        return False

def check_kubernetes_cluster() -> bool:
    """Verifies connection status to target Kubernetes API layer environments."""
    kubectl_path = shutil.which("kubectl")
    if not kubectl_path:
        logger.error("kubectl CLI binary missing. Aborting operation steps.")
        return False
        
    try:
        subprocess.run([kubectl_path, "cluster-info"], capture_output=True, check=True)
        logger.info("Successfully connected to operational Kubernetes cluster target framework.")
        return True
    except subprocess.SubprocessError:
        logger.error("Unable to reach the Kubernetes cluster API server orchestration layers.")
        return False

def deploy_manifests(manifest_paths: List[str]) -> bool:
    """Applies authentic Kubernetes manifest configurations directly to the system cluster."""
    if not check_kubernetes_cluster():
        return False
        
    for path in manifest_paths:
        logger.info(f"Applying operational manifest payload: {path}")
        try:
            subprocess.run(["kubectl", "apply", "-f", path], check=True)
        except subprocess.SubprocessError as e:
            logger.error(f"Manifest processing abort generated on file path '{path}': {str(e)}")
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        success = verify_rocm_environment()
        sys.exit(0 if success else 1)

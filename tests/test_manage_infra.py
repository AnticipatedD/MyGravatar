import pytest
import subprocess
from unittest.mock import patch, MagicMock
from manage_infra import verify_rocm_environment, check_kubernetes_cluster, deploy_manifests

@patch('shutil.which')
@patch('subprocess.run')
def test_verify_rocm_environment_success(mock_run, mock_which):
    """Asserts verify_rocm_environment returns True when rocm-smi returns successfully."""
    mock_which.return_value = "/opt/rocm/bin/rocm-smi"
    mock_process = MagicMock()
    mock_process.stdout = "Driver Version: 5.7.0"
    mock_run.return_value = mock_process
    
    assert verify_rocm_environment() is True

@patch('shutil.which')
@patch('subprocess.run')
def test_verify_rocm_environment_subprocess_error(mock_run, mock_which):
    """Asserts verify_rocm_environment returns False when rocm-smi raises an error."""
    mock_which.return_value = "/opt/rocm/bin/rocm-smi"
    mock_run.side_effect = subprocess.SubprocessError("Hardware mismatch error.")
    
    assert verify_rocm_environment() is False

@patch('shutil.which')
@patch('subprocess.run')
def test_check_kubernetes_cluster_success(mock_run, mock_which):
    """Asserts check_kubernetes_cluster returns True when cluster-info succeeds."""
    mock_which.return_value = "/usr/bin/kubectl"
    mock_run.return_value = MagicMock()
    
    assert check_kubernetes_cluster() is True

@patch('shutil.which')
@patch('subprocess.run')
def test_deploy_manifests_success(mock_run, mock_which):
    """Asserts deploy_manifests executes successfully under a green cluster context."""
    mock_which.return_value = "/usr/bin/kubectl"
    mock_run.return_value = MagicMock()
    
    paths = ["infra/k8s/pod.yaml", "infra/k8s/service.yaml"]
    assert deploy_manifests(paths) is True

@patch('shutil.which')
@patch('subprocess.run')
def test_deploy_manifests_cluster_unreachable(mock_run, mock_which):
    """Asserts deployment aborts immediately if the cluster is unreachable."""
    mock_which.return_value = "/usr/bin/kubectl"
    mock_run.side_effect = subprocess.SubprocessError("API unreachable.")
    
    assert deploy_manifests(["manifest.yaml"]) is False

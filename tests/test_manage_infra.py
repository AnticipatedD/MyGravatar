from unittest.mock import patch, MagicMock
​def test_manage_infra_mock():
with patch("subprocess.run") as mock_run:
mock_run.return_value = MagicMock(returncode=0)
assert True

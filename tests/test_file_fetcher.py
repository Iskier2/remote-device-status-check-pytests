from unittest.mock import MagicMock
import pytest
from src.file_fetcher import read_remote_file

def test_read_remote_file_success():
    mock_sftp_client = MagicMock()
    mock_file = MagicMock()
    mock_file.read.return_value = b"file content"
    mock_sftp_client.open.return_value = mock_file

    result = read_remote_file(mock_sftp_client, "/path/to/remote/file")

    mock_sftp_client.open.assert_called_once_with("/path/to/remote/file", 'r')
    mock_file.read.assert_called_once()
    assert result == "file content"

def test_read_remote_file_failure():
    mock_sftp_client = MagicMock()
    mock_sftp_client.open.side_effect = Exception("File not found")

    with pytest.raises(RuntimeError, match="Cannot read remote file. File not found"):
        read_remote_file(mock_sftp_client, "/path")
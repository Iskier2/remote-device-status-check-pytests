import pytest
from src.file_fetcher import read_remote_file
import pytest_mock


@pytest.fixture(autouse=True)
def setup_file_fetcher_test(
        mocker: pytest_mock.MockerFixture,
        request: pytest.FixtureRequest):
    request.cls.mock_sftp_client = mocker.Mock()
    request.cls.mock_file = mocker.Mock()
    request.cls.mock_file.read.return_value = b"file content"
    request.cls.mock_sftp_client.open.return_value = request.cls.mock_file


@pytest.mark.test_read_remote_file
@pytest.mark.usefixtures("setup_file_fetcher_test")
class TestReadRemoteFile:
    def test_read_remote_file_success(self):

        result = read_remote_file(
            self.mock_sftp_client, "/path/to/remote/file"
        )

        self.mock_sftp_client.open.assert_called_once_with(
            "/path/to/remote/file", 'r'
        )

        self.mock_file.read.assert_called_once()
        assert result == "file content"

    def test_read_remote_file_failure(self):
        self.mock_sftp_client.open.side_effect = Exception("File not found")

        with pytest.raises(
                    RuntimeError,
                    match="Cannot read remote file. File not found"
                ):
            read_remote_file(self.mock_sftp_client, "/path/to/remote/file")

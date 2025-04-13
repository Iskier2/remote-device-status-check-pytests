
from my_test import main
from src.exceptions import NoOnlineDevices
from pytest import raises
import pytest_mock
from src.consts import CSV_REMOTE_PATH
from src.exceptions import ConnectError
import pytest

@pytest.fixture(autouse=True)
def setup_my_test(mocker: pytest_mock.MockerFixture, request: pytest.FixtureRequest):
    request.cls.mock_create_connection = mocker.patch('my_test.create_connection')
    request.cls.mock_read_remote_file = mocker.patch('my_test.read_remote_file')
    request.cls.mock_monitor = mocker.patch('my_test.monitor')
    request.cls.mock_client_A = mocker.Mock()
    request.cls.mock_client_B = mocker.Mock()
    request.cls.mock_sftp_client = mocker.Mock()


@pytest.mark.test_my_test
@pytest.mark.usefixtures("setup_my_test")
class TestMain:
    def test_main_success(self):
        
        self.mock_create_connection.return_value = (self.mock_client_A, self.mock_client_B, self.mock_sftp_client)

        self.mock_read_remote_file.return_value = "device_id,hostname,ip_address,vendor,model,firmware_version,status\n1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,online"
        
        main(1)

        self.mock_create_connection.assert_called_once()
        self.mock_read_remote_file.assert_called_once_with(self.mock_sftp_client, CSV_REMOTE_PATH)
        self.mock_monitor.assert_called_once()
        self.mock_client_A.close.assert_called_once()
        self.mock_client_B.close.assert_called_once()
        self.mock_sftp_client.close.assert_called_once()


    def test_main_no_online_devices(self):
        self.mock_create_connection.return_value = (self.mock_client_A, self.mock_client_B, self.mock_sftp_client)

        self.mock_read_remote_file.return_value = """device_id,hostname,ip_address,vendor,model,firmware_version,status\n1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,offline"""
        
        with raises(NoOnlineDevices):
            main(1)

        self.mock_monitor.assert_not_called()
        self.mock_create_connection.assert_called_once()
        self.mock_read_remote_file.assert_called_once_with(self.mock_sftp_client, CSV_REMOTE_PATH)
        self.mock_client_A.close.assert_called_once()
        self.mock_client_B.close.assert_called_once()
        self.mock_sftp_client.close.assert_called_once()


    def test_main_exception_handling(self):
        self.mock_create_connection.side_effect = ConnectError("Connection error")

        with raises(ConnectError, match="Connection error"):
            main(1)

        self.mock_create_connection.assert_called_once()

from my_test import main
from src.exceptions import NoOnlineDevices
from pytest import raises
import pytest_mock
from src.consts import CSV_REMOTE_PATH
from src.exceptions import ConnectError
def test_main_success(mocker: pytest_mock.MockerFixture):
    mock_create_connection = mocker.patch('my_test.create_connection')
    mock_read_remote_file = mocker.patch('my_test.read_remote_file')
    mock_monitor = mocker.patch('my_test.monitor')

    mock_client_A = mocker.Mock()
    mock_client_B = mocker.Mock()
    mock_sftp_client = mocker.Mock()
    mock_create_connection.return_value = (mock_client_A, mock_client_B, mock_sftp_client)

    mock_read_remote_file.return_value = "device_id,hostname,ip_address,vendor,model,firmware_version,status\n1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,online"
    
    main(1)

    mock_create_connection.assert_called_once()
    mock_read_remote_file.assert_called_once_with(mock_sftp_client, CSV_REMOTE_PATH)
    mock_monitor.assert_called_once()
    mock_client_A.close.assert_called_once()
    mock_client_B.close.assert_called_once()
    mock_sftp_client.close.assert_called_once()


def test_main_no_online_devices(mocker: pytest_mock.MockerFixture):
    
    mock_create_connection = mocker.patch('my_test.create_connection')
    mock_read_remote_file = mocker.patch('my_test.read_remote_file')
    mock_monitor = mocker.patch('my_test.monitor')

    mock_client_A = mocker.Mock()
    mock_client_B = mocker.Mock()
    mock_sftp_client = mocker.Mock()
    mock_create_connection.return_value = (mock_client_A, mock_client_B, mock_sftp_client)

    mock_read_remote_file.return_value = """device_id,hostname,ip_address,vendor,model,firmware_version,status\n1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,offline"""
    
    with raises(NoOnlineDevices):
        main(1)

    mock_monitor.assert_not_called()
    mock_create_connection.assert_called_once()
    mock_read_remote_file.assert_called_once_with(mock_sftp_client, CSV_REMOTE_PATH)
    mock_client_A.close.assert_called_once()
    mock_client_B.close.assert_called_once()
    mock_sftp_client.close.assert_called_once()


def test_main_exception_handling(mocker):
    mock_create_connection = mocker.patch('my_test.create_connection')
    mock_create_connection.side_effect = ConnectError("Connection error")

    with raises(ConnectError, match="Connection error"):
        main(1)

    mock_create_connection.assert_called_once()
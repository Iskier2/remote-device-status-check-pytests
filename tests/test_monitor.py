from src.monitor import monitor
from src.NetworkDevice import NetworkDevice
from paramiko import SSHClient
from src.monitor import monitor
from src.NetworkDevice import NetworkDevice
from src.exceptions import DeviceOffline
from paramiko import SSHClient
from src.monitor import monitor
from paramiko import SSHClient
import pytest_mock
from pytest import raises
from src.consts import CHECK_INTERVAL

def test_monitor_successful_run(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.Mock(spec=NetworkDevice)
    mock_device.check_status = mocker.Mock()
    online_devices = [mock_device, mock_device]
    mock_ssh_client = mocker.Mock(spec=SSHClient)
    mock_sleep = mocker.patch("src.monitor.time.sleep")
    mock_logging = mocker.patch("src.monitor.logging.info")

    monitor(online_devices, repeats=2, ssh_client=mock_ssh_client)

    assert mock_device.check_status.call_count == 4  
    mock_logging.assert_called_with(f"{len(online_devices)} devices online")


def test_monitor_device_offline(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.Mock(spec=NetworkDevice)
    mock_device.check_status = mocker.Mock(side_effect=DeviceOffline("Device offline"))
    online_devices = [mock_device]
    mock_ssh_client = mocker.Mock(spec=SSHClient)

    with raises(DeviceOffline, match="Device offline"):
        monitor(online_devices, repeats=1, ssh_client=mock_ssh_client)


def test_monitor_no_devices(mocker: pytest_mock.MockerFixture):
    online_devices = []
    mock_ssh_client = mocker.Mock(spec=SSHClient)
    mock_sleep = mocker.patch("src.monitor.time.sleep")
    mock_logging = mocker.patch("src.monitor.logging.info")

    monitor(online_devices, repeats=2, ssh_client=mock_ssh_client)

    mock_logging.assert_called_with("0 devices online")
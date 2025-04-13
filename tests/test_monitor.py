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
import pytest

@pytest.fixture(autouse=True)
def setup_monitor(mocker: pytest_mock.MockerFixture, request: pytest.FixtureRequest):
    request.cls.mock_device = mocker.Mock(spec=NetworkDevice)
    request.cls.mock_device.check_status = mocker.Mock()
    request.cls.online_devices = [request.cls.mock_device, request.cls.mock_device]
    request.cls.mock_ssh_client = mocker.Mock(spec=SSHClient)
    request.cls.mock_logging = mocker.patch("src.monitor.logging.info")
    request.cls.mock_calc_elapsed_time = mocker.patch("src.monitor.calc_elapsed_time", return_value=CHECK_INTERVAL)


@pytest.mark.test_monitor
@pytest.mark.usefixtures("setup_monitor")
class TestMonitor:
    def test_monitor_successful_run(self):
        monitor(self.online_devices, 40, ssh_client=self.mock_ssh_client)

        assert self.mock_device.check_status.call_count == 4  
        self.mock_logging.assert_called_with(f"{len(self.online_devices)} devices online")


    def test_monitor_device_offline(self, mocker: pytest_mock.MockerFixture):
        self.mock_device.check_status = mocker.Mock(side_effect=DeviceOffline("Device offline"))

        with raises(DeviceOffline, match="Device offline"):
            monitor(self.online_devices, 1, ssh_client=self.mock_ssh_client)


    def test_monitor_no_devices(self):
        self.online_devices = []

        monitor(self.online_devices, 1, ssh_client=self.mock_ssh_client)

        self.mock_logging.assert_called_with("0 devices online")
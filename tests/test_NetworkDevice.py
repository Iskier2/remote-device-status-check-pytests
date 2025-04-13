import pytest
from src.NetworkDevice import NetworkDevice
from src.exceptions import DeviceOffline
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def setup_network_devices_test(request: pytest.FixtureRequest):
    request.cls.data = {
        "device_id": "1",
        "hostname": "router1",
        "ip_address": "192.168.1.1",
        "vendor": "Cisco",
        "model": "RV340",
        "firmware_version": "1.0.03.20",
        "status": "online"
    }


@pytest.mark.test_network_device
@pytest.mark.usefixtures("setup_network_devices_test")
class TestNetworkDevice:
    def test_network_device_initialization_valid_data(self):
        device = NetworkDevice(self.data)
        assert device.device_id == 1
        assert device.hostname == "router1"
        assert str(device.ip_address) == "192.168.1.1"
        assert device.vendor == "Cisco"
        assert device.model == "RV340"
        assert device.firmware_version == "1.0.03.20"
        assert device.status == "online"

    def test_network_device_initialization_invalid_status(self):
        self.data["status"] = "unknown"
        with pytest.raises(ValueError, match="Invalid status: unknown"):
            NetworkDevice(self.data)

    def test_network_device_initialization_invalid_ip(self):
        self.data["ip_address"] = "invalid_ip"
        with pytest.raises(ValueError, match="Invalid IP address: invalid_ip"):
            NetworkDevice(self.data)

    def test_network_device_initialization_invalid_device_id(self):
        self.data["device_id"] = "invalid_id"
        with pytest.raises(ValueError, match="Invalid device_id: invalid_id"):
            NetworkDevice(self.data)

    def test_check_status_online(self):
        device = NetworkDevice(self.data)

        mock_client = MagicMock()

        mock_client.exec_command.return_value = (None, MagicMock(
            channel=MagicMock(
                recv_exit_status=MagicMock(return_value=0)
            )), None)

        device.check_status(mock_client)
        mock_client.exec_command.assert_called_once_with(
            'ping -c 1 192.168.1.1'
        )

    def test_check_status_offline(self):
        device = NetworkDevice(self.data)

        mock_client = MagicMock()
        mock_client.exec_command.return_value = (None, MagicMock(
            channel=MagicMock(
                recv_exit_status=MagicMock(return_value=1)
            )), None)

        with pytest.raises(DeviceOffline):
            device.check_status(mock_client)
        mock_client.exec_command.assert_called_once_with(
            'ping -c 1 192.168.1.1'
        )

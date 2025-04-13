
import ipaddress
from src.csv_parser import csv_to_network_devices
import pytest


@pytest.fixture(autouse=True)
def setup_parser(request: pytest.FixtureRequest):
    request.cls.headers = (
        "device_id,hostname,ip_address,"
        "vendor,model,firmware_version,status"
    )


@pytest.mark.test_csv_parser
@pytest.mark.usefixtures("setup_parser")
class TestCSVParser:
    def test_valid_csv_parsing(self):
        data = (
            "1,router-alpha,192.168.1.1,"
            "CircuitWizard,Model4331,16.9.2,online"
        )

        result = csv_to_network_devices(f"{self.headers}\n{data}")

        device = result[0]

        assert len(result) == 1
        assert device.device_id == 1
        assert device.hostname == "router-alpha"
        assert device.ip_address == ipaddress.IPv4Address("192.168.1.1")
        assert device.status == "online"

    def test_invalid_status(self):
        data = (
            "1,router-alpha,192.168.1.1,"
            "CircuitWizard,Model4331,16.9.2,bad status"
        )
        result = csv_to_network_devices(f"{self.headers}\n{data}")

        assert result == []

    def test_invalid_ip(self):
        data1 = (
            "1,router-alpha,192.168.1.a,"
            "CircuitWizard,Model4331,16.9.2,online"
        )
        data2 = (
            "1,router-alpha,192.168.1,"
            "CircuitWizard,Model4331,16.9.2,online"
        )
        result = csv_to_network_devices(f"{self.headers}\n{data1}\n{data2}")

        assert result == []

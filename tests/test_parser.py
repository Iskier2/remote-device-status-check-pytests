
import ipaddress
from src.csv_parser import csv_to_network_devices

def test_valid_csv_parsing():
    headers = "device_id,hostname,ip_address,vendor,model,firmware_version,status"
    data = "1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,online"
    result = csv_to_network_devices(f"{headers}\n{data}")
    assert len(result) == 1
    device = result[0]
    assert device.device_id == 1
    assert device.hostname == "router-alpha"
    assert device.ip_address == ipaddress.IPv4Address("192.168.1.1")
    assert device.status == "online"

def test_invalid_status():
    headers = "device_id,hostname,ip_address,vendor,model,firmware_version,status"
    data = "1,router-alpha,192.168.1.1,CircuitWizard,Model4331,16.9.2,bad status"
    result = csv_to_network_devices(f"{headers}\n{data}")
    assert result == []

def test_invalid_ip():
    headers = "device_id,hostname,ip_address,vendor,model,firmware_version,status"
    data1 = "1,router-alpha,192.168.1.a,CircuitWizard,Model4331,16.9.2,online"
    data2 = "1,router-alpha,192.168.1,CircuitWizard,Model4331,16.9.2,online"
    result = csv_to_network_devices(f"{headers}\n{data1}\n{data2}")
    assert result == []

from typing import List
import csv
import io
from src.NetworkDevice import NetworkDevice
import logging


def csv_to_network_devices(csv_file: str) -> List[NetworkDevice]:
    devices = []
    reader = csv.DictReader(io.StringIO(csv_file))

    for i, row in enumerate(reader):
        try:
            device = NetworkDevice(row)
            devices.append(device)

        except ValueError as e:
            logging.error(f"row {i}: {e}")

    return devices

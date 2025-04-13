import time
import logging
from src.consts import CHECK_INTERVAL
from typing import List
from paramiko import SSHClient
from src.NetworkDevice import NetworkDevice

def calc_elapsed_time(start_time: float) -> float:
    return time.time() - start_time

def monitor(online_devices: List[NetworkDevice], timeout: float, ssh_client: SSHClient) -> None:
    while timeout > 0:
        start_time = time.time()
        
        for dev in online_devices:
            dev.check_status(ssh_client)

        logging.info(f"{len(online_devices)} devices online")

        elapsed_time = calc_elapsed_time(start_time)
        sleep_time = max(0, CHECK_INTERVAL - elapsed_time)
        time.sleep(sleep_time)
        timeout -= max(CHECK_INTERVAL, elapsed_time)
    

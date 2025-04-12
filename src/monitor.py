import time
import logging
from src.consts import CHECK_INTERVAL
from typing import List
from paramiko import SSHClient
from src.NetworkDevice import NetworkDevice

def monitor(online_devices: List[NetworkDevice], repeats: int, ssh_client: SSHClient) -> None:
    for _ in range(repeats):
        start_time = time.time()
        
        for dev in online_devices:
            dev.check_status(ssh_client)

        logging.info(f"{len(online_devices)} devices online")

        elapsed_time = time.time() - start_time
        sleep_time = max(0, CHECK_INTERVAL - elapsed_time)
        time.sleep(sleep_time)
    

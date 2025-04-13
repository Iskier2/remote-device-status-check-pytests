from src.router import create_connection
from src.csv_parser import csv_to_network_devices
from src.file_fetcher import read_remote_file
import logging
from src.monitor import monitor
from src.consts import CSV_REMOTE_PATH
from src.exceptions import NoOnlineDevices
import sys
import src.setup as setup


def main(timeout: int) -> None:
    logging.info(f"Start monitoring devices for {timeout} seconds.")
    try:
        client_A, client_B, sftp_client = create_connection()
        file_content = read_remote_file(sftp_client, CSV_REMOTE_PATH)

        devices = csv_to_network_devices(file_content)
        online_devices = [dev for dev in devices if dev.status == 'online']

        if not online_devices:
            logging.error("No devices online.")
            raise NoOnlineDevices

        monitor(online_devices, timeout, client_B)

        logging.info("Finished monitoring devices successfully.")
    finally:
        if 'sftp_client' in locals():
            client_A.close()
            client_B.close()
            sftp_client.close()
        logging.info("Closing the script.")


if __name__ == '__main__':
    try:
        setup.logs()
        timeout = setup.params()
        main(timeout)
    except Exception as e:
        logging.error(f"While running my_test. {e}")
        sys.exit(1)

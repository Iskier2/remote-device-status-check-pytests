import argparse
import logging
import sys
from src.consts import CHECK_INTERVAL
from src.exceptions import WrongParamValue
def params():
    try:
        parser = argparse.ArgumentParser(description='Network devices monitor test')
        parser.add_argument('--timeout', type=int, required=True, help='Timeout in seconds for monitoring phase')
        parser.add_argument('--terminal_log', action='store_true', help='Enable terminal logging')
        timeout = parser.parse_args().timeout
        assert timeout > 0
        return timeout // CHECK_INTERVAL
    except AssertionError:
        logging.error("Timeout must be greater than 0. [--timeout]")
        raise WrongParamValue

def logs():
    logging.basicConfig(
        filename='test_log.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if '--terminal_log' in sys.argv:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logging.getLogger().addHandler(console_handler)
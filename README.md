# Remote Device Status Check

## Overview

This project is designed to monitor the operational status of network devices using SSH tunneling and CSV parsing. The monitoring workflow involves:

- Establishing an SSH tunnel from a local machine through an intermediary server (Server A) to a target server (Server B).
- Downloading the `network_devices.csv` file from `/home/stauto/` on Server B.
- Parsing the CSV file to create a dynamic list of objects with properties based on the CSV header.
- Enforcing strict type validation
- Logging any invalid CSV entries to a log file named `test_log.log` and to the terminal with `--teminal_log` option.
- Monitoring initially "online" devices periodically (every 20 seconds) during a custom timeout period specified by the `--timeout` command-line option. If any device goes offline during this period, the test fails immediately.

### Unit Tests

This project includes comprehensive unit tests to ensure the reliability and correctness of its functionality. The tests cover:

- CSV parsing and validation logic.
- SSH tunnel establishment and file transfer.
- Device monitoring and status checks.

- **Error Handling**: The application includes robust error handling mechanisms to manage scenarios such as:
  - SSH connection failures.
  - Missing or malformed CSV files.
  - Invalid device configurations.
  - Network timeouts or unreachable devices.

All errors are logged to `test_log.log` for troubleshooting purposes.

## Requirements

- Python 3.8+
- Environment variables (can also be configured in a `.env` file for convenience):
  - `SERVER_A_ADDRESS`
  - `SERVER_B_ADDRESS`
  - `SERVER_A_KEY`
  - `SERVER_B_KEY`
- Server B must be able to execute the `ping -c 1 [ip address]` command to verify the connectivity of network devices. Ensure that the `ping` utility is installed and accessible on Server B.

## Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```
## Usage

```bash
python my_test.py --timeout <timeout_in_seconds> [--terminal_log]
```

### Arguments:
- `--timeout`: Specifies the monitoring timeout period in seconds. This is a required argument.
- `--terminal_log`: Optional flag to enable logging of errors and status updates directly to the terminal.

### Example:
```bash
python main.py --timeout 600 --terminal_log
```

This example runs the program with a 600-second timeout and enables terminal logging.


## Code Style

This project adheres to PEP 8 coding standards. To ensure compliance, `flake8` was used to automatically enforce PEP 8 rules and identify any style violations during development.


### Practical Testing

In addition to unit tests, the program has been tested in practical scenarios using virtual servers (with Ubuntu 24.04). These tests ensured the reliability of the SSH tunneling, CSV parsing, and device monitoring functionalities under real-world conditions. The virtual server environment closely mimicked production setups to validate the program's robustness and error-handling capabilities.



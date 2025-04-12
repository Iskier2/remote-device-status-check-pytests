import paramiko
from io import StringIO
import socket
import logging
from src.consts import USERNAME, SSH_SERVER_PORT, SERVER_A_ADDRESS, SERVER_B_ADDRESS, SERVER_A_KEY, SERVER_B_KEY
from src.exceptions import ConnectError


def connect_server(host: str, port: int, username: str, key: paramiko.PKey, sock: paramiko.Channel = None) -> paramiko.SSHClient:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, pkey=key, sock=sock)
        return client
    
    except paramiko.AuthenticationException as auth_err:
        logging.error(f"Authentication failed while connecting to server {host}: {auth_err}")
        raise ConnectError
    except paramiko.SSHException as ssh_err:
        logging.error(f"SSH error occurred while connecting to server {host}: {ssh_err}")
        raise ConnectError
    except socket.error as sock_err:
        logging.error(f"Socket error occurred while connecting to server {host}: {sock_err}")
        raise ConnectError
    except Exception as e:
        logging.error(f"An unexpected error occurred while connecting to server {host}: {e}")
        raise ConnectError
    


def open_channel(client_A: paramiko.SSHClient, server_b_host: str, server_b_port: int) -> paramiko.Channel:
    try:
        transport = client_A.get_transport()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            port = s.getsockname()[1]
        
        src_addr = ('127.0.0.1', port)
        dest_addr = (server_b_host, server_b_port)
        channel = transport.open_channel("direct-tcpip", dest_addr, src_addr)
        
        return channel
    
    except paramiko.SSHException as ssh_err:
        logging.error(f"SSH error occurred while opening channel: {ssh_err}")
        raise ConnectError
    except socket.error as sock_err:
        logging.error(f"Socket error occurred while opening channel: {sock_err}")
        raise ConnectError
    

def create_connection() -> tuple[paramiko.SSHClient, paramiko.SSHClient, paramiko.SFTPClient]:
    try:
        a_key = paramiko.RSAKey.from_private_key(StringIO(SERVER_A_KEY))
        b_key = paramiko.RSAKey.from_private_key(StringIO(SERVER_B_KEY))
        client_A = connect_server(SERVER_A_ADDRESS, SSH_SERVER_PORT, USERNAME, a_key)
        channel = open_channel(client_A, SERVER_B_ADDRESS, SSH_SERVER_PORT)
        client_B = connect_server(SERVER_B_ADDRESS, SSH_SERVER_PORT, USERNAME, b_key, sock=channel)
        sftp_client = client_B.open_sftp()

        return client_A, client_B, sftp_client
    except ConnectError:
        raise ConnectError
    except paramiko.SSHException as ssh_err:
        logging.error(f"SSH error occurred during connection setup: {ssh_err}")
        raise ConnectError
    except paramiko.AuthenticationException as auth_err:
        logging.error(f"Authentication error occurred during connection setup: {auth_err}")
        raise ConnectError
    except socket.error as sock_err:
        logging.error(f"Socket error occurred during connection setup: {sock_err}")
        raise ConnectError
    except Exception as e:
        logging.error(f"An unexpected error occurred during connection setup: {e}")
        raise ConnectError
    


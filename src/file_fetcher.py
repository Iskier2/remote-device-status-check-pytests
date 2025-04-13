from paramiko import SFTPClient


def read_remote_file(sftp_client: SFTPClient, filepath: str) -> str:
    try:
        return sftp_client.open(filepath, 'r').read().decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Cannot read remote file. {e}")

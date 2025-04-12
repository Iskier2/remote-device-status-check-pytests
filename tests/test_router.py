from unittest.mock import patch, MagicMock
from src.router import connect_server, open_channel, create_connection
from src.exceptions import ConnectError
import paramiko
import pytest
import socket

def test_connect_server_success():
    mock_client = MagicMock()
    with patch("src.router.paramiko.SSHClient", return_value=mock_client):
        key = MagicMock()
        client = connect_server("127.0.0.1", 22, "user", key)
        assert client == mock_client
        mock_client.connect.assert_called_once_with(
            hostname="127.0.0.1", port=22, username="user", pkey=key, sock=None
        )


def test_connect_server_authentication_error():
    with patch("src.router.paramiko.SSHClient") as mock_ssh_client:
        mock_ssh_client.return_value.connect.side_effect = paramiko.AuthenticationException
        with pytest.raises(ConnectError):
            connect_server("127.0.0.1", 22, "user", MagicMock())


def test_connect_server_ssh_error():
    with patch("src.router.paramiko.SSHClient") as mock_ssh_client:
        mock_ssh_client.return_value.connect.side_effect = paramiko.SSHException
        with pytest.raises(ConnectError):
            connect_server("127.0.0.1", 22, "user", MagicMock())


def test_connect_server_socket_error():
    with patch("src.router.paramiko.SSHClient") as mock_ssh_client:
        mock_ssh_client.return_value.connect.side_effect = socket.error
        with pytest.raises(ConnectError):
            connect_server("127.0.0.1", 22, "user", MagicMock())


def test_open_channel_success():
    mock_transport = MagicMock()
    mock_client = MagicMock()
    mock_client.get_transport.return_value = mock_transport

    with patch("socket.socket") as mock_socket:
        mock_socket.return_value.__enter__.return_value.getsockname.return_value = ("127.0.0.1", 12345)
        channel = open_channel(mock_client, "127.0.0.2", 22)
        assert channel == mock_transport.open_channel.return_value
        mock_transport.open_channel.assert_called_once_with(
            "direct-tcpip", ("127.0.0.2", 22), ("127.0.0.1", 12345)
        )


def test_open_channel_ssh_error():
    mock_transport = MagicMock()
    mock_transport.open_channel.side_effect = paramiko.SSHException
    mock_client = MagicMock()
    mock_client.get_transport.return_value = mock_transport

    with pytest.raises(ConnectError):
        open_channel(mock_client, "127.0.0.2", 22)


def test_open_channel_socket_error():
    mock_client = MagicMock()

    with patch("socket.socket") as mock_socket:
        mock_socket.side_effect = socket.error
        with pytest.raises(ConnectError):
            open_channel(mock_client, "127.0.0.2", 22)


def test_create_connection_success():
    mock_client_A = MagicMock()
    mock_client_B = MagicMock()
    mock_sftp_client = MagicMock()

    with patch("src.router.connect_server", side_effect=[mock_client_A, mock_client_B]) as mock_connect_server, \
         patch("src.router.open_channel", return_value=MagicMock()) as mock_open_channel, \
         patch("src.router.paramiko.RSAKey.from_private_key", return_value=MagicMock()), \
         patch.object(mock_client_B, "open_sftp", return_value=mock_sftp_client):
        client_A, client_B, sftp_client = create_connection()
        assert client_A == mock_client_A
        assert client_B == mock_client_B
        assert sftp_client == mock_sftp_client
        mock_connect_server.assert_called()
        mock_open_channel.assert_called_once()


def test_create_connection_connect_error():
    with patch("src.router.connect_server", side_effect=ConnectError):
        with pytest.raises(ConnectError):
            create_connection()


def test_create_connection_ssh_error():
    with patch("src.router.connect_server", side_effect=paramiko.SSHException):
        with pytest.raises(ConnectError):
            create_connection()


def test_create_connection_authentication_error():
    with patch("src.router.connect_server", side_effect=paramiko.AuthenticationException):
        with pytest.raises(ConnectError):
            create_connection()


def test_create_connection_socket_error():
    with patch("src.router.connect_server", side_effect=socket.error):
        with pytest.raises(ConnectError):
            create_connection()
from unittest.mock import patch, MagicMock
from src.router import connect_server, open_channel, create_connection
from src.exceptions import ConnectError
import paramiko
import pytest
import socket
import pytest_mock


@pytest.fixture(autouse=True)
def setup_test_open_channel(
            mocker: pytest_mock.MockerFixture,
            request: pytest.FixtureRequest
        ):
    mock_transport = mocker.Mock()
    request.cls.mock_client = mocker.Mock()
    request.cls.mock_transport = mock_transport
    request.cls.mock_client.get_transport.return_value = mock_transport
    request.cls.mock_transport.open_channel.return_value = mocker.Mock()


@pytest.mark.test_connect_server
class TestConnectServer:
    def test_connect_server_success(self):
        mock_client = MagicMock()
        with patch("src.router.paramiko.SSHClient", return_value=mock_client):
            key = MagicMock()
            client = connect_server("127.0.0.1", 22, "user", key)
            assert client == mock_client
            mock_client.connect.assert_called_once_with(
                hostname="127.0.0.1", port=22,
                username="user", pkey=key, sock=None
            )

    def test_connect_server_authentication_error(self):
        with patch("src.router.paramiko.SSHClient") as mock_ssh_client:
            mock_ssh_client.side_effect = paramiko.AuthenticationException
            with pytest.raises(ConnectError):
                connect_server("127.0.0.1", 22, "user", MagicMock())

    def test_connect_server_ssh_error(self):
        with patch("src.router.paramiko.SSHClient") as mock_ssh_client:
            mock_ssh_client.side_effect = paramiko.SSHException
            with pytest.raises(ConnectError):
                connect_server("127.0.0.1", 22, "user", MagicMock())

    def test_connect_server_socket_error(self):
        with patch("src.router.paramiko.SSHClient") as mock_ssh_client:
            mock_ssh_client.side_effect = socket.error
            with pytest.raises(ConnectError):
                connect_server("127.0.0.1", 22, "user", MagicMock())


@pytest.mark.test_open_channel
@pytest.mark.usefixtures("setup_test_open_channel")
class TestOpenChannel:
    def test_open_channel_success(self):

        with patch("socket.socket") as mock_socket:
            enter = mock_socket.return_value.__enter__
            enter.return_value.getsockname.return_value = (
                "127.0.0.1", 12345
            )
            channel = open_channel(self.mock_client, "127.0.0.2", 22)
            assert channel == self.mock_transport.open_channel.return_value
            self.mock_transport.open_channel.assert_called_once_with(
                "direct-tcpip", ("127.0.0.2", 22), ("127.0.0.1", 12345)
            )

    def test_open_channel_ssh_error(self):
        self.mock_transport.open_channel.side_effect = paramiko.SSHException

        with pytest.raises(ConnectError):
            open_channel(self.mock_client, "127.0.0.2", 22)

    def test_open_channel_socket_error(self):

        with patch("socket.socket") as mock_socket:
            mock_socket.side_effect = socket.error
            with pytest.raises(ConnectError):
                open_channel(self.mock_client, "127.0.0.2", 22)


@pytest.mark.test_create_connection
class TestCreateConnection:
    def test_create_connection_success(self):
        mock_client_A = MagicMock()
        mock_client_B = MagicMock()
        mock_sftp_client = MagicMock()

        with patch(
                    "src.router.connect_server",
                    side_effect=[mock_client_A, mock_client_B]
                ) as mock_connect_server, \
                patch(
                    "src.router.open_channel",
                    return_value=MagicMock()
                ) as mock_open_channel, \
                patch(
                    "src.router.paramiko.RSAKey.from_private_key",
                    return_value=MagicMock()), \
                patch.object(
                    mock_client_B, "open_sftp",
                    return_value=mock_sftp_client
                ):
            client_A, client_B, sftp_client = create_connection()
            assert client_A == mock_client_A
            assert client_B == mock_client_B
            assert sftp_client == mock_sftp_client
            mock_connect_server.assert_called()
            mock_open_channel.assert_called_once()

    def test_create_connection_connect_error(self):
        with patch("src.router.connect_server", side_effect=ConnectError):
            with pytest.raises(ConnectError):
                create_connection()

    def test_create_connection_ssh_error(self):
        with patch(
                    "src.router.connect_server",
                    side_effect=paramiko.SSHException
                ):
            with pytest.raises(ConnectError):
                create_connection()

    def test_create_connection_authentication_error(self):
        with patch(
                    "src.router.connect_server",
                    side_effect=paramiko.AuthenticationException
                ):
            with pytest.raises(ConnectError):
                create_connection()

    def test_create_connection_socket_error(self):
        with patch("src.router.connect_server", side_effect=socket.error):
            with pytest.raises(ConnectError):
                create_connection()

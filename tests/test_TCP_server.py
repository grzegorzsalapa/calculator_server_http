import pytest
from unittest.mock import MagicMock, patch
from calculator_server.TCP_server import main


def _set_up_mocked_calculator_socket(recv_value=None):
    socket_instance = MagicMock(name="SocketInstance")
    socket_instance.accept = MagicMock(return_value=(0, 0))
    socket_instance.recv = MagicMock(return_value=recv_value)
    socket_instance.sendall = MagicMock()

    socket_context = MagicMock(name="SocketContext")
    socket_context.__enter__ = MagicMock(return_value=socket_instance)

    socket_mock = MagicMock()
    socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_context)

    return socket_mock


def test_that_received_binary_expression_returns_correct_binary_result():
    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'2+2')

    with patch('calculator_server.TCP_server.socket', new=socket_mock):
        main()
        socket_mock.socket().__enter__().sendall.assert_called_with(b'4')
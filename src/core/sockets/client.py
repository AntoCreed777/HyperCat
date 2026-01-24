import socket
from typing import override

from .base_socket import BaseSocket
from .type_status import TypeStatus


class SocketClient(BaseSocket):
    conn: socket.socket

    @override
    def __init__(self, host="localhost", port=54321):
        self.conn = socket.create_connection((host, port))
        print(f"Connected to server at {host}:{port}")

    def send_data(self, data: str | dict):
        self._send_message(data, TypeStatus.ENVIO_DATOS)

        status, response = self._receive_message()
        if status == TypeStatus.ERROR:
            raise Exception(response)

    def receive_data(self) -> str | dict:
        status, data = self._receive_message()
        if status == TypeStatus.ERROR:
            raise Exception(data)
        return data

    @override
    def close(self):
        if self.conn:
            self.conn.close()

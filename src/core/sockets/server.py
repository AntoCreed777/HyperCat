import socket
from typing import override

from .base_socket import BaseSocket
from .type_status import TypeStatus


class SocketServer(BaseSocket):
    server_socket: socket.socket
    conn: socket.socket | None = None

    @override
    def __init__(self, host="localhost", port=54321):
        self.server_socket = socket.create_server((host, port))
        self.server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

    def accept_connection(self):
        self.conn, addr = self.server_socket.accept()
        print(f"Connection from {addr} has been established!")
        return addr

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
        self.server_socket.close()

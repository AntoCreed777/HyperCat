import json
import socket
import struct
from abc import ABC, abstractmethod
from functools import wraps

from .message_socket import MessageSocket
from .type_status import TypeStatus


class BaseSocket(ABC):
    conn: socket.socket | None = None

    def asegurar_conexion(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.conn is None:
                raise ConnectionError("No connection established")
            return func(self, *args, **kwargs)

        return wrapper

    # ---------- Bajo Nivel ----------
    @asegurar_conexion
    def _send_json(self, data: dict):
        payload = json.dumps(data).encode("utf-8")
        header = struct.pack("!I", len(payload))
        self.conn.sendall(header + payload)

    def _recv_json(self) -> dict:
        header = self._recv_exact(4)
        length = struct.unpack("!I", header)[0]

        data = self._recv_exact(length)

        return json.loads(data.decode("utf-8"))

    @asegurar_conexion
    def _recv_exact(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk
        return data

    # ---------- Protocolo ----------
    def _send_message(self, message: str | dict, status: TypeStatus):
        data = MessageSocket.create_message(message, status)
        self._send_json(data)

    def _receive_message(self) -> tuple[TypeStatus, str | dict]:
        data = self._recv_json()
        return MessageSocket.parse_message(data)

    # ---------- API ----------
    def respond_success(self, message: str = ""):
        self._send_message(message, TypeStatus.SUCCESS)

    def respond_error(self, message: str):
        self._send_message(message, TypeStatus.ERROR)

    def send_data(self, data: str | dict):
        self._send_message(data, TypeStatus.ENVIO_DATOS)

        status, response = self._receive_message()
        if status == TypeStatus.ERROR:
            raise Exception(response)

    def receive_data(self) -> str | dict | None:
        status, data = self._receive_message()

        if status == TypeStatus.CLOSE:
            self.close()
            return None

        if status == TypeStatus.ERROR:
            raise Exception(data)
        return data

    @abstractmethod
    def close(self):
        pass

    # ---------- Context manager ----------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

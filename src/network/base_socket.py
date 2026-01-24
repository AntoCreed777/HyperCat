"""Módulo que contiene la clase base abstracta para sockets."""

import json
import socket
import struct
from abc import ABC, abstractmethod
from functools import wraps

from .message_socket import MessageSocket
from .type_status import TypeStatus


class BaseSocket(ABC):
    """
    Clase base abstracta para gestionar comunicación por sockets.

    Esta clase proporciona métodos de bajo nivel para enviar y recibir datos
    JSON a través de sockets, así como un protocolo de mensajes de alto nivel.

    Attributes:
        conn: El socket de conexión, None si no está conectado.
    """

    conn: socket.socket | None = None

    def asegurar_conexion(func):
        """
        Decorador que asegura que exista una conexión activa antes de ejecutar una función.

        Args:
            func: La función a decorar.

        Returns:
            La función decorada que verifica la conexión.

        Raises:
            ConnectionError: Si no hay una conexión establecida.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.conn is None:
                raise ConnectionError("No connection established")
            return func(self, *args, **kwargs)

        return wrapper

    # ---------- Bajo Nivel ----------
    @asegurar_conexion
    def _send_json(self, data: dict):
        """
        Envía datos JSON a través del socket.

        Encapsula el JSON con un encabezado que contiene la longitud del payload.

        Args:
            data: Diccionario a enviar en formato JSON.
        """
        payload = json.dumps(data).encode("utf-8")
        header = struct.pack("!I", len(payload))
        self.conn.sendall(header + payload)

    def _recv_json(self) -> dict:
        """
        Recibe datos JSON desde el socket.

        Lee primero el encabezado (4 bytes) para obtener la longitud,
        luego recibe exactamente esa cantidad de datos.

        Returns:
            Diccionario con los datos JSON recibidos.
        """
        header = self._recv_exact(4)
        length = struct.unpack("!I", header)[0]

        data = self._recv_exact(length)

        return json.loads(data.decode("utf-8"))

    @asegurar_conexion
    def _recv_exact(self, n: int) -> bytes:
        """
        Recibe exactamente n bytes del socket.

        Args:
            n: Número de bytes a recibir.

        Returns:
            Los bytes recibidos.

        Raises:
            ConnectionError: Si la conexión se cierra antes de recibir todos los datos.
        """
        data = b""
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk
        return data

    # ---------- Protocolo ----------
    def _send_message(self, message: str | dict, status: TypeStatus):
        """
        Envía un mensaje con estado mediante el protocolo de MessageSocket.

        Args:
            message: El mensaje a enviar (string o diccionario).
            status: El estado del mensaje (TypeStatus).
        """
        data = MessageSocket.create_message(message, status)
        self._send_json(data)

    def _receive_message(self) -> tuple[TypeStatus, str | dict]:
        """
        Recibe un mensaje del socket y lo procesa.

        Returns:
            Una tupla (TypeStatus, mensaje) con el estado y contenido del mensaje.
        """
        data = self._recv_json()
        return MessageSocket.parse_message(data)

    # ---------- API ----------
    def respond_success(self, message: str = ""):
        """
        Envía una respuesta de éxito al remitente.

        Args:
            message: Mensaje de éxito a enviar, vacío por defecto.
        """
        self._send_message(message, TypeStatus.SUCCESS)

    def respond_error(self, message: str):
        """
        Envía una respuesta de error al remitente.

        Args:
            message: Mensaje de error a enviar.
        """
        self._send_message(message, TypeStatus.ERROR)

    def send_data(self, data: str | dict):
        """
        Envía datos y espera una respuesta de confirmación.

        Args:
            data: Datos a enviar (string o diccionario).

        Raises:
            Exception: Si la respuesta es un error.
        """
        self._send_message(data, TypeStatus.ENVIO_DATOS)

        status, response = self._receive_message()
        if status == TypeStatus.ERROR:
            raise Exception(response)

    def receive_data(self) -> str | dict | None:
        """
        Recibe datos desde el socket.

        Returns:
            Los datos recibidos, o None si se recibe una señal de cierre.

        Raises:
            Exception: Si la respuesta es un error.
        """
        status, data = self._receive_message()

        if status == TypeStatus.CLOSE:
            self.close()
            return None

        if status == TypeStatus.ERROR:
            raise Exception(data)
        return data

    @abstractmethod
    def close(self):
        """
        Cierra la conexión del socket.

        Este método debe ser implementado por las clases derivadas.
        """
        pass

    # ---------- Context manager ----------
    def __enter__(self):
        """
        Método de entrada para usar BaseSocket como context manager.

        Returns:
            La instancia del socket.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Método de salida para usar BaseSocket como context manager.

        Cierra la conexión al salir del contexto.

        Args:
            exc_type: Tipo de excepción si ocurrió una.
            exc_value: Valor de la excepción si ocurrió una.
            traceback: Traceback de la excepción si ocurrió una.
        """
        self.close()

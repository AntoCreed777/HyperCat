"""Módulo que contiene la clase servidor para comunicación por socket."""

import socket
from typing import override

from .base_socket import BaseSocket
from .type_status import TypeStatus


class SocketServer(BaseSocket):
    """
    Clase que implementa un servidor de socket para aceptar conexiones de clientes.

    Se encarga de escuchar en un puerto específico y gestionar las conexiones
    entrantes de los clientes.

    Attributes:
        server_socket: El socket de escucha del servidor.
        conn: El socket de conexión activa con un cliente.
    """

    server_socket: socket.socket
    conn: socket.socket | None = None

    @override
    def __init__(self, host="localhost", port=54321):
        """
        Inicializa el servidor y lo pone en modo de escucha.

        Args:
            host: La dirección IP del servidor, por defecto 'localhost'.
            port: El puerto de escucha, por defecto 54321.
        """
        self.server_socket = socket.create_server((host, port))
        self.server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

    def accept_connection(self):
        """
        Acepta una conexión entrante de un cliente.

        Configura el socket con SO_KEEPALIVE para detectar desconexiones físicas.

        Returns:
            La dirección (IP, puerto) del cliente conectado.

        Raises:
            RuntimeError: Si ya hay un cliente conectado.
        """
        if self.conn is not None:
            raise RuntimeError("A client is already connected")

        self.conn, addr = self.server_socket.accept()
        # Configuración Keep-Alive para detectar si la otra PC se desconecta físicamente
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        print(f"Connection from {addr} has been established!")
        return addr

    @override
    def close(self):
        """
        Cierra tanto la conexión activa como el servidor de escucha.

        Primero cierra la conexión del cliente y luego cierra el socket de escucha.
        """
        self.close_connection()
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            print("Socket de escucha del servidor cerrado.")

    def close_connection(self):
        """
        Cierra únicamente la conexión con el cliente actual.

        Envía una señal de cierre al cliente y luego cierra su socket.
        """
        if self.conn:
            try:
                # Avisar al cliente que el servidor va a cerrar
                self._send_message("Server closing", TypeStatus.CLOSE)

                self.conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                # El cliente ya se había desconectado
                pass
            finally:
                self.conn.close()
                self.conn = None
                print("Conexión con el cliente cerrada de forma segura.")

"""Módulo que contiene la clase cliente para comunicación por socket."""

import socket
from typing import override

from .base_socket import BaseSocket
from .type_status import TypeStatus


class SocketClient(BaseSocket):
    """
    Clase que implementa un cliente de socket para conectarse a un servidor.

    Se encarga de establecer la conexión con un servidor remoto y gestionar
    la comunicación a través de sockets.

    Attributes:
        conn: El socket de conexión activa con el servidor.
    """

    conn: socket.socket

    @override
    def __init__(self, host="localhost", port=54321):
        """
        Inicializa el cliente y establece la conexión con el servidor.

        Args:
            host: La dirección IP o nombre del servidor, por defecto 'localhost'.
            port: El puerto del servidor, por defecto 54321.
        """
        self.conn = socket.create_connection((host, port))
        print(f"Connected to server at {host}:{port}")

    @override
    def close(self):
        """
        Cierra la conexión con el servidor de forma segura.

        Envía una señal de cierre al servidor, realiza el shutdown del socket
        y luego cierra la conexión.
        """
        if self.conn:
            try:
                # 1. Aviso lógico al servidor
                self._send_message("", TypeStatus.CLOSE)

                # 2. Cierre de canales de transmisión (TCP FIN)
                self.conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                # Si el servidor ya cerró o la red cayó, ignoramos el error
                pass
            finally:
                # 3. Liberación definitiva de recursos
                self.conn.close()
                self.conn = None
                print("Conexión cerrada de forma segura.")

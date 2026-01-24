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
        if self.conn is not None:
            raise RuntimeError("A client is already connected")

        self.conn, addr = self.server_socket.accept()
        # Configuración Keep-Alive para detectar si la otra PC se desconecta físicamente
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        print(f"Connection from {addr} has been established!")
        return addr

    @override
    def close(self):
        """Cierra tanto la conexión activa como el servidor de escucha."""
        self.close_connection()
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            print("Socket de escucha del servidor cerrado.")

    def close_connection(self):
        """Cierra únicamente la conexión con el cliente actual."""
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

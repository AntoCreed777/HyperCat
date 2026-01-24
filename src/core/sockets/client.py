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

    @override
    def close(self):
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

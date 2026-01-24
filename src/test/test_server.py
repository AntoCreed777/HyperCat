"""Script de prueba para el servidor de socket.

Este módulo contiene un servidor interactivo que acepta conexiones de clientes
y permite enviar y recibir mensajes de forma interactiva.
"""

from src.core import SocketServer

server = SocketServer()
server.accept_connection()

while True:
    # Envio de datos
    entrada = input("> ")

    if entrada.lower() == "exit":
        break

    server.send_data(entrada)

    # Recepción de datos
    data = server.receive_data()

    if data is None:  # El cliente cerró la conexión
        break

    print(f"Received data:\t{data}")

    server.respond_success()

server.close()

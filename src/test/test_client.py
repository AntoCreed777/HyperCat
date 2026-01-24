"""Script de prueba para el cliente de socket.

Este módulo contiene un cliente interactivo que se conecta a un servidor
y permite enviar y recibir mensajes de forma interactiva.
"""

from src.network import SocketClient

client = SocketClient()

while True:
    # Recepción de datos
    data = client.receive_data()

    if data is None:  # El servidor cerró la conexión
        break

    print(f"Received data:\t{data}")

    client.respond_success()

    # Envio de datos
    entrada = input("> ")

    if entrada.lower() == "exit":
        break

    client.send_data(entrada)

client.close()

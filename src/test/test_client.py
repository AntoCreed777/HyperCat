from src.core import SocketClient

client = SocketClient()

while True:
    # Recepción de datos
    data = client.receive_data()

    print(f"Received data:\t{data}")

    client.respond_success()

    # Envio de datos
    entrada = input("> ")

    if entrada.lower() == "exit":
        break

    client.send_data(entrada)

client.close()
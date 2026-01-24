"""Módulo que contiene la clase para crear y procesar mensajes de socket."""

from .type_status import TypeStatus


class MessageSocket:
    """
    Clase utilitaria para crear y procesar mensajes en formato socket.

    Esta clase maneja la serialización y deserialización de mensajes
    que se envían a través de la red.
    """

    @staticmethod
    def create_message(message: str | dict, status_code: TypeStatus) -> dict:
        """
        Crea un mensaje estructurado para enviar a través del socket.

        Args:
            message: El contenido del mensaje (string o diccionario).
            status_code: El estado del mensaje (TypeStatus).

        Returns:
            Diccionario con los campos 'status' y 'message'.
        """
        response = {"status": status_code.name, "message": message}

        return response

    @staticmethod
    def parse_message(response: dict) -> tuple[TypeStatus, str | dict]:
        """
        Procesa un mensaje recibido desde el socket.

        Args:
            response: Diccionario con los datos del mensaje.

        Returns:
            Tupla (TypeStatus, mensaje) con el estado y contenido del mensaje.
        """
        status_code = TypeStatus[response["status"]]
        message = response["message"]

        return status_code, message

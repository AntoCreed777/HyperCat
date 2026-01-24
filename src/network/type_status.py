"""Módulo que contiene la enumeración de estados de tipo de mensaje."""

from enum import Enum, auto


class TypeStatus(Enum):
    """
    Enumeración de los posibles estados de un mensaje en el socket.

    Define los tipos de mensajes que pueden ser enviados:
        SUCCESS: Mensaje de éxito.
        ERROR: Mensaje de error.
        ENVIO_DATOS: Envío de datos.
        CLOSE: Señal de cierre de conexión.
    """

    SUCCESS = auto()
    ERROR = auto()
    ENVIO_DATOS = auto()
    CLOSE = auto()

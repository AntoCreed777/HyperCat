from enum import Enum, auto


class TypeStatus(Enum):
    SUCCESS = auto()
    ERROR = auto()
    ENVIO_DATOS = auto()
    CLOSE = auto()

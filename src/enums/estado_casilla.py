from enum import Enum, auto


class EstadoCasilla(Enum):
    VACIA = auto()
    X = auto()
    O = auto()

    def ocupada(self) -> bool:
        return self != EstadoCasilla.VACIA

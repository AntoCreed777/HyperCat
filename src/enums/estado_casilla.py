"""Módulo con la enumeración de estados de casilla."""

from enum import Enum, auto


class EstadoCasilla(Enum):
    """
    Enumeración de los posibles estados de una casilla en el juego de Gato.

    Esta clase define los estados VACIA, X y O para el tablero de juego.
    """

    VACIA = auto()
    X = auto()
    O = auto()

    def ocupada(self) -> bool:
        """
        Verifica si la casilla está ocupada.

        Returns:
            True si la casilla contiene X u O, False si está vacía.
        """
        return self != EstadoCasilla.VACIA

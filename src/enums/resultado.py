"""Módulo con la enumeración de resultados del juego."""

from enum import Enum, auto


class Resultado(Enum):
    """
    Enumeración de los posibles resultados del juego.

    Esta clase define los resultados posibles: VICTORIA_X, VICTORIA_O, EMPATE y EN_CURSO.
    """

    VICTORIA_X = auto()
    VICTORIA_O = auto()
    EMPATE = auto()
    EN_CURSO = auto()

    def terminado(self) -> bool:
        """
        Verifica si el juego ha terminado.

        Returns:
            True si el juego ha terminado (victoria o empate), False si está en curso.
        """
        return self != Resultado.EN_CURSO

    def mensaje(self) -> str:
        """
        Obtiene el mensaje correspondiente al resultado del juego.

        Returns:
            Un mensaje descriptivo del resultado del juego.
        """
        match self:
            case Resultado.VICTORIA_X:
                return "¡Felicidades! X ha ganado."
            case Resultado.VICTORIA_O:
                return "¡Felicidades! O ha ganado."
            case Resultado.EMPATE:
                return "El juego ha terminado en empate."
            case Resultado.EN_CURSO:
                return ""

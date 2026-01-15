from enum import Enum, auto


class Resultado(Enum):
    VICTORIA_X = auto()
    VICTORIA_O = auto()
    EMPATE = auto()
    EN_CURSO = auto()

    def terminado(self) -> bool:
        return self != Resultado.EN_CURSO

    def mensaje(self) -> str:
        match self:
            case Resultado.VICTORIA_X:
                return "¡Felicidades! X ha ganado."
            case Resultado.VICTORIA_O:
                return "¡Felicidades! O ha ganado."
            case Resultado.EMPATE:
                return "El juego ha terminado en empate."
            case Resultado.EN_CURSO:
                return ""

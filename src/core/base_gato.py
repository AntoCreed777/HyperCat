from abc import ABC, abstractmethod
from typing import Any, Literal, TypeAlias

from enums.estado_casilla import EstadoCasilla
from enums.resultado import Resultado

Tablero: TypeAlias = list[list[Any]]
Turno: TypeAlias = Literal[EstadoCasilla.X, EstadoCasilla.O]


class BaseGato(ABC):
    turno: Turno
    tablero: Tablero
    resultado: Resultado

    def __init__(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        self._generar_tablero()
        self.turno = turno_inicial
        self.resultado = Resultado.EN_CURSO

    def reiniciar(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        self._generar_tablero()
        self.turno = turno_inicial
        self.resultado = Resultado.EN_CURSO

    @abstractmethod
    def _generar_tablero(self) -> None:
        pass

    def _fuera_de_rango(self, fila: int, columna: int) -> bool:
        return not (0 <= fila < 3 and 0 <= columna < 3)

    def _cambiar_turno(self) -> None:
        self.turno = (
            EstadoCasilla.O if self.turno == EstadoCasilla.X else EstadoCasilla.X
        )
    
    def _vincular_Jugador_tipo_resultado(self, jugador: Turno) -> Resultado:
        if jugador == EstadoCasilla.X:
            return Resultado.VICTORIA_X
        elif jugador == EstadoCasilla.O:
            return Resultado.VICTORIA_O
        raise ValueError("Jugador inválido para vincular resultado.")

    @abstractmethod
    def jugar(self, fila: int, columna: int) -> bool:
        pass

    @abstractmethod
    def validar_victoria(self) -> Resultado:
        pass

    def terminado(self) -> bool:
        return self.validar_victoria().terminado()

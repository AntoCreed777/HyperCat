from abc import ABC, abstractmethod
from typing import Generic, Literal, TypeAlias, TypeVar

from enums import EstadoCasilla, Resultado

ContenidoCasilla = TypeVar("ContenidoCasilla")
Tablero: TypeAlias = list[list[ContenidoCasilla]]
Turno: TypeAlias = Literal[EstadoCasilla.X, EstadoCasilla.O]


class BaseGato(ABC, Generic[ContenidoCasilla]):
    turno: Turno
    tablero: Tablero[ContenidoCasilla]
    resultado: Resultado
    reiniciado: bool

    def __init__(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        self._generar_tablero()
        self.turno = turno_inicial
        self.resultado = Resultado.EN_CURSO
        self.reiniciado = False

    def reiniciar(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        self._generar_tablero()
        self.turno = turno_inicial
        self.resultado = Resultado.EN_CURSO
        self.reiniciado = True

    @abstractmethod
    def _generar_tablero(self) -> None:
        pass

    def _fuera_de_rango(self, fila: int, columna: int, size: int = 3) -> bool:
        return not (0 <= fila < size and 0 <= columna < size)

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

    def validar_victoria(self) -> Resultado:
        if self.resultado is not Resultado.EN_CURSO:
            return self.resultado

        lineas = (
            [
                # Filas
                [(i, 0), (i, 1), (i, 2)]
                for i in range(3)
            ]
            + [
                # Columnas
                [(0, i), (1, i), (2, i)]
                for i in range(3)
            ]
            + [
                # Diagonales
                [(0, 0), (1, 1), (2, 2)],
                [(0, 2), (1, 1), (2, 0)],
            ]
        )

        # Validar victoria
        for linea in lineas:
            if r := self._linea_ganadora(linea):
                self.resultado = r
                return r

        # Validar empate
        if self._validar_empate():
            self.resultado = Resultado.EMPATE
        else:
            self.resultado = Resultado.EN_CURSO

        return self.resultado

    @abstractmethod
    def jugar(self, fila: int, columna: int):
        pass

    @abstractmethod
    def _linea_ganadora(self, coords: list[tuple[int, int]]) -> Resultado | None:
        """Comprueba si una línea específica es ganadora."""
        pass

    @abstractmethod
    def _validar_empate(self) -> bool:
        """
        Determina si el juego ha terminado en empate.

        Returns:
            bool: True si el juego ha terminado en empate, False de lo contrario.
        """
        pass

    def terminado(self) -> bool:
        return self.validar_victoria().terminado()

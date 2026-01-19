from typing import override

from enums import EstadoCasilla, Resultado

from .base_gato import BaseGato, Tablero
from .exceptions_custom import *


class Gato(BaseGato[EstadoCasilla]):

    @override
    def _generar_tablero(self) -> None:
        self.tablero: Tablero[EstadoCasilla] = [
            [EstadoCasilla.VACIA for _ in range(3)] for _ in range(3)
        ]

    @override
    def jugar(self, fila: int, columna: int):
        self.reiniciado = False

        if self.validar_victoria().terminado():
            raise JuegoTerminadoError()

        if self._fuera_de_rango(fila, columna):
            raise FueraDeRangoError()

        if self.tablero[fila][columna] != EstadoCasilla.VACIA:
            raise CasillaOcupadaError()

        self.tablero[fila][columna] = self.turno
        self._cambiar_turno()

    @override
    def _linea_ganadora(self, coords: list[tuple[int, int]]) -> Resultado | None:
        e = self.tablero[coords[0][0]][coords[0][1]]
        if e != EstadoCasilla.VACIA and all(self.tablero[f][c] == e for f, c in coords):
            return self._vincular_Jugador_tipo_resultado(e)
        return None

    @override
    def _validar_empate(self) -> bool:
        return all(
            self.tablero[fila][columna] != EstadoCasilla.VACIA
            for fila in range(3)
            for columna in range(3)
        )

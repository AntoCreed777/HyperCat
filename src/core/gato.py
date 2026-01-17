from typing import TypeAlias, override

from enums.estado_casilla import EstadoCasilla
from enums.resultado import Resultado

from .base_gato import BaseGato

Tablero: TypeAlias = list[list[EstadoCasilla]]


class Gato(BaseGato):

    @override
    def _generar_tablero(self) -> None:
        self.tablero: Tablero = [
            [EstadoCasilla.VACIA for _ in range(3)] for _ in range(3)
        ]

    @override
    def jugar(self, fila: int, columna: int) -> bool:
        if self.validar_victoria().terminado():
            return False  # Juego ya terminado

        if self._fuera_de_rango(fila, columna):
            return False  # Jugada inválida

        if self.tablero[fila][columna] != EstadoCasilla.VACIA:
            return False  # Jugada inválida

        self.tablero[fila][columna] = self.turno
        self._cambiar_turno()
        return True  # Jugada válida

    @override
    def _linea_ganadora(self, coords: list[tuple[int, int]]) -> Resultado | None:
        e = self.tablero[coords[0][0]][coords[0][1]]
        if e != EstadoCasilla.VACIA and all(
            self.tablero[f][c] == e for f, c in coords
        ):
            return self._vincular_Jugador_tipo_resultado(e)
        return None

    @override
    def _validar_empate(self) -> bool:
        for fila in self.tablero:
            for casilla in fila:
                if casilla == EstadoCasilla.VACIA:
                    return False
        return True
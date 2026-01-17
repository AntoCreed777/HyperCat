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
    def validar_victoria(self) -> Resultado:
        if self.resultado is not Resultado.EN_CURSO:
            return self.resultado

        # Validar filas y columnas
        for i in range(3):
            if (
                self.tablero[i][0]
                == self.tablero[i][1]
                == self.tablero[i][2]
                != EstadoCasilla.VACIA
            ):
                self.resultado = self._vincular_Jugador_tipo_resultado(
                    self.tablero[i][0]
                )
                return self.resultado

            if (
                self.tablero[0][i]
                == self.tablero[1][i]
                == self.tablero[2][i]
                != EstadoCasilla.VACIA
            ):
                self.resultado = self._vincular_Jugador_tipo_resultado(
                    self.tablero[0][i]
                )
                return self.resultado

        # Validar diagonales
        if (
            self.tablero[0][0]
            == self.tablero[1][1]
            == self.tablero[2][2]
            != EstadoCasilla.VACIA
        ):
            self.resultado = self._vincular_Jugador_tipo_resultado(self.tablero[0][0])
            return self.resultado
        if (
            self.tablero[0][2]
            == self.tablero[1][1]
            == self.tablero[2][0]
            != EstadoCasilla.VACIA
        ):
            self.resultado = self._vincular_Jugador_tipo_resultado(self.tablero[0][2])
            return self.resultado

        # Validar empate
        for fila in self.tablero:
            for casilla in fila:
                if casilla == EstadoCasilla.VACIA:
                    return Resultado.EN_CURSO

        self.resultado = Resultado.EMPATE
        return self.resultado

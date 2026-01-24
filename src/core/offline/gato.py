"""Módulo que implementa el juego de Gato clásico."""

from typing import override

from core.base_gato import BaseGato, Tablero
from core.exceptions_custom import *
from enums import EstadoCasilla, Resultado


class GatoOffline(BaseGato[EstadoCasilla]):
    """
    Clase que representa el juego de Gato clásico (Tic-Tac-Toe).

    Esta clase implementa la lógica del juego de Gato tradicional de 3x3.
    Hereda de BaseGato y especifica EstadoCasilla como tipo de contenido.
    """

    @override
    def _generar_tablero(self) -> None:
        """Genera un tablero de 3x3 con todas las casillas vacías."""
        self.tablero: Tablero[EstadoCasilla] = [
            [EstadoCasilla.VACIA for _ in range(3)] for _ in range(3)
        ]

    @override
    def jugar(self, fila: int, columna: int):
        """
        Realiza un movimiento en el tablero de juego.

        Args:
            fila: El índice de la fila donde se quiere jugar [0-2].
            columna: El índice de la columna donde se quiere jugar [0-2].

        Raises:
            JuegoTerminadoError: Si el juego ya ha terminado.
            FueraDeRangoError: Si la posición está fuera del tablero.
            CasillaOcupadaError: Si la casilla ya está ocupada.
        """
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
        """
        Verifica si hay una línea ganadora en las coordenadas dadas.

        Args:
            coords: Lista de tuplas con las coordenadas (fila, columna) a verificar.

        Returns:
            El resultado de victoria si hay una línea ganadora, None en caso contrario.
        """
        e = self.tablero[coords[0][0]][coords[0][1]]
        if e != EstadoCasilla.VACIA and all(self.tablero[f][c] == e for f, c in coords):
            return self._vincular_jugador_tipo_resultado(e)
        return None

    @override
    def _validar_empate(self) -> bool:
        """
        Verifica si el juego ha terminado en empate.

        Returns:
            True si todas las casillas están ocupadas, False en caso contrario.
        """
        return all(
            self.tablero[fila][columna] != EstadoCasilla.VACIA
            for fila in range(3)
            for columna in range(3)
        )

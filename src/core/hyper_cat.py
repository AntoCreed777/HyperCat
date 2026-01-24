"""Módulo que implementa el juego HyperCat."""

from typing import Optional, override

from src.core.base_gato import BaseGato, Tablero, Turno
from src.core.exceptions_custom import *
from src.core.gato import Gato
from src.enums import EstadoCasilla, Resultado


class HyperCat(BaseGato[Gato]):
    """
    Clase que representa el juego HyperCat (Ultimate Tic-Tac-Toe).

    Esta clase implementa la variante avanzada del juego de Gato donde
    el tablero está compuesto por 9 tableros de Gato más pequeños.

    Attributes:
        elegir_cualquiera: Indica si el jugador puede elegir cualquier sub-tablero.
        gato_a_jugar_despues: Coordenadas del próximo sub-tablero donde se debe jugar.
    """

    elegir_cualquiera: bool
    gato_a_jugar_despues: tuple[int, int] | None

    def __init__(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        """
        Inicializa el juego HyperCat.

        Args:
            turno_inicial: El turno inicial del juego, por defecto es X.
        """
        super().__init__(turno_inicial)
        self.elegir_cualquiera = True
        self.gato_a_jugar_despues = None

    def reiniciar(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        """
        Reinicia el juego HyperCat a su estado inicial.

        Args:
            turno_inicial: El turno inicial después del reinicio, por defecto es X.
        """
        super().reiniciar(turno_inicial)
        self.elegir_cualquiera = True
        self.gato_a_jugar_despues = None

    @override
    def _generar_tablero(self) -> None:
        """Genera un tablero de 3x3 donde cada casilla es un juego de Gato."""
        self.tablero: Tablero[Gato] = [
            [Gato() for _ in range(3)] for _ in range(3)
        ]

    @override
    def jugar(
        self,
        subfila: int,
        subcolumna: int,
        fila: Optional[int] = None,
        columna: Optional[int] = None,
    ):
        """
        Realiza un movimiento en el tablero de HyperCat.

        Args:
            subfila: El índice de la fila dentro del sub-tablero [0-2].
            subcolumna: El índice de la columna dentro del sub-tablero [0-2].
            fila: El índice de la fila del sub-tablero en el tablero principal [0-2].
                  Requerido si elegir_cualquiera es True.
            columna: El índice de la columna del sub-tablero en el tablero principal [0-2].
                     Requerido si elegir_cualquiera es True.

        Raises:
            JuegoTerminadoError: Si el juego principal ya ha terminado.
            EstadoInconsistenteError: Si los parámetros no coinciden con el estado del juego.
            FueraDeRangoError: Si las coordenadas están fuera del rango válido.
            SubGatoTerminadoError: Si se intenta jugar en un sub-tablero terminado.
        """
        self.reiniciado = False

        if self.validar_victoria().terminado():
            raise JuegoTerminadoError()

        if self.elegir_cualquiera:
            if fila is None or columna is None:
                raise EstadoInconsistenteError()
            if self._fuera_de_rango(fila, columna):
                raise FueraDeRangoError()
        else:
            if self.gato_a_jugar_despues is None:
                raise EstadoInconsistenteError()
            fila, columna = self.gato_a_jugar_despues

        gato_seleccionado = self.tablero[fila][columna]
        if gato_seleccionado.terminado():
            self.elegir_cualquiera = True
            raise SubGatoTerminadoError()

        gato_seleccionado.turno = self.turno

        try:
            gato_seleccionado.jugar(subfila, subcolumna)
        except GatoError as e:
            raise GatoError(
                f"No se pudo jugar en el gato seleccionado\nSub Gato ({fila}, {columna}): {str(e)}"
            )

        # Si el sub-gato termina en empate, lo reinicio
        if gato_seleccionado.validar_victoria() == Resultado.EMPATE:
            gato_seleccionado.reiniciar()

        gato_destino = self.tablero[subfila][subcolumna]
        # Validar si el gato a jugar despues ha terminado, en cuyo caso permito elegir cualquiera
        if gato_destino.terminado():
            self.elegir_cualquiera = True
            self.gato_a_jugar_despues = None
        else:
            self.elegir_cualquiera = False
            self.gato_a_jugar_despues = (subfila, subcolumna)

        self._cambiar_turno()

    @override
    def _linea_ganadora(self, coords: list[tuple[int, int]]) -> Resultado | None:
        r = self.tablero[coords[0][0]][coords[0][1]].resultado
        if r != Resultado.EN_CURSO and all(
            self.tablero[f][c].resultado == r for f, c in coords
        ):
            return r
        return None

    @override
    def _validar_empate(self) -> bool:
        return all(self.tablero[f][c].terminado() for f in range(3) for c in range(3))

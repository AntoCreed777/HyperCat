from typing import override

from enums import EstadoCasilla, Resultado

from .base_gato import BaseGato, Tablero, Turno
from .exceptions_custom import JuegoTerminadoError
from .gato import Gato


class HyperCat(BaseGato[Gato]):
    elegir_cualquiera: bool
    gato_a_jugar_despues: tuple[int, int] | None

    def __init__(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        super().__init__(turno_inicial)
        self.elegir_cualquiera = True
        self.gato_a_jugar_despues = None

    @override
    def _generar_tablero(self) -> None:
        self.tablero: Tablero[Gato] = [[Gato() for _ in range(3)] for _ in range(3)]

    @override
    def jugar(self, subfila: int, subcolumna: int, fila: int = -1, columna: int = -1):
        if self.validar_victoria().terminado():
            raise JuegoTerminadoError("El juego ya ha terminado.")

        if self.elegir_cualquiera:
            if self._fuera_de_rango(fila, columna):
                raise ValueError("Debe especificar un gato válido para jugar.")
        else:
            if self.gato_a_jugar_despues is None:
                raise RuntimeError("No se ha establecido el gato a jugar después.")
            fila, columna = self.gato_a_jugar_despues

        gato_seleccionado = self.tablero[fila][columna]
        if gato_seleccionado.terminado():
            self.elegir_cualquiera = True
            raise JuegoTerminadoError("El gato seleccionado ya ha terminado.")

        gato_seleccionado.turno = self.turno

        try:
            gato_seleccionado.jugar(subfila, subcolumna)
        except ValueError as e:
            raise ValueError(
                f"No se pudo jugar en el gato seleccionado\nSub Gato ({fila}, {columna}): {str(e)}"
            )

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

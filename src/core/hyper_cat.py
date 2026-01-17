from .base_gato import BaseGato
from .gato import Gato

from typing import override, TypeAlias, Literal
from enums.estado_casilla import EstadoCasilla
from enums.resultado import Resultado

Tablero: TypeAlias = list[list[Gato]]
Turno: TypeAlias = Literal[EstadoCasilla.X, EstadoCasilla.O]


class HyperCat(BaseGato):
    elegir_cualquiera: bool
    gato_a_jugar_despues: tuple[int, int] | None

    def __init__(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        super().__init__(turno_inicial)
        self.elegir_cualquiera = True
        self.gato_a_jugar_despues = None
    
    @override
    def _generar_tablero(self) -> None:
        self.tablero: Tablero = [
            [Gato() for _ in range(3)] for _ in range(3)
        ]
    
    @override
    def jugar(self, subfila: int, subcolumna: int, fila: int = -1, columna: int = -1) -> bool:
        if self.validar_victoria().terminado():
            return False  # Juego ya terminado

        if self.elegir_cualquiera:
            if self._fuera_de_rango(fila, columna):
                raise ValueError("Debe especificar un gato válido para jugar.")
        else:
            if self.gato_a_jugar_despues is None:
                raise ValueError("No se ha establecido el gato a jugar después.")
            fila, columna = self.gato_a_jugar_despues

        gato_seleccionado = self.tablero[fila][columna]
        if gato_seleccionado.terminado():
            self.elegir_cualquiera = True
            raise ValueError("El gato seleccionado ya ha terminado.")

        gato_seleccionado.turno = self.turno
        jugada_valida = gato_seleccionado.jugar(subfila, subcolumna)
        if jugada_valida:
            self._cambiar_turno()
            self.gato_a_jugar_despues = (subfila, subcolumna)
            self.elegir_cualquiera = False
        return jugada_valida
    
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
        if all(
            self.tablero[f][c].terminado() for f in range(3) for c in range(3)
        ):
            return True
        return False

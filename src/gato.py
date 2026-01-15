from enum.casillas import EstadoCasilla
from enum.resultado import Resultado

tablero_type = list[list[EstadoCasilla]]


class Gato:
    def __init__(self, turno_inicial: EstadoCasilla = EstadoCasilla.X) -> None:
        self.__generar_tablero()
        self.turno = turno_inicial

    def reiniciar(self) -> None:
        self.__generar_tablero()
        self.turno = EstadoCasilla.X

    def __generar_tablero(self) -> None:
        tablero: tablero_type = []

        for _ in range(3):
            fila = []
            for _ in range(3):
                fila.append(EstadoCasilla.VACIA)
            tablero.append(fila)

        self.tablero = tablero

    def jugar(self, fila: int, columna: int) -> bool:
        if fila < 0 or fila > 2 or columna < 0 or columna > 2:
            return False  # Jugada inválida

        if self.tablero[fila][columna] != EstadoCasilla.VACIA:
            return False  # Jugada inválida

        self.tablero[fila][columna] = self.turno
        self.__cambiar_turno()
        return True  # Jugada válida

    def __cambiar_turno(self) -> None:
        self.turno = (
            EstadoCasilla.O if self.turno == EstadoCasilla.X else EstadoCasilla.X
        )

    def validar_victoria(self) -> Resultado:
        # Validar filas y columnas
        for i in range(3):
            if (
                self.tablero[i][0]
                == self.tablero[i][1]
                == self.tablero[i][2]
                != EstadoCasilla.VACIA
            ):
                return self.__vincular_Jugador_tipo_resultado(self.tablero[i][0])
            if (
                self.tablero[0][i]
                == self.tablero[1][i]
                == self.tablero[2][i]
                != EstadoCasilla.VACIA
            ):
                return self.__vincular_Jugador_tipo_resultado(self.tablero[0][i])

        # Validar diagonales
        if (
            self.tablero[0][0]
            == self.tablero[1][1]
            == self.tablero[2][2]
            != EstadoCasilla.VACIA
        ):
            return self.__vincular_Jugador_tipo_resultado(self.tablero[0][0])
        if (
            self.tablero[0][2]
            == self.tablero[1][1]
            == self.tablero[2][0]
            != EstadoCasilla.VACIA
        ):
            return self.__vincular_Jugador_tipo_resultado(self.tablero[0][2])

        # Validar empate
        for fila in self.tablero:
            for casilla in fila:
                if casilla == EstadoCasilla.VACIA:
                    return Resultado.EN_CURSO

        return Resultado.EMPATE

    def __vincular_Jugador_tipo_resultado(self, jugador: EstadoCasilla) -> Resultado:
        if jugador == EstadoCasilla.X:
            return Resultado.VICTORIA_X
        elif jugador == EstadoCasilla.O:
            return Resultado.VICTORIA_O

    def imprimir_tablero(self) -> None:
        for fila in self.tablero:
            print(" | ".join(casilla.name for casilla in fila))
            print("-" * 9)

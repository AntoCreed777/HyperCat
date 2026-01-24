"""Módulo que contiene la clase base abstracta para el juego de Gato."""

from abc import ABC, abstractmethod
from typing import Generic, Literal, TypeAlias, TypeVar

from src.enums import EstadoCasilla, Resultado

ContenidoCasilla = TypeVar("ContenidoCasilla")
Tablero: TypeAlias = list[list[ContenidoCasilla]]
Turno: TypeAlias = Literal[EstadoCasilla.X, EstadoCasilla.O]


class BaseGato(ABC, Generic[ContenidoCasilla]):
    """
    Clase base abstracta para el juego de Gato.

    Esta clase define la interfaz común y las propiedades para los juegos de Gato.
    Implementa la lógica base del juego que puede ser extendida por clases derivadas.

    Attributes:
        turno: El turno actual del juego (X u O).
        tablero: El tablero de juego representado como una matriz.
        resultado: El resultado actual del juego.
        reiniciado: Indica si el juego ha sido reiniciado.
    """

    turno: Turno
    tablero: Tablero[ContenidoCasilla]
    resultado: Resultado
    reiniciado: bool

    def __init__(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        """
        Inicializa el tablero de juego y establece el turno inicial.

        Args:
            turno_inicial: El turno inicial del juego, por defecto es X.
        """
        self._generar_tablero()
        self.turno = turno_inicial
        self.resultado = Resultado.EN_CURSO
        self.reiniciado = False

    def reiniciar(self, turno_inicial: Turno = EstadoCasilla.X) -> None:
        """
        Reinicia el juego a su estado inicial.

        Args:
            turno_inicial: El turno inicial después del reinicio, por defecto es X.
        """
        self._generar_tablero()
        self.turno = turno_inicial
        self.resultado = Resultado.EN_CURSO
        self.reiniciado = True

    @abstractmethod
    def _generar_tablero(self) -> None:
        """
        Genera el tablero de juego.

        Este método debe ser implementado por las clases derivadas.
        """
        pass

    def _fuera_de_rango(self, fila: int, columna: int, size: int = 3) -> bool:
        """
        Verifica si una posición está fuera del rango del tablero.

        Args:
            fila: El índice de la fila a verificar.
            columna: El índice de la columna a verificar.
            size: El tamaño del tablero, por defecto es 3.

        Returns:
            True si la posición está fuera de rango, False en caso contrario.
        """
        return not (0 <= fila < size and 0 <= columna < size)

    def _cambiar_turno(self) -> None:
        """Cambia el turno al siguiente jugador."""
        self.turno = (
            EstadoCasilla.O if self.turno == EstadoCasilla.X else EstadoCasilla.X
        )

    def _vincular_jugador_tipo_resultado(self, jugador: Turno) -> Resultado:
        """
        Vincula un jugador con su correspondiente tipo de resultado de victoria.

        Args:
            jugador: El jugador (X u O) para vincular con el resultado.

        Returns:
            El resultado de victoria correspondiente al jugador.

        Raises:
            ValueError: Si el jugador no es válido.
        """
        if jugador == EstadoCasilla.X:
            return Resultado.VICTORIA_X
        elif jugador == EstadoCasilla.O:
            return Resultado.VICTORIA_O
        raise ValueError("Jugador inválido para vincular resultado.")

    def validar_victoria(self) -> Resultado:
        """
        Valida si hay un ganador o empate en el juego.

        Returns:
            El resultado actual del juego (victoria, empate o en curso).
        """
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
        """
        Realiza un movimiento en el juego.

        Args:
            fila: El índice de la fila donde se quiere jugar.
            columna: El índice de la columna donde se quiere jugar.
        """
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
        """
        Verifica si el juego ha terminado.

        Returns:
            True si el juego ha terminado, False en caso contrario.
        """
        return self.validar_victoria().terminado()

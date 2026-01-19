"""Módulo con las excepciones personalizadas del juego."""


class GatoError(Exception):
    """
    Excepción base para todos los errores del juego.

    Esta excepción se lanza para errores relacionados con el juego de Gato.
    """

    def __init__(self, message: str):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message: El mensaje de error a mostrar.
        """
        super().__init__("Error relacionado con el juego.\n" + message)


class JuegoTerminadoError(GatoError):
    """
    Se intenta jugar cuando el juego ya terminó.

    Esta excepción se lanza cuando se intenta hacer un movimiento
    después de que el juego ha finalizado.
    """

    def __init__(self):
        """Inicializa la excepción JuegoTerminadoError."""
        super().__init__(
            "El juego ya ha terminado. No se pueden hacer más movimientos."
        )


class SubGatoTerminadoError(GatoError):
    """
    Se intenta jugar en un sub-gato que ya terminó.

    Esta excepción se lanza cuando se intenta hacer un movimiento
    en un sub-tablero que ya ha finalizado.
    """

    def __init__(self):
        """Inicializa la excepción SubGatoTerminadoError."""
        super().__init__(
            "El sub-gato ya ha terminado. No se pueden hacer más movimientos en él."
        )


class MovimientoInvalidoError(GatoError):
    """Movimiento inválido por reglas del juego."""

    def __init__(self, message: str):
        """Inicializa la excepción MovimientoInvalidoError.

        Args:
            message: El mensaje de error.
        """
        super().__init__("Movimiento inválido.\n" + message)


class FueraDeRangoError(MovimientoInvalidoError):
    """La fila o columna está fuera del tablero."""

    def __init__(self):
        """Inicializa la excepción FueraDeRangoError."""
        super().__init__(
            "La fila o columna especificada está fuera del rango permitido del tablero."
        )


class CasillaOcupadaError(MovimientoInvalidoError):
    """Se intenta jugar en una casilla ocupada."""

    def __init__(self):
        """Inicializa la excepción CasillaOcupadaError."""
        super().__init__("La casilla especificada ya está ocupada por otro jugador.")


class GatoNoEspecificadoError(GatoError):
    """No se especificó el sub-gato cuando era obligatorio hacerlo."""

    def __init__(self):
        """Inicializa la excepción GatoNoEspecificadoError."""
        super().__init__("No se especificó el sub-gato cuando era obligatorio hacerlo.")


class EstadoInconsistenteError(GatoError):
    """El juego entró en un estado inválido (error interno)."""

    def __init__(self, message: str):
        """Inicializa la excepción EstadoInconsistenteError.

        Args:
            message: El mensaje de error.
        """
        super().__init__("El juego ha entrado en un estado inconsistente.\n" + message)

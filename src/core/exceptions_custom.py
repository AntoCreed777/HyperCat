class GatoError(Exception):
    """Excepción base para todos los errores del juego."""

    def __init__(self, message: str):
        super().__init__("Error relacionado con el juego.\n" + message)


class JuegoTerminadoError(GatoError):
    """Se intenta jugar cuando el juego ya terminó."""

    def __init__(self):
        super().__init__(
            "El juego ya ha terminado. No se pueden hacer más movimientos."
        )


class SubGatoTerminadoError(GatoError):
    """Se intenta jugar en un sub-gato que ya terminó."""

    def __init__(self):
        super().__init__(
            "El sub-gato ya ha terminado. No se pueden hacer más movimientos en él."
        )


class MovimientoInvalidoError(GatoError):
    """Movimiento inválido por reglas del juego."""

    def __init__(self, message: str):
        super().__init__("Movimiento inválido.\n" + message)


class FueraDeRangoError(MovimientoInvalidoError):
    """La fila o columna está fuera del tablero."""

    def __init__(self):
        super().__init__(
            "La fila o columna especificada está fuera del rango permitido del tablero."
        )


class CasillaOcupadaError(MovimientoInvalidoError):
    """Se intenta jugar en una casilla ocupada."""

    def __init__(self):
        super().__init__("La casilla especificada ya está ocupada por otro jugador.")


class GatoNoEspecificadoError(GatoError):
    """No se especificó el sub-gato cuando era obligatorio hacerlo."""

    def __init__(self):
        super().__init__("No se especificó el sub-gato cuando era obligatorio hacerlo.")


class EstadoInconsistenteError(GatoError):
    """El juego entró en un estado inválido (error interno)."""

    def __init__(self, message: str):
        super().__init__("El juego ha entrado en un estado inconsistente.\n" + message)

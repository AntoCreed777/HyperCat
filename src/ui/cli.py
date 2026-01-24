from core.base_gato import BaseGato
from core import Gato
from enums import EstadoCasilla, Resultado


def print_gato(gato: BaseGato) -> None:
    """Imprime el estado actual del gato en la consola."""
    if not isinstance(gato, BaseGato):
        raise ValueError("El objeto proporcionado no es una instancia de BaseGato.")
    
    if isinstance(gato, Gato):
        tamano = 3
    else:   # HyperCat
        tamano = 9

    for fila_iterator in range(tamano):
        fila_str = ""

        fila = fila_iterator // 3 if tamano == 9 else fila_iterator

        if fila_iterator % 3 == 0 and fila_iterator != 0:
            print("-" * (tamano * 4 + 2))

        for columna_iterator in range(tamano):
            columna = columna_iterator // 3 if tamano == 9 else columna_iterator

            if columna_iterator % 3 == 0 and columna_iterator != 0:
                fila_str += " | "

            casilla = gato.tablero[fila][columna]

            match casilla:
                # Casilla simple
                case EstadoCasilla.VACIA:
                    fila_str += " . "
                case EstadoCasilla.X:
                    fila_str += " X "
                case EstadoCasilla.O:
                    fila_str += " O "

                # Subgato
                case Gato():
                    match casilla.validar_victoria():
                        case Resultado.EN_CURSO:
                            fila_str += " . "
                        case Resultado.VICTORIA_X:
                            fila_str += " X "
                        case Resultado.VICTORIA_O:
                            fila_str += " O "
                        case _:
                            raise ValueError("Resultado desconocido en subgato.")

                case _:
                    raise ValueError(
                        f"Tipo de casilla desconocido: {type(casilla)}"
                    )

        print(fila_str.strip())

    print()  # Línea en blanco después del gato

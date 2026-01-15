from enum.casillas import EstadoCasilla
from enum.resultado import Resultado

from gato import Gato


def main():
    juego = Gato()

    while True:
        print("\n\n\n\n")
        juego.imprimir_tablero()
        fila = int(input("Ingrese la fila (0, 1, 2): "))
        columna = int(input("Ingrese la columna (0, 1, 2): "))

        if not juego.jugar(fila, columna):
            print("Movimiento inválido. Inténtalo de nuevo.")
            continue

        estado = juego.validar_victoria()
        if estado == Resultado.VICTORIA_X or estado == Resultado.VICTORIA_O:
            juego.imprimir_tablero()
            ganador = "X" if estado == Resultado.VICTORIA_X else "O"
            print(f"¡Felicidades! {ganador} ha ganado.")
            break
        elif estado == Resultado.EMPATE:
            juego.imprimir_tablero()
            print("El juego ha terminado en empate.")
            break


if __name__ == "__main__":
    main()

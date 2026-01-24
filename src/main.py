"""Módulo principal del juego."""

from ui import *


def main():
    """
    Función principal para iniciar el juego.

    Muestra las opciones de juego disponibles y maneja la entrada del usuario
    para seleccionar el tipo de juego a jugar.

    Lanza el juego seleccionado.
    """
    print("Que deseas jugar?", "\n1. HyperCat", "\n2. TicTacToe (Gato clasico)", "\n\n")

    while True:
        eleccion = input("Ingresa el numero del juego: ")
        match eleccion:
            case "1":
                VentanaHyperCatOffline().run()
                break
            case "2":
                VentanaGatoOffline().run()
                break
            case _:
                print("Opcion no valida\n\n")


if __name__ == "__main__":
    main()

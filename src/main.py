from ui import *


def main():
    print(
        "Que deseas jugar?",
        "\n1. HyperCat",
        "\n2. TicTacToe (Gato clasico)",
        "\n\n"
    )

    while True:
        eleccion = input("Ingresa el numero del juego: ")
        match eleccion:
            case "1":
                VentanaHyperCat().run()
                break
            case "2":
                VentanaGato().run()
                break
            case _:
                print("Opcion no valida\n\n")


if __name__ == "__main__":
    main()

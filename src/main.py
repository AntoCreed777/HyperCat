import tkinter as tk
from tkinter import messagebox

from enums.resultado import Resultado
from gato import Gato


def desactivar_tablero(botones):
    for fila in botones:
        for boton in fila:
            boton.config(state="disabled")


def click_event_in_button(i, j, boton, juego: Gato, botones):
    simbolo = juego.turno.name

    if not juego.jugar(i, j):
        messagebox.showwarning("Movimiento inválido")
        return

    boton.config(text=simbolo, state="disabled")

    resultado = juego.validar_victoria()

    if resultado in (Resultado.VICTORIA_X, Resultado.VICTORIA_O, Resultado.EMPATE):
        match resultado:
            case Resultado.VICTORIA_X:
                text = "¡Felicidades! X ha ganado."
            case Resultado.VICTORIA_O:
                text = "¡Felicidades! O ha ganado."
            case Resultado.EMPATE:
                text = "El juego ha terminado en empate."

        desactivar_tablero(botones)
        messagebox.showinfo("Fin del juego", text)


def main():
    DIMENSION = 800
    PAD = 10
    DIM_BOTON = (DIMENSION - PAD * 4) // 3

    ventana = tk.Tk()
    ventana.title("Hyper Cat")
    ventana.geometry(f"{DIMENSION}x{DIMENSION}")
    ventana.resizable(False, False)

    juego = Gato()
    botones = [[None for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            x = PAD + j * (DIM_BOTON + PAD)
            y = PAD + i * (DIM_BOTON + PAD)

            btn = tk.Button(
                ventana, text="", font=("Arial", 56, "bold"), relief="solid", bd=2
            )

            btn.config(
                command=lambda i=i, j=j, b=btn: click_event_in_button(
                    i, j, b, juego, botones
                )
            )

            btn.place(x=x, y=y, width=DIM_BOTON, height=DIM_BOTON)

            botones[i][j] = btn

    ventana.mainloop()


if __name__ == "__main__":
    main()

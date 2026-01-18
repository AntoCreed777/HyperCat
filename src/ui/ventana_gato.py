import tkinter as tk
from tkinter import messagebox

from core.gato import Gato
from enums import EstadoCasilla, Resultado


class VentanaGato:
    DIM: int = 800
    PAD: int = 10
    BTN: int = (DIM - PAD * 4) // 3

    juego: Gato
    botones: list[list[tk.Button]]
    ventana: tk.Tk

    def __init__(self):
        self.juego = Gato()
        self.botones = [[None] * 3 for _ in range(3)]

        self.ventana = tk.Tk()
        self._configurar()
        self._crear_tablero()

    def _configurar(self):
        self.ventana.title("Gato Normal")
        self.ventana.geometry(f"{self.DIM}x{self.DIM}")
        self.ventana.resizable(False, False)

    def _crear_tablero(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.ventana, font=("Arial", 56, "bold"))

                btn.config(command=lambda i=i, j=j, b=btn: self._click(i, j, b))

                btn.place(
                    x=self.PAD + j * (self.BTN + self.PAD),
                    y=self.PAD + i * (self.BTN + self.PAD),
                    width=self.BTN,
                    height=self.BTN,
                )

                self.botones[i][j] = btn

    def _click(self, i: int, j: int, boton: tk.Button):
        simbolo = self.juego.turno.name

        try:
            self.juego.jugar(i, j)
        except ValueError as e:
            messagebox.showwarning(str(e))
            return

        boton.config(
            text=simbolo,
            state="disabled",
            disabledforeground="blue" if simbolo == EstadoCasilla.X.name else "red",
        )

        resultado = self.juego.validar_victoria()
        if resultado.terminado():
            self._fin_juego(resultado)

    def _fin_juego(self, resultado: Resultado):
        for fila in self.botones:
            for boton in fila:
                boton.config(state="disabled")

        messagebox.showinfo("Fin del juego", resultado.mensaje())

    def run(self):
        self.ventana.mainloop()

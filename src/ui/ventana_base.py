import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox

from core.base_gato import BaseGato
from enums import Colors, EstadoCasilla, Resultado


class VentanaBase(ABC):
    juego: BaseGato
    botones: list[list[tk.Button]]
    ventana: tk.Tk

    cantidad_botones: int

    def __init__(self, juego: BaseGato, titulo: str, cantidad_botones: int = 3):
        self.cantidad_botones = cantidad_botones

        self.DIM: int = 800
        self.PAD: int = 10
        self.BTN: int = (
            self.DIM - self.PAD * (cantidad_botones + 1)
        ) // cantidad_botones

        self.juego = juego()
        self.botones = [[None] * cantidad_botones for _ in range(cantidad_botones)]

        self.ventana = tk.Tk()
        self._configurar(titulo)
        self._crear_tablero()

    def _configurar(self, titulo: str):
        self.ventana.title(titulo)
        self.ventana.geometry(f"{self.DIM}x{self.DIM}")
        self.ventana.resizable(False, False)

    def _crear_tablero(self):
        for i in range(self.cantidad_botones):
            for j in range(self.cantidad_botones):
                btn = tk.Button(
                    self.ventana,
                    font=("Arial", 56, "bold"),
                    activebackground=Colors.ORANGE,
                    bg=self._color_segun_cuadrante(i, j),
                )

                btn.config(command=lambda i=i, j=j, b=btn: self._click(i, j, b))

                btn.place(
                    x=self.PAD + j * (self.BTN + self.PAD),
                    y=self.PAD + i * (self.BTN + self.PAD),
                    width=self.BTN,
                    height=self.BTN,
                )

                self.botones[i][j] = btn

    @abstractmethod
    def _click(self, i: int, j: int, boton: tk.Button):
        pass

    def _fin_juego(self, resultado: Resultado):
        simbolo_ganador = "X" if resultado == Resultado.VICTORIA_X else "O"
        for i in range(self.cantidad_botones):
            for j in range(self.cantidad_botones):
                self.botones[i][j].config(
                    text=simbolo_ganador,
                    state="disabled",
                    disabledforeground=Colors.GOLD,
                    bg=self._color_segun_simbolo(simbolo_ganador),
                )

        messagebox.showinfo("Fin del juego", resultado.mensaje())

    def _bloquear_todos_botones(self):
        for f in range(self.cantidad_botones):
            for c in range(self.cantidad_botones):
                self.botones[f][c].config(
                    state="disabled", bg=self._color_segun_cuadrante(f, c)
                )

    def run(self):
        self.ventana.mainloop()

    def _color_segun_simbolo(self, simbolo: str) -> Colors:
        match simbolo:
            case EstadoCasilla.X.name:
                return Colors.BLUE
            case EstadoCasilla.O.name:
                return Colors.RED
            case _:
                return Colors.BLACK

    def _color_segun_cuadrante(
        self, fila: int, columna: int, activo: bool = False
    ) -> Colors:
        if (fila // 3 + columna // 3) % 2 == 0:
            return Colors.LIGHT_GREEN if activo else Colors.DARK_GREEN
        else:
            return Colors.LIGHT_PINK if activo else Colors.DARK_MAGENTA

    def _bloquear_boton_con_simbolo(self, boton: tk.Button, simbolo: str) -> None:
        boton.config(
            text=simbolo,
            state="disabled",
            disabledforeground=self._color_segun_simbolo(simbolo),
        )

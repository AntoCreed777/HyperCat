import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox
from typing import Type

from core.base_gato import BaseGato
from enums import Colors, EstadoCasilla, Resultado


class VentanaBase(ABC):
    juego: BaseGato
    botones_tablero: list[list[tk.Button]]
    ventana: tk.Tk

    cantidad_botones: int
    turno: tk.Label

    def __init__(self, juego: Type[BaseGato], titulo: str, cantidad_botones: int = 3):
        self.cantidad_botones = cantidad_botones

        self.DIM: int = 800
        self.PAD: int = 10
        self.BTN: int = (
            self.DIM - self.PAD * (cantidad_botones + 1)
        ) // cantidad_botones

        self.juego = juego()
        self.botones_tablero = [
            [None] * cantidad_botones for _ in range(cantidad_botones)
        ]

        self.ventana = tk.Tk()
        self._configurar(titulo)

        # Crear etiqueta de turno actual
        self.turno = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 24, "bold"),
        )
        self.turno.place(relx=0.5, x=0, y=30, anchor="n")

        # Crear boton para reiniciar el juego
        boton_reiniciar = tk.Button(
            self.ventana,
            text="Reiniciar",
            font=("Arial", 12),
            bg=Colors.LIGHT_BLUE,
            activebackground=Colors.BLUE,
            command=self._reiniciar_juego,
        )
        boton_reiniciar.place(relx=0.9, x=0, y=30, anchor="n")

        self._actualizar_turno()
        self._crear_tablero()

    def _configurar(self, titulo: str):
        self.ventana.title(titulo)
        self.ventana.geometry(f"{self.DIM}x{self.DIM + 100}")
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
                    y=self.PAD + i * (self.BTN + self.PAD) + 100,
                    width=self.BTN,
                    height=self.BTN,
                )

                self.botones_tablero[i][j] = btn

    @abstractmethod
    def _click(self, i: int, j: int, boton: tk.Button):
        pass

    def _fin_juego(self, resultado: Resultado):
        self.turno.config(text="Juego terminado", fg=Colors.MEDIUM_ORCHID)

        match resultado:
            case Resultado.VICTORIA_X:
                simbolo_ganador = "X"
            case Resultado.VICTORIA_O:
                simbolo_ganador = "O"
            case Resultado.EMPATE:
                simbolo_ganador = "-"

        for i in range(self.cantidad_botones):
            for j in range(self.cantidad_botones):
                self.botones_tablero[i][j].config(
                    text=simbolo_ganador,
                    state="disabled",
                    disabledforeground=Colors.GOLD,
                    bg=self._color_segun_simbolo(simbolo_ganador),
                )

        messagebox.showinfo("Fin del juego", resultado.mensaje())

    def _bloquear_todos_botones(self):
        for f in range(self.cantidad_botones):
            for c in range(self.cantidad_botones):
                self.botones_tablero[f][c].config(
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

    def _actualizar_turno(self) -> None:
        turno_actual = self.juego.turno.name
        self.turno.config(
            text=f"Turno de: {turno_actual}",
            fg=self._color_segun_simbolo(turno_actual),
        )

    def _reiniciar_juego(self) -> None:
        self.juego.reiniciar()
        self._actualizar_turno()

        for i in range(self.cantidad_botones):
            for j in range(self.cantidad_botones):
                self.botones_tablero[i][j].config(
                    text="",
                    state="normal",
                    bg=self._color_segun_cuadrante(i, j),
                )

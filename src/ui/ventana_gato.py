import tkinter as tk
from tkinter import messagebox
from typing import override

from core.gato import Gato

from .ventana_base import VentanaBase


class VentanaGato(VentanaBase):
    juego: Gato

    def __init__(self):
        super().__init__(Gato, "Gato Normal", cantidad_botones=3)

    @override
    def _click(self, i: int, j: int, boton: tk.Button):
        simbolo = self.juego.turno.name

        try:
            self.juego.jugar(i, j)
        except ValueError as e:
            messagebox.showwarning(str(e))
            return

        self._bloquear_boton_con_simbolo(boton, simbolo)

        resultado = self.juego.validar_victoria()
        if resultado.terminado():
            self._fin_juego(resultado)

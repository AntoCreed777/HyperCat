"""Módulo con la ventana del juego de Gato clásico."""

import tkinter as tk
from tkinter import messagebox
from typing import override

from core.exceptions_custom import *
from core.gato import Gato

from .ventana_base import VentanaBase


class VentanaGato(VentanaBase):
    """
    Clase que representa la ventana del juego de Gato clásico.

    Esta clase maneja la interfaz de usuario para el juego de Gato tradicional.
    """

    juego: Gato

    def __init__(self):
        """Inicializa la ventana del juego de Gato."""
        super().__init__(Gato, "Gato Normal", cantidad_botones=3)

    @override
    def _click(self, i: int, j: int, boton: tk.Button):
        """
        Maneja el evento de clic en un botón del tablero.

        Args:
            i: El índice de la fila del botón clickeado.
            j: El índice de la columna del botón clickeado.
            boton: El botón que fue clickeado.
        """
        simbolo = self.juego.turno.name

        try:
            self.juego.jugar(i, j)

        except MovimientoInvalidoError as e:
            messagebox.showwarning("Movimiento inválido")
            return

        except JuegoTerminadoError:
            messagebox.showinfo("Fin del juego", "El juego ya terminó.")
            return

        except GatoError as e:
            messagebox.showerror("Error", str(e))
            return

        self._bloquear_boton_con_simbolo(boton, simbolo)

        resultado = self.juego.validar_victoria()
        if resultado.terminado():
            self._fin_juego(resultado)
        else:
            self._actualizar_turno()

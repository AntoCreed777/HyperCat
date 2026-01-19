import tkinter as tk
from tkinter import messagebox
from typing import override

from core.exceptions_custom import *
from core.hyper_cat import HyperCat
from enums import Resultado

from .ventana_base import VentanaBase


class VentanaHyperCat(VentanaBase):
    juego: HyperCat

    def __init__(self):
        super().__init__(HyperCat, "Hyper Cat", cantidad_botones=9)

    @override
    def _click(self, i: int, j: int, boton: tk.Button):

        fila = i // 3
        columna = j // 3
        sub_fila = i % 3
        sub_columna = j % 3

        simbolo = self.juego.turno.name

        try:
            self.juego.jugar(
                subfila=sub_fila, subcolumna=sub_columna, fila=fila, columna=columna
            )

        except MovimientoInvalidoError as e:
            messagebox.showwarning("Movimiento inválido", str(e))
            return

        except JuegoTerminadoError:
            messagebox.showinfo("Fin del juego", "El juego ya ha terminado.")
            return

        except GatoError as e:
            messagebox.showerror("Error del juego", str(e))
            return

        # Actualizar el botón presionado
        self._bloquear_boton_con_simbolo(boton, simbolo)

        # Bloquear todos los botones primero
        self._bloquear_todos_botones()

        # Habilitar los botones del siguiente sub-juego si no se puede elegir cualquiera
        if not self.juego.elegir_cualquiera:
            siguiente_fila, siguiente_columna = self.juego.gato_a_jugar_despues
            self._activar_botones_no_ocupados_sub_juego(
                siguiente_fila, siguiente_columna
            )
        # Si se puede elegir cualquier sub-juego, habilitar los que no estén terminados
        else:
            self._activar_botones_no_ocupados()

        # Validar si el sub-juego ha terminado
        sub_juego_resultado = self.juego.tablero[fila][columna].validar_victoria()
        match sub_juego_resultado:
            case Resultado.VICTORIA_X:
                for sub_i in range(3):
                    for sub_j in range(3):
                        btn = self.botones[fila * 3 + sub_i][columna * 3 + sub_j]
                        self._bloquear_boton_con_simbolo(btn, "X")
            case Resultado.VICTORIA_O:
                for sub_i in range(3):
                    for sub_j in range(3):
                        btn = self.botones[fila * 3 + sub_i][columna * 3 + sub_j]
                        self._bloquear_boton_con_simbolo(btn, "O")
            case Resultado.EMPATE:
                self.juego.tablero[fila][columna].reiniciar()
                for sub_i in range(3):
                    for sub_j in range(3):
                        btn = self.botones[fila * 3 + sub_i][columna * 3 + sub_j]
                        btn.config(text="")

        resultado = self.juego.validar_victoria()
        if resultado.terminado():
            self._fin_juego(resultado)

    def _activar_botones_no_ocupados(self):
        for fila_sub_gato in range(3):
            for columna_sub_gato in range(3):
                self._activar_botones_no_ocupados_sub_juego(
                    fila_sub_gato, columna_sub_gato
                )

    def _activar_botones_no_ocupados_sub_juego(
        self, fila_sub_gato: int, columna_sub_gato: int
    ):
        for i in range(3):
            for j in range(3):
                sub_juego = self.juego.tablero[fila_sub_gato][columna_sub_gato]
                if not sub_juego.terminado():
                    ocupado = sub_juego.tablero[i][j].ocupada()
                    state = "disabled" if ocupado else "normal"
                    bg = self._color_segun_cuadrante(
                        fila_sub_gato * 3 + i,
                        columna_sub_gato * 3 + j,
                        activo=ocupado is False,
                    )
                    self.botones[fila_sub_gato * 3 + i][
                        columna_sub_gato * 3 + j
                    ].config(state=state, bg=bg)

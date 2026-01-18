import tkinter as tk
from tkinter import messagebox

from core.hyper_cat import HyperCat
from enums import EstadoCasilla, Resultado


class VentanaHyperCat:
    DIM: int = 800
    PAD: int = 10
    BTN: int = (DIM - PAD * 10) // 9

    juego: HyperCat
    botones: list[list[tk.Button]]
    ventana: tk.Tk

    def __init__(self):
        self.juego = HyperCat()
        self.botones = [[None] * 9 for _ in range(9)]

        self.ventana = tk.Tk()
        self._configurar()
        self._crear_tablero()

    def _configurar(self):
        self.ventana.title("Hyper Cat")
        self.ventana.geometry(f"{self.DIM}x{self.DIM}")
        self.ventana.resizable(False, False)

    def _crear_tablero(self):
        for i in range(9):
            for j in range(9):
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

        fila = i // 3
        columna = j // 3
        sub_fila = i % 3
        sub_columna = j % 3

        simbolo = self.juego.turno.name

        try:
            self.juego.jugar(
                subfila=sub_fila, subcolumna=sub_columna, fila=fila, columna=columna
            )
        except Exception as e:
            messagebox.showwarning(str(e))
            return

        # Actualizar el botón presionado
        boton.config(
            text=simbolo,
            state="disabled",
            disabledforeground="blue" if simbolo == EstadoCasilla.X.name else "red",
        )

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
                        btn.config(
                            text="X", state="disabled", disabledforeground="blue"
                        )
            case Resultado.VICTORIA_O:
                for sub_i in range(3):
                    for sub_j in range(3):
                        btn = self.botones[fila * 3 + sub_i][columna * 3 + sub_j]
                        btn.config(text="O", state="disabled", disabledforeground="red")
            case Resultado.EMPATE:
                self.juego.tablero[fila][columna].reiniciar()
                for sub_i in range(3):
                    for sub_j in range(3):
                        btn = self.botones[fila * 3 + sub_i][columna * 3 + sub_j]
                        btn.config(text="")

        resultado = self.juego.validar_victoria()
        if resultado.terminado():
            self._fin_juego(resultado)

    def _fin_juego(self, resultado: Resultado):
        for fila in self.botones:
            for boton in fila:
                boton.config(state="disabled")

        messagebox.showinfo("Fin del juego", resultado.mensaje())

    def _bloquear_todos_botones(self):
        for fila in self.botones:
            for boton in fila:
                boton.config(state="disabled")

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
                    state = (
                        "disabled" if sub_juego.tablero[i][j].ocupada() else "normal"
                    )
                    self.botones[fila_sub_gato * 3 + i][
                        columna_sub_gato * 3 + j
                    ].config(state=state)

    def run(self):
        self.ventana.mainloop()

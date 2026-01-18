import tkinter as tk
from tkinter import messagebox

from core.hyper_cat import HyperCat
from enums import Colors, EstadoCasilla, Resultado


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
            messagebox.showwarning("Movimiento inválido", str(e))

            return

        # Actualizar el botón presionado
        boton.config(
            text=simbolo,
            state="disabled",
            disabledforeground=self._color_segun_simbolo(simbolo),
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
                        simbolo = "X"
                        btn.config(
                            text=simbolo,
                            state="disabled",
                            disabledforeground=self._color_segun_simbolo(simbolo),
                        )
            case Resultado.VICTORIA_O:
                for sub_i in range(3):
                    for sub_j in range(3):
                        btn = self.botones[fila * 3 + sub_i][columna * 3 + sub_j]
                        simbolo = "O"
                        btn.config(
                            text=simbolo,
                            state="disabled",
                            disabledforeground=self._color_segun_simbolo(simbolo),
                        )
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
        simbolo_ganador = "X" if resultado == Resultado.VICTORIA_X else "O"
        for i in range(9):
            for j in range(9):
                self.botones[i][j].config(
                    text=simbolo_ganador,
                    state="disabled",
                    disabledforeground=Colors.GOLD,
                    bg=self._color_segun_simbolo(simbolo_ganador),
                )

        messagebox.showinfo("Fin del juego", resultado.mensaje())

    def _bloquear_todos_botones(self):
        for f in range(9):
            for c in range(9):
                self.botones[f][c].config(
                    state="disabled", bg=self._color_segun_cuadrante(f, c)
                )

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

"""Ventana visual paso a paso para Gauss y Gauss-Jordan."""

import tkinter as tk
from tkinter import ttk

from interfaces.ventana_matriz import crear_matriz_visual


class VentanaProceso:
    """Presenta una operación de fila a la vez con una matriz visual."""

    def __init__(self, parent, pasos, numero_variables, titulo="Procedimiento • Paso a paso"):
        self.pasos = pasos
        self.numero_variables = numero_variables
        self.indice = 0
        self.titulo_ventana = titulo

        self.ventana = tk.Toplevel(parent)
        self.ventana.title(self.titulo_ventana)
        self.ventana.geometry("900x700")
        self.ventana.minsize(760, 600)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.construir()
        self.mostrar_paso()

    def construir(self):
        contenedor = ttk.Frame(self.ventana, padding=24)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Procedimiento de reducción por filas",
            style="PageTitle.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            contenedor,
            text="Cada paso muestra la operación elemental y la matriz resultante, como en el procedimiento escrito a mano.",
            style="ProcessSubtitle.TLabel",
            wraplength=820,
        ).pack(anchor="w", pady=(4, 8))

        self.progreso = ttk.Label(
            contenedor, text="", style="ProcessSubtitle.TLabel"
        )
        self.progreso.pack(anchor="w", pady=(0, 14))

        tarjeta = ttk.Frame(contenedor, style="Card.TFrame", padding=22)
        tarjeta.pack(fill="both", expand=True)

        self.titulo = ttk.Label(
            tarjeta, text="", style="SectionTitle.TLabel"
        )
        self.titulo.pack(anchor="w")

        self.operacion = ttk.Label(
            tarjeta, text="", style="Operation.TLabel", wraplength=780
        )
        self.operacion.pack(anchor="w", pady=(8, 16))

        self.matriz_area = ttk.Frame(tarjeta, style="Matrix.TFrame", padding=18)
        self.matriz_area.pack(fill="both", expand=True)

        navegacion = ttk.Frame(contenedor)
        navegacion.pack(fill="x", pady=(16, 0))

        self.boton_anterior = ttk.Button(
            navegacion, text="← Anterior", command=self.anterior
        )
        self.boton_anterior.pack(side="left")

        ttk.Button(
            navegacion, text="Cerrar", command=self.ventana.destroy
        ).pack(side="right", padx=(10, 0))

        self.boton_siguiente = ttk.Button(
            navegacion, text="Siguiente →",
            style="Accent.TButton", command=self.siguiente
        )
        self.boton_siguiente.pack(side="right")

    def mostrar_paso(self):
        paso = self.pasos[self.indice]
        self.progreso.config(
            text=f"Paso {self.indice + 1} de {len(self.pasos)}"
        )
        self.titulo.config(text=paso["titulo"])
        self.operacion.config(text=f"Operación: {paso['operacion']}")

        for widget in self.matriz_area.winfo_children():
            widget.destroy()

        matriz = crear_matriz_visual(
            self.matriz_area, paso["matriz"], self.numero_variables
        )
        matriz.pack(anchor="center", pady=15)

        if self.indice == 0:
            self.boton_anterior.state(["disabled"])
        else:
            self.boton_anterior.state(["!disabled"])

        if self.indice == len(self.pasos) - 1:
            self.boton_siguiente.state(["disabled"])
        else:
            self.boton_siguiente.state(["!disabled"])

    def siguiente(self):
        if self.indice < len(self.pasos) - 1:
            self.indice += 1
            self.mostrar_paso()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_paso()

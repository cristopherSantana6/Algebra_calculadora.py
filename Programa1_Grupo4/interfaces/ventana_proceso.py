"""Ventana de visualización paso a paso del algoritmo de Gauss."""

import tkinter as tk
from tkinter import ttk

from utilidades.formato import formatear_matriz_lineas


class VentanaProceso:
    """Presenta una operación de fila a la vez."""

    def __init__(self, parent, pasos, numero_variables):
        self.pasos = pasos
        self.numero_variables = numero_variables
        self.indice = 0

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Proceso Gaussiano • Paso a paso")
        self.ventana.geometry("800x650")
        self.ventana.minsize(680, 540)
        self.ventana.transient(parent)
        self.ventana.grab_set()

        self.construir()
        self.mostrar_paso()

    def construir(self):
        contenedor = ttk.Frame(self.ventana, padding=24)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Proceso de Eliminación por Filas",
            style="PageTitle.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            contenedor,
            text="Operaciones y resultados mostrados con fracciones exactas.",
            style="CardSubtitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        self.progreso = ttk.Label(
            contenedor,
            text="",
            style="CardSubtitle.TLabel",
        )
        self.progreso.pack(anchor="w", pady=(4, 18))

        tarjeta = ttk.Frame(contenedor, style="Card.TFrame", padding=20)
        tarjeta.pack(fill="both", expand=True)

        self.titulo = ttk.Label(
            tarjeta,
            text="",
            style="SectionTitle.TLabel",
        )
        self.titulo.pack(anchor="w")

        self.operacion = ttk.Label(
            tarjeta,
            text="",
            style="Operation.TLabel",
            wraplength=680,
        )
        self.operacion.pack(anchor="w", pady=(8, 18))

        marco = ttk.Frame(tarjeta, style="Matrix.TFrame", padding=18)
        marco.pack(fill="both", expand=True)

        self.matriz_texto = tk.Text(
            marco,
            height=12,
            font=("Consolas", 12),
            relief="flat",
            borderwidth=0,
            bg="#F7F9FA",
            fg="#23343A",
            state="disabled",
        )
        self.matriz_texto.pack(fill="both", expand=True)

        navegacion = ttk.Frame(contenedor)
        navegacion.pack(fill="x", pady=(16, 0))

        self.boton_anterior = ttk.Button(
            navegacion,
            text="← Anterior",
            command=self.anterior,
        )
        self.boton_anterior.pack(side="left")

        self.boton_siguiente = ttk.Button(
            navegacion,
            text="Siguiente →",
            style="Accent.TButton",
            command=self.siguiente,
        )
        self.boton_siguiente.pack(side="right")

        ttk.Button(
            navegacion,
            text="Cerrar",
            command=self.ventana.destroy,
        ).pack(side="right", padx=(0, 10))

    def mostrar_paso(self):
        paso = self.pasos[self.indice]
        self.progreso.config(text=f"Paso {self.indice + 1} de {len(self.pasos)}")
        self.titulo.config(text=paso["titulo"])
        self.operacion.config(text=paso["operacion"])

        self.matriz_texto.config(state="normal")
        self.matriz_texto.delete("1.0", "end")
        for linea in formatear_matriz_lineas(paso["matriz"], self.numero_variables):
            self.matriz_texto.insert("end", linea + "\n")
        self.matriz_texto.config(state="disabled")

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

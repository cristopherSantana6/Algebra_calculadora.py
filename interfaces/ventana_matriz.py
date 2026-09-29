"""Componentes para mostrar matrices y procedimientos de forma visual."""

import tkinter as tk
from tkinter import ttk

from utilidades.fracciones import formatear_fraccion


def crear_matriz_visual(parent, matriz, numero_variables=None, cell_width=76, pad=2):
    """Crea una matriz usando celdas visibles en lugar de texto monoespaciado."""
    contenedor = ttk.Frame(parent, style="Matrix.TFrame")
    columnas = max((len(fila) for fila in matriz), default=0)
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if numero_variables is not None and len(fila) > numero_variables:
                if j == numero_variables:
                    ttk.Label(
                        contenedor, text="│", style="MatrixSeparator.TLabel",
                        font=("Cambria Math", 17, "bold")
                    ).grid(row=i, column=j * 2 - 1, padx=(6, 4), pady=pad)
                    col = j * 2
                elif j > numero_variables:
                    col = j * 2
                else:
                    col = j * 2
            else:
                col = j
            etiqueta = ttk.Label(
                contenedor,
                text=formatear_fraccion(valor),
                style="MatrixCell.TLabel",
                width=max(5, int(cell_width / 10)),
                anchor="center",
                padding=(8, 7),
            )
            etiqueta.grid(row=i, column=col, padx=2, pady=pad, sticky="nsew")
    return contenedor


def crear_vector_visual(parent, vector, titulo=None, vertical=True):
    """Muestra un vector como columna matemática."""
    marco = ttk.Frame(parent, style="Card.TFrame")
    if titulo:
        ttk.Label(marco, text=titulo, style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 6))
    if vertical:
        cuerpo = ttk.Frame(marco, style="Matrix.TFrame", padding=8)
        cuerpo.pack(anchor="w")
        for i, valor in enumerate(vector):
            ttk.Label(
                cuerpo, text=formatear_fraccion(valor),
                style="MatrixCell.TLabel", width=8, anchor="center",
                padding=(8, 6)
            ).grid(row=i, column=0, padx=2, pady=2)
    else:
        cuerpo = ttk.Frame(marco, style="Matrix.TFrame", padding=8)
        cuerpo.pack(anchor="w")
        for i, valor in enumerate(vector):
            ttk.Label(
                cuerpo, text=formatear_fraccion(valor),
                style="MatrixCell.TLabel", width=8, anchor="center",
                padding=(8, 6)
            ).grid(row=0, column=i, padx=2, pady=2)
    return marco

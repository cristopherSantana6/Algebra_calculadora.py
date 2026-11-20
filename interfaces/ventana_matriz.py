"""Renderizado adaptable y reutilizable de matrices y vectores en Tkinter."""

from fractions import Fraction
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


def _medidas_matriz(matriz):
    """Devuelve anchos máximos por columna (caracteres) y altos por fila."""
    columnas = max((len(fila) for fila in matriz), default=0)
    anchos = [1] * columnas
    alturas = []
    for fila in matriz:
        alto = 24
        for j, valor in enumerate(fila):
            numero = valor if isinstance(valor, Fraction) else Fraction(valor)
            numerador = str(numero.numerator)
            denominador = str(numero.denominator) if numero.denominator != 1 else ""
            anchos[j] = max(anchos[j], len(numerador), len(denominador))
            if denominador:
                alto = max(alto, 42)
        alturas.append(alto)
    return anchos, alturas


def crear_matriz_visual(parent, matriz, numero_variables=None, cell_width=None, pad=2):
    """Dibuja una matriz en un canvas medido al contenido, con scroll en ambos ejes.

    El ancho se mide con la fuente matemática activa; las fracciones se dibujan
    en dos líneas. `cell_width` queda aceptado por compatibilidad con llamadas
    existentes, pero el contenido determina el tamaño de cada columna.
    """
    contenedor = ttk.Frame(parent, style="Matrix.TFrame")
    columnas = max((len(fila) for fila in matriz), default=0)
    if not columnas:
        return contenedor

    estilo = ttk.Style()
    color = estilo.lookup("MatrixCell.TLabel", "foreground") or "#263238"
    fondo = estilo.lookup("Matrix.TFrame", "background") or "#ffffff"
    fondo_celda = estilo.lookup("MatrixCell.TLabel", "background") or "#ffffff"
    fuente_config = estilo.lookup("MatrixCell.TLabel", "font")
    fuente = tkfont.Font(root=parent, font=fuente_config) if fuente_config else tkfont.nametofont("TkDefaultFont")
    alto_linea = fuente.metrics("linespace")
    # En algunos Windows Cambria Math reporta una caja de línea de 80+ px para
    # 11 pt. Ese dato deja filas enormes; Cambria conserva el aspecto matemático
    # y proporciona métricas normales para colocar cifras y barras.
    if alto_linea > max(36, abs(int(fuente.actual("size"))) * 3):
        fuente.configure(family="Cambria")
        alto_linea = fuente.metrics("linespace")

    datos = [[valor if isinstance(valor, Fraction) else Fraction(valor) for valor in fila] for fila in matriz]
    anchos = [52] * columnas
    altos = []
    for fila in datos:
        alto = max(36, alto_linea + 14)
        for j, valor in enumerate(fila):
            arriba = str(valor.numerator)
            abajo = str(valor.denominator) if valor.denominator != 1 else ""
            anchos[j] = max(anchos[j], fuente.measure(arriba) + 18,
                            fuente.measure(abajo) + 18 if abajo else 0)
            if abajo:
                alto = max(alto, alto_linea * 2 + 16)
        altos.append(alto)

    canvas = tk.Canvas(contenedor, background=fondo, highlightthickness=0, bd=0)
    barra_x = ttk.Scrollbar(contenedor, orient="horizontal", command=canvas.xview)
    barra_y = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    canvas.configure(xscrollcommand=barra_x.set, yscrollcommand=barra_y.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    barra_y.grid(row=0, column=1, sticky="ns")
    barra_x.grid(row=1, column=0, sticky="ew")
    contenedor.rowconfigure(0, weight=1)
    contenedor.columnconfigure(0, weight=1)

    margen = 10
    alto_matriz = sum(altos)
    x_inicial = margen + 14
    y = margen
    x_derecho = x_inicial
    for i, fila in enumerate(datos):
        alto = altos[i]
        x = x_inicial
        for j, valor in enumerate(fila):
            if numero_variables is not None and j == numero_variables:
                canvas.create_line(x + 4, y + 3, x + 4, y + alto - 3, fill=color, width=2)
                x += 14
            ancho = anchos[j]
            canvas.create_rectangle(x, y, x + ancho, y + alto,
                                    fill=fondo_celda, outline=color, width=1)
            centro_x, centro_y = x + ancho / 2, y + alto / 2
            numerador = str(valor.numerator)
            if valor.denominator == 1:
                canvas.create_text(centro_x, centro_y, text=numerador, fill=color, font=fuente)
            else:
                denominador = str(valor.denominator)
                canvas.create_text(centro_x, centro_y - alto_linea / 2,
                                   text=numerador, fill=color, font=fuente)
                canvas.create_line(x + 6, centro_y, x + ancho - 6, centro_y,
                                   fill=color, width=1)
                canvas.create_text(centro_x, centro_y + alto_linea / 2,
                                   text=denominador, fill=color, font=fuente)
            x += ancho + 10
        x_derecho = max(x_derecho, x - 10)
        y += alto

    # Corchetes escalados a la altura total, también cuando haya que desplazarse.
    canvas.create_line(margen + 10, margen, margen + 3, margen,
                       margen + 3, margen + alto_matriz, margen + 10,
                       margen + alto_matriz, fill=color, width=2)
    canvas.create_line(x_derecho + 2, margen, x_derecho + 9, margen,
                       x_derecho + 9, margen + alto_matriz, x_derecho + 2,
                       margen + alto_matriz, fill=color, width=2)
    ancho_total = x_derecho + 18
    alto_total = alto_matriz + margen * 2
    canvas.configure(scrollregion=(0, 0, ancho_total, alto_total))
    canvas.configure(width=min(max(ancho_total, 180), 680),
                     height=min(max(alto_total, 52), 380))
    return contenedor


def crear_vector_visual(parent, vector, titulo=None, vertical=True):
    """Construye una representación adaptable de un vector."""
    marco = ttk.Frame(parent, style="Card.TFrame")
    if titulo:
        ttk.Label(marco, text=titulo, style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 6))
    matriz = [[valor] for valor in vector] if vertical else [list(vector)]
    crear_matriz_visual(marco, matriz).pack(anchor="w")
    return marco

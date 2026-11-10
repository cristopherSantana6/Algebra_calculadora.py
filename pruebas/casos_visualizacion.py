"""Pruebas de estrés de los tamaños matemáticos y del componente Tkinter."""

import tkinter as tk
import sys
from fractions import Fraction

from interfaces.ventana_matriz import _medidas_matriz, crear_matriz_visual
from modulos.modulo_lu import factorizar_lu, verificar_factorizacion
from modulos.modulo_matrices import (
    determinante_reduccion,
    inversa_gauss_jordan,
    multiplicar_matrices,
)


def matriz_estres(n):
    """Construye una matriz triangular exacta, no singular y con fracciones."""
    return [
        [
            Fraction(i + 2) if i == j else Fraction(i + 1, j + 2) if i > j else Fraction(0)
            for j in range(n)
        ]
        for i in range(n)
    ]


def probar_calculos():
    for n in (2, 3, 5, 8, 10):
        matriz = matriz_estres(n)
        lu = factorizar_lu(matriz)
        assert verificar_factorizacion(matriz, lu["matriz_L"], lu["matriz_U"])["es_correcta"]
        determinante_esperado = Fraction(1)
        for diagonal in range(2, n + 2):
            determinante_esperado *= diagonal
        assert determinante_reduccion(matriz)["determinante"] == determinante_esperado
        inversa = inversa_gauss_jordan(matriz)["inversa"]
        identidad = [[Fraction(i == j) for j in range(n)] for i in range(n)]
        assert multiplicar_matrices(matriz, inversa) == identidad
    print("✓ Cálculos exactos y LU/inversa/determinante: tamaños 2, 3, 5, 8 y 10")


def probar_medicion_y_tk():
    grande = Fraction(-123456789012345, 987654321098765)
    matriz = [[Fraction(0), Fraction(1, 2)], [grande, Fraction(-9876543210123456789, 7)]]
    anchos, alturas = _medidas_matriz(matriz)
    assert anchos == [15, 20]
    assert alturas == [42, 42]

    root = tk.Tk()
    root.geometry("720x520")
    for n in (2, 3, 5, 8, 10):
        frame = crear_matriz_visual(root, matriz_estres(n))
        frame.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()
        canvas = next(w for w in frame.winfo_children() if isinstance(w, tk.Canvas))
        region = tuple(map(float, canvas.cget("scrollregion").split()))
        assert region[2] > region[0] and region[3] > region[1]
        assert canvas.winfo_width() > 0 and canvas.winfo_height() > 0
        assert len(canvas.find_all()) >= n * n * 2  # celda y valor, como mínimo
        frame.destroy()

    matriz_ancha = [
        [Fraction(10 ** 35 + i, 10 ** 18 + j) for j in range(8)]
        for i in range(8)
    ]
    frame = crear_matriz_visual(root, matriz_ancha)
    frame.pack(fill="both", expand=True)
    root.update_idletasks()
    root.update()
    canvas = next(w for w in frame.winfo_children() if isinstance(w, tk.Canvas))
    inicio = canvas.xview()[0]
    canvas.xview_moveto(1.0)
    root.update_idletasks()
    assert canvas.xview()[0] > inicio
    root.destroy()
    print("✓ Tkinter: matrices 2×2 a 10×10, celdas dibujadas y scroll horizontal comprobado")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    probar_calculos()
    probar_medicion_y_tk()

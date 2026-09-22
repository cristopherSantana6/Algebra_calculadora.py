"""Operaciones básicas con matrices usando únicamente Python estándar."""

from fractions import Fraction


def validar_matriz(matriz):
    """Comprueba que la lista represente una matriz rectangular no vacía."""
    if not matriz or not matriz[0]:
        raise ValueError("La matriz no puede estar vacía.")
    columnas = len(matriz[0])
    if any(len(fila) != columnas for fila in matriz):
        raise ValueError("La matriz debe ser rectangular.")


def validar_mismas_dimensiones(a, b):
    """Comprueba que A y B tengan el mismo orden; requisito algebraico para A+B y A-B."""
    validar_matriz(a)
    validar_matriz(b)
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones.")


def sumar_matrices(a, b):
    """Calcula A+B sumando cada par de entradas correspondientes."""
    validar_mismas_dimensiones(a, b)
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def restar_matrices(a, b):
    """Calcula A-B restando cada par de entradas correspondientes."""
    validar_mismas_dimensiones(a, b)
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def multiplicar_matriz_escalar(a, escalar):
    """Calcula cA multiplicando cada entrada de A por el escalar c."""
    validar_matriz(a)
    return [[escalar * valor for valor in fila] for fila in a]


def multiplicar_matrices(a, b):
    """Calcula AB mediante bucles anidados: C_ij=sum(A_ik*B_kj).
    La condición algebraica m×n por n×p exige que columnas de A=filas de B."""
    validar_matriz(a)
    validar_matriz(b)
    filas_a, columnas_a = len(a), len(a[0])
    filas_b, columnas_b = len(b), len(b[0])
    if columnas_a != filas_b:
        raise ValueError(
            "No se pueden multiplicar: las columnas de A deben ser iguales a las filas de B."
        )

    resultado = []
    for i in range(filas_a):
        fila_resultado = []
        for j in range(columnas_b):
            suma = Fraction(0)
            for k in range(columnas_a):
                suma += a[i][k] * b[k][j]
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado

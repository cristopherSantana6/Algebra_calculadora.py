"""Casos de prueba del Programa 3 con aritmética racional exacta."""

from fractions import Fraction

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)
from algoritmos.matrices import (
    multiplicar_matrices,
    multiplicar_matriz_escalar,
    restar_matrices,
    sumar_matrices,
)
from algoritmos.vectores import (
    es_combinacion_lineal,
    multiplicar_escalar,
    restar_vectores,
    sumar_vectores,
)
from utilidades.fracciones import formatear_fraccion, leer_fraccion


def ejecutar_casos():
    """Ejecuta las pruebas principales exigidas por el módulo de vectores y matrices."""

    # Sistema Ax=b: también valida la funcionalidad que ya tenía el Programa 1.
    matriz = [
        [Fraction(2), Fraction(-1), Fraction(1), Fraction(3)],
        [Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
        [Fraction(1), Fraction(2), Fraction(-1), Fraction(2)],
    ]
    escalonada, pivotes, inconsistente, pasos = eliminacion_gaussiana(matriz, 3)
    clasificacion, _ = obtener_clasificacion(escalonada, 3, pivotes, inconsistente)
    assert clasificacion == "unica" and pasos
    solucion = resolver_solucion_unica(escalonada, 3, pivotes)
    assert verificar_solucion(matriz, solucion)
    print("✓ Ax=b: solución única y verificación correctas")

    # Vectores.
    a = [Fraction(1), Fraction(2), Fraction(3)]
    b = [Fraction(4), Fraction(5), Fraction(6)]
    assert sumar_vectores(a, b) == [Fraction(5), Fraction(7), Fraction(9)]
    assert restar_vectores(a, b) == [Fraction(-3), Fraction(-3), Fraction(-3)]
    assert multiplicar_escalar(a, Fraction(2)) == [Fraction(2), Fraction(4), Fraction(6)]
    print("✓ Vectores: suma, resta y escalar correctos")

    generadores = [
        [Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(1), Fraction(1)],
    ]
    combinado = [Fraction(2), Fraction(3), Fraction(5)]
    no_combinado = [Fraction(1), Fraction(1), Fraction(3)]
    assert es_combinacion_lineal(generadores, combinado)["es_combinacion"]
    assert not es_combinacion_lineal(generadores, no_combinado)["es_combinacion"]
    print("✓ Combinación lineal: casos sí/no correctos")

    # Matrices.
    A = [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]]
    B = [[Fraction(5), Fraction(6)], [Fraction(7), Fraction(8)]]
    assert sumar_matrices(A, B) == [[6, 8], [10, 12]]
    assert restar_matrices(A, B) == [[-4, -4], [-4, -4]]
    assert multiplicar_matriz_escalar(A, Fraction(2)) == [[2, 4], [6, 8]]
    assert multiplicar_matrices(A, B) == [[19, 22], [43, 50]]
    try:
        multiplicar_matrices([[1, 2, 3]], [[1, 2], [3, 4]])
        raise AssertionError("Debió rechazar dimensiones incompatibles.")
    except ValueError:
        pass
    print("✓ Matrices: suma, resta, escalar y multiplicación correctas")
    print("✓ Matrices: validación de dimensiones incompatibles correcta")

    # Fracciones exactas.
    assert leer_fraccion("1/2") == Fraction(1, 2)
    assert leer_fraccion("-5/8") == Fraction(-5, 8)
    assert leer_fraccion("0.25") == Fraction(1, 4)
    print("✓ Lectura de fracciones y decimales correcta")


if __name__ == "__main__":
    ejecutar_casos()

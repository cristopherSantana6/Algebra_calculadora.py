"""Casos de prueba del Programa 3 con aritmética racional exacta."""

from fractions import Fraction

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    gauss_jordan,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)
from algoritmos.matrices import (
    multiplicar_matrices,
    multiplicar_matriz_vector,
    multiplicar_matriz_escalar,
    restar_matrices,
    sumar_matrices,
)
from algoritmos.vectores import (
    analizar_dependencia_lineal,
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

    reducida, pivotes_j, inconsistente_j, pasos_j = gauss_jordan(matriz, 3)
    assert not inconsistente_j and len(pivotes_j) == 3 and pasos_j
    solucion_j = [reducida[fila][3] for fila, _ in pivotes_j]
    assert verificar_solucion(matriz, solucion_j)
    assert any("÷" in paso["operacion"] for paso in pasos_j)
    print("✓ Gauss-Jordan: forma reducida, solución y formato de división correctos")

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

    independientes = analizar_dependencia_lineal([
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ])
    dependientes = analizar_dependencia_lineal([
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ])
    assert independientes["independiente"]
    assert not dependientes["independiente"]
    assert dependientes["relacion"] == [Fraction(-2), Fraction(1)]
    print("✓ Dependencia lineal: conjuntos independientes y dependientes correctos")

    # Matrices.
    A = [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]]
    B = [[Fraction(5), Fraction(6)], [Fraction(7), Fraction(8)]]
    assert sumar_matrices(A, B) == [[6, 8], [10, 12]]
    assert restar_matrices(A, B) == [[-4, -4], [-4, -4]]
    assert multiplicar_matriz_escalar(A, Fraction(2)) == [[2, 4], [6, 8]]
    assert multiplicar_matrices(A, B) == [[19, 22], [43, 50]]
    u = [Fraction(4), Fraction(-1)]
    v = [Fraction(-3), Fraction(5)]
    assert multiplicar_matriz_vector(A, [u[0] + v[0], u[1] + v[1]]) == [Fraction(9), Fraction(19)]
    assert [x + y for x, y in zip(multiplicar_matriz_vector(A, u), multiplicar_matriz_vector(A, v))] == [Fraction(9), Fraction(19)]
    print("✓ Producto matriz–vector y propiedad distributiva correctos")
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


    # Casos del I Corte: distributividad y producto matriz-vector.
    A_ex1 = [
        [Fraction(1, 2), Fraction(1, 3)],
        [Fraction(-1, 3), Fraction(1, 2)],
    ]
    u_ex1 = [Fraction(1), Fraction(0)]
    v_ex1 = [Fraction(0), Fraction(1)]
    suma_ex1 = sumar_vectores(u_ex1, v_ex1)
    izquierda_ex1 = multiplicar_matriz_vector(A_ex1, suma_ex1)
    derecha_ex1 = sumar_vectores(
        multiplicar_matriz_vector(A_ex1, u_ex1),
        multiplicar_matriz_vector(A_ex1, v_ex1),
    )
    assert izquierda_ex1 == derecha_ex1
    print("✓ I Corte: propiedad distributiva A(u+v)=Au+Av correcta")

    A_ex3 = [
        [Fraction(1, 2), Fraction(0), Fraction(1, 3)],
        [Fraction(0), Fraction(1, 2), Fraction(1, 3)],
        [Fraction(1, 3), Fraction(1, 3), Fraction(0)],
    ]
    v_ex3 = [Fraction(1), Fraction(1), Fraction(1)]
    producto_ex3 = multiplicar_matriz_vector(A_ex3, v_ex3)
    assert producto_ex3 == [Fraction(5, 6), Fraction(5, 6), Fraction(2, 3)]
    columnas_ex3 = [[fila[j] for fila in A_ex3] for j in range(3)]
    combinado_ex3 = [sum(v_ex3[j] * columnas_ex3[j][i] for j in range(3)) for i in range(3)]
    assert combinado_ex3 == producto_ex3
    print("✓ I Corte: A·v y combinación lineal de columnas correctas")


if __name__ == "__main__":
    ejecutar_casos()

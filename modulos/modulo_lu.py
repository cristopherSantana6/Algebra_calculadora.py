"""Factorización LU (A = LU) y solución de Ax = b por sustitución hacia adelante y hacia atrás.

Obtiene U con operaciones de reemplazo de fila (Fᵢ ← Fᵢ − l·Fⱼ), registra cada multiplicador l en L,
verifica L·U == A y resuelve Ly = b y Ux = y reutilizando Gauss-Jordan y el producto de modulo_matrices.
Funciones puras: reciben listas anidadas y devuelven resultados, sin input() ni print().
Unidad: Programa 6 de Álgebra Lineal (MTM0120), Universidad Americana.
Elaborado por: Rafael Antonio Arauz Navarro, Patricia del Carmen Oquist Talavera,
Cristopher Rafael Santana Ríos y Blanca Alejandra Zeledón Abea
"""

from fractions import Fraction

from modulos.modulo_gauss import gauss_jordan, resolver_solucion_unica
from modulos.modulo_matrices import (
    matriz_identidad,
    multiplicar_matrices,
    multiplicar_matriz_vector,
    son_iguales,
    validar_cuadrada,
    validar_matriz,
)
from utilidades.formato import formatear_operacion_eliminacion

MENSAJE_SIN_PERMUTACION = (
    "La matriz no admite Factorización LU sin permutación (requiere pivoteo parcial PA = LU)"
)
MENSAJE_FACTORIZACION_CORRECTA = "La factorización es correcta (L · U == A)"
MENSAJE_COMPROBACION_EXITOSA = "Comprobación exitosa: A · x == b"


def factorizar_lu(matriz_a):
    """Factoriza A (m×n) como L·U solo con reemplazos de fila; lanza ValueError si exige permutar filas.
    Devuelve matriz_L (m×m, unos en la diagonal), matriz_U (m×n), los multiplicadores y los pasos.
    """
    validar_matriz(matriz_a)
    matriz_U = [[Fraction(valor) for valor in fila] for fila in matriz_a]
    filas, columnas = len(matriz_U), len(matriz_U[0])
    matriz_L = matriz_identidad(filas)
    multiplicadores = []
    pasos = [{"titulo": "Matriz inicial", "operacion": "U comienza igual que A; L comienza como la identidad.",
              "matriz_U": [fila[:] for fila in matriz_U], "matriz_L": [fila[:] for fila in matriz_L]}]

    fila_pivote = 0
    for columna in range(columnas):
        if fila_pivote >= filas:
            break
        pivote = matriz_U[fila_pivote][columna]
        entradas_debajo = [matriz_U[fila][columna] for fila in range(fila_pivote + 1, filas)]
        if pivote == 0:
            # Un pivote nulo con una entrada no nula debajo exige intercambiar filas, y LU sin permutación no existe.
            if any(entrada != 0 for entrada in entradas_debajo):
                raise ValueError(MENSAJE_SIN_PERMUTACION)
            continue
        for fila in range(fila_pivote + 1, filas):
            multiplicador_l = matriz_U[fila][columna] / pivote
            if multiplicador_l == 0:
                continue
            # El multiplicador se registra en L antes de alterar la fila de U.
            matriz_L[fila][fila_pivote] = multiplicador_l
            multiplicadores.append({"fila": fila, "columna": fila_pivote, "valor": multiplicador_l})
            matriz_U[fila] = [x - multiplicador_l * y for x, y in zip(matriz_U[fila], matriz_U[fila_pivote])]
            pasos.append({
                "titulo": "Eliminación debajo del pivote",
                "operacion": formatear_operacion_eliminacion(fila + 1, fila_pivote + 1, multiplicador_l),
                "matriz_U": [fila_u[:] for fila_u in matriz_U],
                "matriz_L": [fila_l[:] for fila_l in matriz_L],
            })
        fila_pivote += 1
    return {"matriz_L": matriz_L, "matriz_U": matriz_U, "multiplicadores": multiplicadores, "pasos": pasos}


def verificar_factorizacion(matriz_a, matriz_L, matriz_U):
    """Multiplica L·U con el producto de la Calculadora y lo compara con A.
    Devuelve el producto, si coincide con A y el mensaje de verificación.
    """
    producto_lu = multiplicar_matrices(matriz_L, matriz_U)
    es_correcta = son_iguales(producto_lu, [[Fraction(valor) for valor in fila] for fila in matriz_a])
    mensaje = MENSAJE_FACTORIZACION_CORRECTA if es_correcta else "La factorización es incorrecta (L · U ≠ A)"
    return {"producto": producto_lu, "es_correcta": es_correcta, "mensaje": mensaje}


def _resolver_por_reduccion(matriz_coeficientes, vector_termino):
    """Reduce [matriz | vector] con Gauss-Jordan y devuelve (solución, pasos); ValueError si no es única."""
    orden = len(matriz_coeficientes)
    aumentada = [fila[:] + [vector_termino[indice]] for indice, fila in enumerate(matriz_coeficientes)]
    reducida, pivotes, inconsistente, pasos = gauss_jordan(aumentada, orden)
    if inconsistente or len(pivotes) < orden:
        raise ValueError("El sistema triangular es singular: no tiene solución única.")
    return resolver_solucion_unica(reducida, orden, pivotes), pasos


def sustitucion_adelante(matriz_L, vector_b):
    """Resuelve Ly = b reduciendo [L | b]; devuelve el vector intermedio y los pasos."""
    validar_cuadrada(matriz_L)
    vector_y, pasos = _resolver_por_reduccion(matriz_L, vector_b)
    return {"vector_y": vector_y, "pasos": pasos}


def sustitucion_atras(matriz_U, vector_y):
    """Resuelve Ux = y reduciendo [U | y]; devuelve la solución y los pasos."""
    validar_cuadrada(matriz_U)
    vector_x, pasos = _resolver_por_reduccion(matriz_U, vector_y)
    return {"vector_x": vector_x, "pasos": pasos}


def resolver_con_lu(matriz_a, vector_b):
    """Resuelve Ax = b (A cuadrada) encadenando LU, Ly = b, Ux = y y la comprobación A·x == b.
    Devuelve L, U, la verificación de la factorización, y, x, los pasos y la comprobación final.
    """
    validar_cuadrada(matriz_a)
    if len(vector_b) != len(matriz_a):
        raise ValueError("El vector b debe tener tantas componentes como filas tiene A.")
    vector_b = [Fraction(valor) for valor in vector_b]
    factorizacion = factorizar_lu(matriz_a)
    matriz_L, matriz_U = factorizacion["matriz_L"], factorizacion["matriz_U"]
    verificacion = verificar_factorizacion(matriz_a, matriz_L, matriz_U)
    adelante = sustitucion_adelante(matriz_L, vector_b)
    atras = sustitucion_atras(matriz_U, adelante["vector_y"])
    producto_ax = multiplicar_matriz_vector([[Fraction(v) for v in fila] for fila in matriz_a], atras["vector_x"])
    es_exacta = producto_ax == vector_b
    return {
        "matriz_L": matriz_L, "matriz_U": matriz_U, "multiplicadores": factorizacion["multiplicadores"],
        "pasos_factorizacion": factorizacion["pasos"], "verificacion": verificacion,
        "vector_y": adelante["vector_y"], "pasos_adelante": adelante["pasos"],
        "vector_x": atras["vector_x"], "pasos_atras": atras["pasos"],
        "producto_ax": producto_ax, "comprobacion_exitosa": es_exacta,
        "mensaje_comprobacion": MENSAJE_COMPROBACION_EXITOSA if es_exacta else "La comprobación falló (A · x ≠ b)",
    }

"""Algoritmos de eliminación por filas para el Programa 1.

El cálculo se realiza con Fraction de la biblioteca estándar de Python,
por lo que los resultados racionales se conservan de forma exacta.
No se utilizan NumPy, SciPy ni funciones de álgebra lineal.
"""

from fractions import Fraction

from utilidades.fracciones import formatear_fraccion
from utilidades.formato import formatear_operacion_eliminacion


ZERO = Fraction(0, 1)


def es_cero(valor):
    """Determina si un valor es exactamente cero."""
    return valor == ZERO


def copiar_matriz(matriz):
    return [fila[:] for fila in matriz]


def intercambiar_filas(matriz, fila_a, fila_b):
    matriz[fila_a], matriz[fila_b] = matriz[fila_b], matriz[fila_a]


def limpiar_ceros(matriz, numero_variables):
    """Normaliza representaciones de cero."""
    for i in range(len(matriz)):
        for j in range(numero_variables + 1):
            if es_cero(matriz[i][j]):
                matriz[i][j] = ZERO


def eliminacion_gaussiana(matriz, numero_variables):
    """Reduce la matriz aumentada a forma escalonada y guarda cada paso."""
    matriz_trabajo = copiar_matriz(matriz)
    filas = len(matriz_trabajo)
    fila_pivote = 0
    pivotes = []
    pasos = [
        {
            "titulo": "Matriz inicial",
            "operacion": "Inicio del proceso de eliminación por filas.",
            "matriz": copiar_matriz(matriz_trabajo),
        }
    ]

    for columna in range(numero_variables):
        if fila_pivote >= filas:
            break

        fila_mejor = fila_pivote
        for fila in range(fila_pivote + 1, filas):
            if abs(matriz_trabajo[fila][columna]) > abs(matriz_trabajo[fila_mejor][columna]):
                fila_mejor = fila

        if es_cero(matriz_trabajo[fila_mejor][columna]):
            pasos.append({
                "titulo": f"Columna {columna + 1} sin pivote",
                "operacion": (
                    f"No se encontró pivote distinto de cero en la columna {columna + 1}; "
                    "se continúa."
                ),
                "matriz": copiar_matriz(matriz_trabajo),
            })
            continue

        if fila_mejor != fila_pivote:
            intercambiar_filas(matriz_trabajo, fila_mejor, fila_pivote)
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{fila_pivote + 1} ↔ R{fila_mejor + 1}",
                "matriz": copiar_matriz(matriz_trabajo),
            })

        pivote = matriz_trabajo[fila_pivote][columna]
        for j in range(columna, numero_variables + 1):
            matriz_trabajo[fila_pivote][j] /= pivote

        limpiar_ceros(matriz_trabajo, numero_variables)
        pasos.append({
            "titulo": "Normalización del pivote",
            "operacion": f"R{fila_pivote + 1} ← R{fila_pivote + 1} / ({formatear_fraccion(pivote)})",
            "matriz": copiar_matriz(matriz_trabajo),
        })

        for fila in range(fila_pivote + 1, filas):
            factor = matriz_trabajo[fila][columna]
            if es_cero(factor):
                continue

            for j in range(columna, numero_variables + 1):
                matriz_trabajo[fila][j] -= factor * matriz_trabajo[fila_pivote][j]

            limpiar_ceros(matriz_trabajo, numero_variables)
            pasos.append({
                "titulo": "Eliminación debajo del pivote",
                "operacion": formatear_operacion_eliminacion(
                    fila + 1,
                    fila_pivote + 1,
                    factor,
                ),
                "matriz": copiar_matriz(matriz_trabajo),
            })

        pivotes.append((fila_pivote, columna))
        fila_pivote += 1

    limpiar_ceros(matriz_trabajo, numero_variables)

    return (
        matriz_trabajo,
        pivotes,
        detectar_inconsistencia(matriz_trabajo, numero_variables),
        pasos,
    )


def detectar_inconsistencia(matriz, numero_variables):
    """Detecta una fila 0 ... 0 | c, con c distinto de cero."""
    for fila in matriz:
        coeficientes_cero = all(
            es_cero(fila[j]) for j in range(numero_variables)
        )
        if coeficientes_cero and not es_cero(fila[numero_variables]):
            return True
    return False


def obtener_clasificacion(matriz_escalonada, numero_variables, pivotes, inconsistente):
    """Clasifica el sistema según sus pivotes y filas inconsistentes."""
    if inconsistente:
        return "inconsistente", []

    if len(pivotes) == numero_variables:
        return "unica", []

    columnas_pivote = {columna for _, columna in pivotes}
    variables_libres = [
        columna
        for columna in range(numero_variables)
        if columna not in columnas_pivote
    ]
    return "infinita", variables_libres


def resolver_solucion_unica(matriz_escalonada, numero_variables, pivotes):
    """Resuelve por sustitución regresiva usando aritmética racional exacta."""
    solucion = [ZERO] * numero_variables

    for fila_pivote, columna_pivote in reversed(pivotes):
        valor = matriz_escalonada[fila_pivote][numero_variables]

        for columna in range(columna_pivote + 1, numero_variables):
            valor -= matriz_escalonada[fila_pivote][columna] * solucion[columna]

        coeficiente = matriz_escalonada[fila_pivote][columna_pivote]
        solucion[columna_pivote] = valor / coeficiente

    return solucion


def verificar_solucion(matriz_original, solucion):
    """Comprueba la solución sustituyéndola en el sistema original."""
    for fila in matriz_original:
        suma = ZERO
        for i, valor in enumerate(solucion):
            suma += fila[i] * valor
        if suma != fila[-1]:
            return False
    return True

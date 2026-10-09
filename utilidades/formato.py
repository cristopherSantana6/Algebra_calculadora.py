"""
Funciones auxiliares para presentar resultados de Álgebra Lineal.
Formatea números racionales, operaciones elementales y matrices.
Distingue matrices normales de matrices aumentadas para facilitar su lectura.
"""

from utilidades.fracciones import formatear_fraccion, formatear_factor


def formatear_numero(valor):
    """Convierte un valor racional a una representación legible.
    Recibe un número y devuelve su representación como entero o fracción.
    """
    return formatear_fraccion(valor)


def formatear_operacion(valor):
    """Formatea un factor utilizado en una operación matemática.
    Recibe un valor numérico y devuelve su representación como fracción.
    """
    return formatear_factor(valor)


def formatear_operacion_eliminacion(fila, fila_pivote, factor):
    """Genera el texto de una operación elemental entre filas.
    Recibe dos índices de fila y un factor; devuelve la operación formateada.
    """
    factor_texto = formatear_factor(abs(factor))
    if factor > 0:
        return f"R{fila} ← R{fila} - ({factor_texto})R{fila_pivote}"
    return f"R{fila} ← R{fila} + ({factor_texto})R{fila_pivote}"


def formatear_matriz_lineas(matriz, numero_variables):
    """Convierte una matriz en líneas de texto para su presentación.
    Recibe una matriz y el número de variables; devuelve una lista de líneas.
    """
    lineas = []
    for fila in matriz:
        if not fila:
            lineas.append("[ ]")
            continue

        # Matriz normal: no existe columna independiente a la derecha.
        if len(fila) <= numero_variables:
            valores = "  ".join(
                f"{formatear_numero(valor):>7}" for valor in fila
            )
            lineas.append(f"[ {valores} ]")
            continue

        # Matriz aumentada: las primeras columnas son las variables y la
        # última columna corresponde al término independiente.
        izquierda = "  ".join(
            f"{formatear_numero(valor):>7}" for valor in fila[:numero_variables]
        )
        derecha = formatear_numero(fila[numero_variables])
        lineas.append(f"[ {izquierda}  | {derecha:>7} ]")

    return lineas

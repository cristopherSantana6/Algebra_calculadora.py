"""Funciones auxiliares de presentación."""

from utilidades.fracciones import formatear_fraccion, formatear_factor


def formatear_numero(valor):
    """Muestra un valor racional como entero o fracción."""
    return formatear_fraccion(valor)


def formatear_operacion(valor):
    """Muestra un factor de operación como fracción."""
    return formatear_factor(valor)


def formatear_operacion_eliminacion(fila, fila_pivote, factor):
    """Genera una operación de fila legible usando fracciones."""
    factor_texto = formatear_factor(abs(factor))
    if factor > 0:
        return f"R{fila} ← R{fila} - ({factor_texto})R{fila_pivote}"
    return f"R{fila} ← R{fila} + ({factor_texto})R{fila_pivote}"


def formatear_matriz_lineas(matriz, numero_variables):
    """Convierte una matriz aumentada en líneas legibles."""
    lineas = []
    for fila in matriz:
        izquierda = "  ".join(
            f"{formatear_numero(valor):>7}" for valor in fila[:numero_variables]
        )
        derecha = formatear_numero(fila[numero_variables])
        lineas.append(f"[ {izquierda}  | {derecha:>7} ]")
    return lineas

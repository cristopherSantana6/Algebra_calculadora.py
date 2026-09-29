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
    """Convierte matrices normales o aumentadas en líneas legibles.

    Si la fila contiene exactamente ``numero_variables`` elementos, se trata
    de una matriz normal (por ejemplo, el resultado de A+B, A-B, cA o A·B)
    y se muestran todos sus elementos sin barra vertical.

    Si contiene un elemento adicional, se interpreta como matriz aumentada
    [A|b], utilizada por los sistemas Ax=b y la eliminación de Gauss.
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

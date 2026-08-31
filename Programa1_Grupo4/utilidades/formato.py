"""Funciones auxiliares de presentación."""

from algoritmos.eliminacion_gaussiana import es_cero


def formatear_numero(valor):
    if es_cero(valor):
        valor = 0.0
    if abs(valor - round(valor)) < 1e-10:
        return str(int(round(valor)))
    return f"{valor:.4f}".rstrip("0").rstrip(".")


def formatear_operacion(valor):
    return f"{valor:g}"


def formatear_matriz_lineas(matriz, numero_variables):
    lineas = []
    for fila in matriz:
        izquierda = "  ".join(
            f"{formatear_numero(valor):>7}" for valor in fila[:numero_variables]
        )
        derecha = formatear_numero(fila[numero_variables])
        lineas.append(f"[ {izquierda}  | {derecha:>7} ]")
    return lineas

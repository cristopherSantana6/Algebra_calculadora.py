"""Operaciones algebraicas con vectores en R^n.

Todas las operaciones usan listas y Fraction de la biblioteca estándar.
No se utilizan NumPy, SciPy ni funciones avanzadas de math.
"""

from fractions import Fraction
from algoritmos.eliminacion_gaussiana import eliminacion_gaussiana, obtener_clasificacion, resolver_solucion_unica


def validar_mismas_dimensiones(*vectores):
    """Verifica que todos los vectores tengan la misma dimensión; algebraicamente,
    solo se pueden sumar o restar vectores pertenecientes al mismo R^n."""
    if not vectores:
        raise ValueError("Debe proporcionar al menos un vector.")
    dimension = len(vectores[0])
    if dimension == 0:
        raise ValueError("Los vectores no pueden estar vacíos.")
    if any(len(v) != dimension for v in vectores):
        raise ValueError("Todos los vectores deben tener la misma dimensión.")


def sumar_vectores(a, b):
    """Calcula a+b componente a componente: (a_i+b_i) para i=1,...,n."""
    validar_mismas_dimensiones(a, b)
    return [x + y for x, y in zip(a, b)]


def restar_vectores(a, b):
    """Calcula a-b componente a componente: (a_i-b_i) para i=1,...,n."""
    validar_mismas_dimensiones(a, b)
    return [x - y for x, y in zip(a, b)]


def multiplicar_escalar(vector, escalar):
    """Calcula c·v componente a componente: (c v_i) para i=1,...,n."""
    return [escalar * x for x in vector]


def es_combinacion_lineal(vectores, b):
    """Determina si b está en el espacio generado por los vectores.
    Algebraicamente resuelve c1*v1+...+ck*vk=b transformándolo en A c=b,
    donde los vectores dados son las columnas de A."""
    if not vectores:
        raise ValueError("Debe proporcionar al menos un vector generador.")
    validar_mismas_dimensiones(*vectores, b)
    n = len(b)
    k = len(vectores)
    matriz = []
    for i in range(n):
        matriz.append([vectores[j][i] for j in range(k)] + [b[i]])

    escalonada, pivotes, inconsistente, pasos = eliminacion_gaussiana(matriz, k)
    clasificacion, libres = obtener_clasificacion(
        escalonada, k, pivotes, inconsistente
    )

    coeficientes = None
    if clasificacion == "unica":
        coeficientes = resolver_solucion_unica(escalonada, k, pivotes)

    return {
        "es_combinacion": not inconsistente,
        "clasificacion": clasificacion,
        "coeficientes": coeficientes,
        "variables_libres": libres,
        "matriz": matriz,
        "escalonada": escalonada,
        "pasos": pasos,
    }


def analizar_dependencia_lineal(vectores):
    """Determina si un conjunto de vectores es linealmente independiente.

    Los vectores se colocan como columnas de una matriz V y se estudia el
    sistema homogéneo Vc=0. El conjunto es independiente si el único
    conjunto de coeficientes que produce el vector cero es el trivial.
    """
    if not vectores:
        raise ValueError("Debe proporcionar al menos un vector.")
    validar_mismas_dimensiones(*vectores)

    n = len(vectores[0])
    k = len(vectores)
    matriz = [[vectores[j][i] for j in range(k)] + [Fraction(0)] for i in range(n)]
    escalonada, pivotes, _, pasos = eliminacion_gaussiana(matriz, k)
    rango = len(pivotes)
    independiente = rango == k

    # Si el conjunto es dependiente, construimos una relación no trivial
    # sencilla asignando 1 a la primera variable libre y resolviendo las pivote.
    relacion = None
    variables_libres = [
        j for j in range(k) if j not in {col for _, col in pivotes}
    ]
    if not independiente and variables_libres:
        relacion = [Fraction(0)] * k
        libre = variables_libres[0]
        relacion[libre] = Fraction(1)
        for fila, columna in reversed(pivotes):
            valor = Fraction(0)
            for j in range(columna + 1, k):
                valor += escalonada[fila][j] * relacion[j]
            relacion[columna] = -valor

    return {
        "independiente": independiente,
        "rango": rango,
        "dimension": n,
        "cantidad": k,
        "variables_libres": variables_libres,
        "relacion": relacion,
        "matriz": matriz,
        "escalonada": escalonada,
        "pasos": pasos,
    }

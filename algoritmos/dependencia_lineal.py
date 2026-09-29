"""Análisis de independencia y dependencia lineal para el Programa 4.

Implementación con Python estándar. No utiliza NumPy, SymPy ni otras
librerías externas. Los vectores se convierten en columnas de V y se
estudia el sistema homogéneo Vc = 0 mediante eliminación por filas.
"""

from fractions import Fraction

from algoritmos.eliminacion_gaussiana import eliminacion_gaussiana


def _validar_vectores(vectores):
    if not vectores:
        raise ValueError("Debe proporcionar al menos un vector.")
    dimension = len(vectores[0])
    if dimension == 0:
        raise ValueError("Los vectores no pueden estar vacíos.")
    if any(len(v) != dimension for v in vectores):
        raise ValueError("Todos los vectores deben tener la misma dimensión.")


def analizar_conjunto_vectores(vectores):
    """Evalúa un conjunto de vectores como L.I. o L.D.

    Retorna la matriz de columnas V, el sistema homogéneo [V|0], la
    forma escalonada, los pivotes, las variables libres y, si corresponde,
    una relación lineal no trivial.
    """
    _validar_vectores(vectores)

    n = len(vectores[0])
    k = len(vectores)

    # Matriz V: cada vector es una columna.
    matriz_columnas = [
        [vectores[j][i] for j in range(k)]
        for i in range(n)
    ]

    # Sistema homogéneo Vc = 0.
    matriz_homogenea = [
        fila[:] + [Fraction(0)]
        for fila in matriz_columnas
    ]

    escalonada, pivotes, _, pasos = eliminacion_gaussiana(
        matriz_homogenea, k
    )

    rango = len(pivotes)
    variables_libres = [
        j for j in range(k)
        if j not in {columna for _, columna in pivotes}
    ]
    independiente = rango == k

    relacion = None
    if not independiente and variables_libres:
        relacion = [Fraction(0)] * k
        libre = variables_libres[0]
        relacion[libre] = Fraction(1)

        # La matriz está en forma escalonada y los pivotes fueron
        # normalizados a 1, por lo que se puede hacer sustitución regresiva.
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
        "matriz_columnas": matriz_columnas,
        "matriz": matriz_homogenea,
        "escalonada": escalonada,
        "pivotes": pivotes,
        "pasos": pasos,
    }


"""Módulo para realizar operaciones algebraicas con vectores en R^n.
Implementa contenidos de Álgebra Lineal relacionados con operaciones vectoriales.
Utiliza listas y Fraction de la biblioteca estándar de Python.
Elaborado por: Cristopher Rafael Santana Ríos y Blanca Alejandra Zeledón Abea
"""

from fractions import Fraction
from algoritmos.eliminacion_gaussiana import eliminacion_gaussiana, es_homogeneo, obtener_clasificacion, resolver_solucion_unica
from algoritmos.dependencia_lineal import analizar_conjunto_vectores


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
    """Suma dos vectores componente a componente.
      Recibe los vectores A y B de igual dimensión y devuelve A + B.
      """
    validar_mismas_dimensiones(a, b)
    return [x + y for x, y in zip(a, b)]


def restar_vectores(a, b):
    """Calcula a-b componente a componente: (a_i-b_i) para i=1,...,n."""
    validar_mismas_dimensiones(a, b)
    return [x - y for x, y in zip(a, b)]


def multiplicar_escalar(vector, escalar):
    """Multiplica un vector por un escalar.
       Recibe un vector y un número; devuelve el vector resultante c·v.
       """
    validar_mismas_dimensiones(vector)
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
    # Los coeficientes se calculan directamente solo cuando el sistema tiene solución única.
    if clasificacion == "unica":
        coeficientes = resolver_solucion_unica(escalonada, k, pivotes)

    return {
        "es_combinacion": not inconsistente,
        "homogeneo": es_homogeneo(matriz, k),
        "clasificacion": clasificacion,
        "coeficientes": coeficientes,
        "variables_libres": libres,
        "matriz": matriz,
        "escalonada": escalonada,
        "pasos": pasos,
    }


def analizar_dependencia_lineal(vectores):
    """Analiza la dependencia lineal de un conjunto de vectores.
    Devuelve el resultado del análisis realizado por el módulo correspondiente."""
    return analizar_conjunto_vectores(vectores)

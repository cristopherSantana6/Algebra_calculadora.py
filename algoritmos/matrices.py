"""Compatibilidad: las operaciones de matrices viven ahora en modulos/modulo_matrices.py.
Este archivo solo reexporta sus nombres para que los imports anteriores sigan funcionando.
"""

from modulos.modulo_matrices import (  # noqa: F401
    validar_matriz,
    validar_mismas_dimensiones,
    sumar_matrices,
    restar_matrices,
    multiplicar_matriz_escalar,
    multiplicar_matrices,
    trasponer_matriz,
    validar_cuadrada,
    menor,
    determinante,
    determinante_reduccion,
    determinante_cofactores,
    desarrollo_cofactores,
    determinante_sarrus,
    resolver_cramer,
    matriz_cofactores,
    matriz_adjunta,
    inversa_por_adjunta,
    multiplicar_matriz_vector,
    inversa_gauss_jordan,
    matriz_identidad,
    matriz_cero,
    inversa,
    comprobar_traspuesta_del_producto,
)

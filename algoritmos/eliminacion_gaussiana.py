"""Compatibilidad: la eliminación gaussiana vive ahora en modulos/modulo_gauss.py.
Este archivo solo reexporta sus nombres para que los imports anteriores sigan funcionando.
"""

from modulos.modulo_gauss import (  # noqa: F401
    es_cero,
    copiar_matriz,
    intercambiar_filas,
    limpiar_ceros,
    eliminacion_gaussiana,
    formatear_operacion_division,
    gauss_jordan,
    detectar_inconsistencia,
    es_homogeneo,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
    ZERO,
)
from modulos.modulo_matrices import inversa_gauss_jordan  # noqa: F401

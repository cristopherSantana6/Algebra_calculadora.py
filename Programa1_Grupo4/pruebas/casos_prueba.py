"""Casos de prueba del Programa 1."""

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)


def ejecutar_casos():
    casos = [
        ("Caso 1 - Solución única", [[1, 1, 5], [2, -1, 1]], 2, "unica"),
        ("Caso 2 - Infinitas soluciones", [[1, 1, 2], [2, 2, 4]], 2, "infinita"),
        ("Caso 3 - Sin solución", [[1, 1, 2], [2, 2, 5]], 2, "inconsistente"),
    ]

    for nombre, matriz, variables, esperado in casos:
        escalonada, pivotes, inconsistente, pasos = eliminacion_gaussiana(matriz, variables)
        clasificacion, libres = obtener_clasificacion(escalonada, variables, pivotes, inconsistente)
        assert clasificacion == esperado, f"{nombre}: esperado {esperado}, obtenido {clasificacion}"
        assert pasos, f"{nombre}: no se registraron pasos"

        if clasificacion == "unica":
            solucion = resolver_solucion_unica(escalonada, variables, pivotes)
            assert verificar_solucion(matriz, solucion), f"{nombre}: verificación fallida"

        print(f"✓ {nombre}: {clasificacion} ({len(pasos)} pasos)")


if __name__ == "__main__":
    ejecutar_casos()

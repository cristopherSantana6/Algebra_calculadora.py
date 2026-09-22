"""Casos de prueba del Programa 1 con aritmética racional exacta."""

from fractions import Fraction

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)
from utilidades.fracciones import formatear_fraccion, leer_fraccion


def ejecutar_casos():
    casos = [
        (
            "Caso 1 - Solución única",
            [[Fraction(2), Fraction(-1), Fraction(1), Fraction(3)],
             [Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
             [Fraction(1), Fraction(2), Fraction(-1), Fraction(2)]],
            3,
            "unica",
        ),
        (
            "Caso 2 - Infinitas soluciones",
            [[Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
             [Fraction(2), Fraction(2), Fraction(2), Fraction(12)],
             [Fraction(3), Fraction(3), Fraction(3), Fraction(18)]],
            3,
            "infinita",
        ),
        (
            "Caso 3 - Sin solución",
            [[Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
             [Fraction(2), Fraction(2), Fraction(2), Fraction(12)],
             [Fraction(3), Fraction(3), Fraction(3), Fraction(20)]],
            3,
            "inconsistente",
        ),
        (
            "Caso fraccionario - Solución exacta",
            [[Fraction(1, 2), Fraction(1), Fraction(3, 2)],
             [Fraction(2), Fraction(-1), Fraction(3)]],
            2,
            "unica",
        ),
    ]

    for nombre, matriz, variables, esperado in casos:
        escalonada, pivotes, inconsistente, pasos = eliminacion_gaussiana(
            matriz,
            variables,
        )
        clasificacion, libres = obtener_clasificacion(
            escalonada,
            variables,
            pivotes,
            inconsistente,
        )
        assert clasificacion == esperado, (
            f"{nombre}: esperado {esperado}, obtenido {clasificacion}"
        )
        assert pasos, f"{nombre}: no se registraron pasos"

        if clasificacion == "unica":
            solucion = resolver_solucion_unica(
                escalonada,
                variables,
                pivotes,
            )
            assert all(isinstance(valor, Fraction) for valor in solucion)
            assert verificar_solucion(matriz, solucion), (
                f"{nombre}: verificación fallida"
            )
            print("Solución:", ", ".join(
                f"x{i + 1}={formatear_fraccion(valor)}"
                for i, valor in enumerate(solucion)
            ))

        elif clasificacion == "infinita":
            print(
                "Variables libres:",
                ", ".join(f"x{columna + 1}" for columna in libres),
            )

        print(f"✓ {nombre}: {clasificacion} ({len(pasos)} pasos)")

    assert leer_fraccion("1/2") == Fraction(1, 2)
    assert leer_fraccion("-5/8") == Fraction(-5, 8)
    assert leer_fraccion("0.25") == Fraction(1, 4)
    print("✓ Lectura de fracciones: correcta")


if __name__ == "__main__":
    ejecutar_casos()

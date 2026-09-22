"""Funciones para lectura y presentación exacta de números racionales."""

from fractions import Fraction


def leer_fraccion(texto):
    """
    Convierte una entrada escrita por el usuario a Fraction.

    Se aceptan, por ejemplo:
        2
        -3
        1/2
        -5/8
        0.25
        1.5
    """
    valor = str(texto).strip().replace(" ", "")
    if not valor:
        raise ValueError("La entrada está vacía.")

    try:
        return Fraction(valor)
    except ValueError:
        raise ValueError(
            f"'{texto}' no es un número válido. Use formatos como 2, -3 o 1/2."
        ) from None


def formatear_fraccion(valor):
    """Devuelve una Fraction como entero o fracción a/b."""
    fraccion = valor if isinstance(valor, Fraction) else Fraction(valor)
    if fraccion.denominator == 1:
        return str(fraccion.numerator)
    return f"{fraccion.numerator}/{fraccion.denominator}"


def formatear_factor(valor):
    """Formato compacto para factores usados en operaciones de fila."""
    return formatear_fraccion(valor)

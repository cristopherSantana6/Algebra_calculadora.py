
"""
Funciones para leer y presentar números racionales de forma exacta.
Utiliza Fraction para representar enteros, fracciones y decimales.
Facilita la entrada de datos y la presentación de resultados de Álgebra Lineal.
"""


from fractions import Fraction


def leer_fraccion(texto):
    """Convierte una entrada textual en un número racional.
    Recibe una cadena con un entero, fracción o decimal y devuelve Fraction.
    Genera ValueError si la entrada está vacía o no tiene un formato válido.
    """
    valor = str(texto).strip().replace(" ", "")
    if not valor:
        raise ValueError("La entrada está vacía.")

    try:
        return Fraction(valor)
    except ZeroDivisionError:
        raise ValueError("El denominador de una fracción no puede ser cero.") from None
    except ValueError:
        raise ValueError(
            f"'{texto}' no es un número válido. Use formatos como 2, -3 o 1/2."
        ) from None


def formatear_fraccion(valor):
    """Representa un número racional como entero o fracción a/b.
       Recibe un valor numérico y devuelve una cadena legible.
       """
    fraccion = valor if isinstance(valor, Fraction) else Fraction(valor)
    if fraccion.denominator == 1:
        return str(fraccion.numerator)
    return f"{fraccion.numerator}/{fraccion.denominator}"


def formatear_factor(valor):
    """Formatea un factor utilizado en operaciones elementales por filas.
        Recibe un valor numérico y devuelve su representación textual compacta.
        """
    return formatear_fraccion(valor)

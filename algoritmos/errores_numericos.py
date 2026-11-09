
"""
Errores Numéricos - Programa 7.
Calculadora de Álgebra Lineal.
Universidad Americana (UAM).

Incluye:
1. Cálculo de errores.
2. Propagación del error.
3. Truncamiento y redondeo iterativo.
4. Inestabilidad numérica.
5. Representación en punto flotante y tipos de errores.

Las funciones realizan cálculos y devuelven resultados.
No dependen de input(), print() ni de Tkinter.
"""

import math
from decimal import (
    Decimal,
    InvalidOperation,
    ROUND_DOWN,
    ROUND_HALF_UP
)

import numpy as np


def validar_real(valor, nombre="Valor"):
    """Convierte un dato numérico y comprueba que sea finito."""
    try:
        numero = float(valor)
    except (ValueError, TypeError, OverflowError):
        raise ValueError(
            f"{nombre} debe ser un número válido."
        ) from None

    if not math.isfinite(numero):
        raise ValueError(
            f"{nombre} debe ser un número finito."
        )

    return numero


# ------------------------------------------------------
# 1. CÁLCULO DIRECTO DE ERRORES
# ------------------------------------------------------

def calcular_errores(valor_verdadero, valor_aproximado):
    """Calcula error absoluto, relativo y porcentual."""

    xv = validar_real(valor_verdadero, "Valor verdadero")
    xa = validar_real(valor_aproximado, "Valor aproximado")

    error_absoluto = abs(xv - xa)

    if not math.isfinite(error_absoluto):
        raise ValueError("El error calculado no es finito.")

    if xv == 0:
        error_relativo = None
        error_porcentual = None
        explicacion = (
            "El valor verdadero es cero. "
            "El error relativo y el porcentual no están "
            "definidos porque no se puede dividir entre cero."
        )
    else:
        error_relativo = error_absoluto / abs(xv)
        error_porcentual = error_relativo * 100

        explicacion = (
            "El error absoluto mide la diferencia entre "
            "el valor verdadero y el aproximado. "
            "El error relativo compara esa diferencia "
            "con la magnitud del valor verdadero."
        )

    return {
        "valor_verdadero": xv,
        "valor_aproximado": xa,
        "error_absoluto": error_absoluto,
        "error_relativo": error_relativo,
        "error_porcentual": error_porcentual,
        "explicacion": explicacion
    }


# ------------------------------------------------------
# 2. PROPAGACIÓN DEL ERROR
# ------------------------------------------------------

def funcion_propagacion(x):
    """Evalúa f(x) = sin(x) + x²."""
    return math.sin(x) + x ** 2


def derivada_propagacion(x):
    """Evalúa f'(x) = cos(x) + 2x."""
    return math.cos(x) + 2 * x


def calcular_propagacion(x, delta_x):
    """Compara la propagación lineal y el cambio real."""

    x = validar_real(x, "Valor de x")
    delta_x = validar_real(delta_x, "Perturbación Δx")

    if abs(x) > 1e100:
        raise ValueError(
            "El valor de x es demasiado grande para "
            "esta simulación."
        )

    x_perturbado = x + delta_x

    if not math.isfinite(x_perturbado):
        raise ValueError(
            "La perturbación produce un valor no finito."
        )

    fx = funcion_propagacion(x)
    fx_perturbada = funcion_propagacion(x_perturbado)

    # Derivada analítica de la función propuesta.
    derivada_exacta = derivada_propagacion(x)

    # Derivada numérica mediante diferencia central.
    h = 1e-5 * max(1.0, abs(x))

    derivada_numerica = (
        funcion_propagacion(x + h)
        - funcion_propagacion(x - h)
    ) / (2 * h)

    delta_y_aproximado = derivada_exacta * delta_x
    delta_y_numerico = derivada_numerica * delta_x

    delta_y_real = fx_perturbada - fx

    diferencia = abs(
        delta_y_aproximado - delta_y_real
    )

    diferencia_numerica = abs(
        delta_y_numerico - delta_y_real
    )

    valores = (
        fx, fx_perturbada,
        derivada_exacta, derivada_numerica,
        delta_y_aproximado, delta_y_numerico,
        delta_y_real, diferencia, diferencia_numerica
    )

    if not all(math.isfinite(v) for v in valores):
        raise ValueError(
            "La operación produjo resultados no finitos."
        )

    return {
        "funcion": "sin(x) + x**2",
        "derivada": "cos(x) + 2*x",
        "x": x,
        "delta_x": delta_x,
        "fx": fx,
        "fx_perturbada": fx_perturbada,
        "derivada_exacta": derivada_exacta,
        "derivada_numerica": derivada_numerica,
        "delta_y_aproximado": delta_y_aproximado,
        "delta_y_numerico": delta_y_numerico,
        "delta_y_real": delta_y_real,
        "diferencia": diferencia,
        "diferencia_numerica": diferencia_numerica,
        "explicacion": (
            "La derivada permite estimar cómo cambia "
            "la función ante una pequeña perturbación. "
            "Es una aproximación de primer orden que "
            "generalmente mejora cuando Δx es pequeño."
        )
    }


# ------------------------------------------------------
# 3. TRUNCAMIENTO VS. REDONDEO
# ------------------------------------------------------

def simular_truncamiento_redondeo(
        incremento="0.1666666667",
        repeticiones=12,
        decimales=2):
    """
    Simula sumas repetidas, truncando o redondeando
    cada incremento antes de acumularlo.
    """

    try:
        incremento = Decimal(str(incremento))
        repeticiones = int(repeticiones)
        decimales = int(decimales)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(
            "Revise el incremento, las repeticiones "
            "y la cantidad de decimales."
        ) from None

    if not incremento.is_finite():
        raise ValueError("El incremento debe ser finito.")

    if not 1 <= repeticiones <= 1000:
        raise ValueError(
            "Las repeticiones deben estar entre 1 y 1000."
        )

    if not 0 <= decimales <= 10:
        raise ValueError(
            "Los decimales deben estar entre 0 y 10."
        )

    unidad = Decimal(1).scaleb(-decimales)

    truncado = incremento.quantize(
        unidad, rounding=ROUND_DOWN
    )

    redondeado = incremento.quantize(
        unidad, rounding=ROUND_HALF_UP
    )

    acumulado_truncado = Decimal(0)
    acumulado_redondeado = Decimal(0)

    pasos = []

    for k in range(1, repeticiones + 1):
        acumulado_truncado += truncado
        acumulado_redondeado += redondeado

        valor_referencia = incremento * k

        pasos.append({
            "iteracion": k,
            "referencia": float(valor_referencia),
            "truncamiento": float(acumulado_truncado),
            "redondeo": float(acumulado_redondeado),
            "error_truncamiento": float(abs(
                valor_referencia - acumulado_truncado
            )),
            "error_redondeo": float(abs(
                valor_referencia - acumulado_redondeado
            ))
        })

    referencia_final = incremento * repeticiones

    return {
        "incremento": str(incremento),
        "repeticiones": repeticiones,
        "decimales": decimales,
        "incremento_truncado": str(truncado),
        "incremento_redondeado": str(redondeado),
        "referencia_final": float(referencia_final),
        "resultado_truncado": float(acumulado_truncado),
        "resultado_redondeado": float(acumulado_redondeado),
        "error_truncamiento": float(abs(
            referencia_final - acumulado_truncado
        )),
        "error_redondeo": float(abs(
            referencia_final - acumulado_redondeado
        )),
        "pasos": pasos,
        "explicacion": (
            "El truncamiento elimina las cifras sobrantes "
            "sin ajustar el último dígito conservado. "
            "El redondeo ajusta ese dígito según la cifra "
            "siguiente. Repetir operaciones puede acumular "
            "los errores de aproximación."
        )
    }


# ------------------------------------------------------
# 4. INESTABILIDAD NUMÉRICA
# ------------------------------------------------------

def analizar_inestabilidad(x):
    """
    Compara dos formas equivalentes de calcular:
    sqrt(x² + 1) - x, para x positivo.
    """

    x = validar_real(x, "Valor de x")

    if x <= 0 or x > 1e150:
        raise ValueError(
            "Ingrese un valor positivo de x, "
            "menor o igual que 1e150."
        )

    # Forma directa: puede perder cifras por cancelación.
    resultado_directo = math.sqrt(x ** 2 + 1) - x

    # Forma algebraicamente equivalente y más estable.
    resultado_estable = 1 / (
        math.sqrt(x ** 2 + 1) + x
    )

    diferencia = abs(
        resultado_directo - resultado_estable
    )

    return {
        "x": x,
        "expresion_directa": "sqrt(x**2 + 1) - x",
        "expresion_estable": "1/(sqrt(x**2 + 1) + x)",
        "resultado_directo": resultado_directo,
        "resultado_estable": resultado_estable,
        "diferencia": diferencia,
        "explicacion": (
            "Al restar dos números muy parecidos, "
            "pueden perderse cifras significativas. "
            "La expresión reformulada evita esa resta "
            "y suele producir un resultado más estable."
        )
    }


# ------------------------------------------------------
# 5. PUNTO FLOTANTE
# ------------------------------------------------------

def analizar_punto_flotante():
    """Muestra precisión, overflow y underflow controlados."""

    suma = 0.1 + 0.2
    comparacion = suma == 0.3

    epsilon = float(np.finfo(float).eps)

    # Overflow: el resultado excede el rango del float.
    with np.errstate(over="ignore", under="ignore"):
        overflow = np.float64(1e308) * np.float64(10)

        # Menor subnormal positivo representable.
        minimo_positivo = np.nextafter(
            np.float64(0), np.float64(1)
        )

        # Su mitad ya no puede representarse en float64.
        underflow = minimo_positivo / np.float64(2)

    return {
        "suma": suma,
        "comparacion": comparacion,
        "epsilon": epsilon,
        "overflow": float(overflow),
        "underflow": float(underflow),
        "minimo_positivo": float(minimo_positivo),
        "explicacion": (
            "Muchos decimales, como 0.1 y 0.2, "
            "no tienen una representación binaria exacta "
            "en punto flotante. Por eso la suma puede "
            "diferir ligeramente de 0.3.\n\n"
            "El épsilon de máquina es la distancia entre "
            "1.0 y el siguiente número representable mayor "
            "en doble precisión.\n\n"
            "Overflow ocurre cuando un resultado excede "
            "el rango representable. Underflow ocurre "
            "cuando un resultado no nulo es demasiado "
            "pequeño para representarse con la precisión "
            "disponible."
        )
    }


# ------------------------------------------------------
# 6. DEFINICIONES DE TIPOS DE ERROR
# ------------------------------------------------------

def obtener_tipos_errores():
    """Devuelve definiciones breves y ejemplos."""

    return [
        {
            "tipo": "Error inherente",
            "definicion": (
                "Error que ya existe en los datos iniciales."
            ),
            "ejemplo": (
                "Medir una longitud como 2.5 m cuando "
                "su valor real es 2.503 m."
            )
        },
        {
            "tipo": "Error de redondeo",
            "definicion": (
                "Se produce al aproximar un número "
                "a una cantidad limitada de cifras."
            ),
            "ejemplo": "Redondear 3.14159 a 3.14."
        },
        {
            "tipo": "Error de truncamiento",
            "definicion": (
                "Se produce al sustituir un proceso "
                "matemático por una aproximación finita."
            ),
            "ejemplo": (
                "Aproximar e^x mediante los primeros "
                "términos de su serie de Taylor."
            )
        },
        {
            "tipo": "Overflow",
            "definicion": (
                "Un resultado excede el rango máximo "
                "representable por el tipo numérico."
            ),
            "ejemplo": (
                "Multiplicar dos valores float64 muy grandes."
            )
        },
        {
            "tipo": "Underflow",
            "definicion": (
                "Un resultado no nulo es demasiado pequeño "
                "para representarse adecuadamente."
            ),
            "ejemplo": (
                "Dividir entre dos el menor número "
                "subnormal positivo de float64."
            )
        },
        {
            "tipo": "Error del modelo matemático",
            "definicion": (
                "Ocurre cuando el modelo simplifica "
                "o no representa completamente la realidad."
            ),
            "ejemplo": (
                "Predecir el movimiento de un objeto "
                "sin considerar la resistencia del aire."
            )
        }
    ]

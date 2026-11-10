
"""
Genera puntos, valida el dominio y representa funciones.
Admite marcar la raíz aproximada del Método de Bisección.
"""

import math

import numpy as np
import sympy as sp
from matplotlib.figure import Figure

from algoritmos.biseccion import X, convertir_funcion


def generar_puntos(funcion, x_min, x_max, cantidad=2001):
    """Genera los puntos necesarios para graficar una función.
    Valida el intervalo y descarta resultados no reales o infinitos.
    Detecta saltos grandes para evitar unir posibles asíntotas.
    """
    # Validar que los límites ingresados sean numéricos.
    try:
        x_min = float(x_min)
        x_max = float(x_max)
    except (ValueError, TypeError, OverflowError):
        raise ValueError(
            "Los límites deben ser números válidos."
        ) from None

    if not math.isfinite(x_min) or not math.isfinite(x_max):
        raise ValueError("Los límites deben ser finitos.")

    if x_min >= x_max:
        raise ValueError(
            "El límite inferior debe ser menor que el superior."
        )

    if cantidad < 1000:
        raise ValueError("Se requieren al menos 1000 puntos.")

    # Convertir la función y generar puntos distribuidos en el intervalo.
    expresion = convertir_funcion(funcion)
    x = np.linspace(x_min, x_max, cantidad)

    # Construimos una función NumPy sin utilizar eval()
    # sobre el texto ingresado por el usuario.
    funcion_numpy = sp.lambdify(
        X, expresion, modules=["numpy"]
    )

    try:
        with np.errstate(all="ignore"):
            valores = funcion_numpy(x)

            # Una función constante devuelve un escalar;
            # lo convertimos en un arreglo del mismo tamaño.
            valores = np.broadcast_to(
                np.asarray(valores, dtype=complex),
                x.shape
            ).copy()

    except (ValueError, TypeError, ZeroDivisionError,
            OverflowError) as error:
        raise ValueError(
            f"No se pudo evaluar la función: {error}"
        ) from error

    # Solo admitimos resultados reales y finitos.
    validos = (
        np.isfinite(valores.real)
        & np.isfinite(valores.imag)
        & (np.abs(valores.imag) < 1e-10)
    )

    # Los valores inválidos se representan con NaN para no graficarlos.
    y = np.where(validos, valores.real, np.nan)

    if not np.any(validos):
        raise ValueError(
            "La función no tiene valores reales válidos "
            "en el intervalo seleccionado."
        )

    # Detectar saltos grandes, especialmente los producidos
    # por asíntotas en funciones racionales y trigonométricas.
    finitos = y[np.isfinite(y)]

    if len(finitos) >= 3:
        escala = np.percentile(np.abs(finitos), 75)
        escala = max(float(escala), 1e-12)

        diferencias = np.abs(np.diff(y))
        diferencias_finitas = diferencias[
            np.isfinite(diferencias)
        ]

        if len(diferencias_finitas):
            cambio_normal = np.median(
                diferencias_finitas
            )
            umbral = max(
                20 * cambio_normal,
                2 * escala,
                1e-12
            )

            for i in range(len(y) - 1):
                if not (
                    np.isfinite(y[i])
                    and np.isfinite(y[i + 1])
                ):
                    continue

                salto = abs(y[i + 1] - y[i])

                # Un salto extraordinario con cambio de
                # signo puede indicar una asíntota vertical.
                if (
                    salto > umbral
                    and y[i] * y[i + 1] < 0
                    and min(abs(y[i]), abs(y[i + 1]))
                    > escala
                ):
                    y[i + 1] = np.nan

    # Devolver los puntos y la información necesaria para la gráfica.
    return {
        "funcion": funcion,
        "expresion": expresion,
        "x": x,
        "y": y,
        "x_min": x_min,
        "x_max": x_max,
        "puntos_validos": int(np.isfinite(y).sum()),
        "puntos_totales": cantidad,
    }


def crear_grafica(funcion, x_min, x_max,
                 raiz=None, intervalo_raiz=None):
    """Construye la representación gráfica de una función.
    Incluye ejes, cuadrícula, leyenda y límites del intervalo.
    Permite señalar una raíz aproximada y el intervalo de Bisección.
    """
    # Obtener los puntos válidos de la función.
    datos = generar_puntos(
        funcion, x_min, x_max
    )

    # Crear la figura de Matplotlib.
    figura = Figure(
        figsize=(9, 5),
        dpi=100,
        facecolor="white"
    )

    eje = figura.add_subplot(111)

    # Dibujar la curva con el color establecido en la interfaz.
    eje.plot(
        datos["x"],
        datos["y"],
        color="#7057B5",
        linewidth=2,
        label=f"f(x) = {funcion}"
    )

    # Dibujar los ejes horizontal y vertical.
    eje.axhline(
        0, color="#555555", linewidth=0.8
    )
    eje.axvline(
        0, color="#555555", linewidth=0.8
    )

    # Marcar la raíz cuando proviene de Bisección.
    if raiz is not None:
        raiz = float(raiz)

        if not math.isfinite(raiz):
            raise ValueError("La raíz debe ser finita.")

        if datos["x_min"] <= raiz <= datos["x_max"]:
            valor_raiz = complex(
                sp.N(datos["expresion"].subs(X, raiz))
            )

            if (
                math.isfinite(valor_raiz.real)
                and math.isfinite(valor_raiz.imag)
                and abs(valor_raiz.imag) < 1e-10
            ):
                eje.scatter(
                    [raiz],
                    [valor_raiz.real],
                    color="#D9534F",
                    s=65,
                    zorder=5,
                    label=f"Raíz aproximada: {raiz:.8f}"
                )

    # Mostrar el intervalo inicial de Bisección.
    if intervalo_raiz is not None:
        a, b = intervalo_raiz

        eje.axvspan(
            a, b,
            color="#E8B86D",
            alpha=0.15,
            label="Intervalo inicial de Bisección"
        )

    # Configurar el título y los nombres de los ejes.
    eje.set_title(
        "Graficador de Funciones",
        fontsize=14,
        fontweight="bold"
    )

    eje.set_xlabel("Eje X")
    eje.set_ylabel("Eje Y")

    # Mantener los límites establecidos por el usuario.
    eje.set_xlim(
        datos["x_min"],
        datos["x_max"]
    )

    # Mostrar la cuadrícula para facilitar la lectura.
    eje.grid(
        True,
        linestyle="--",
        alpha=0.35
    )

    # Agregar la leyenda y ajustar la distribución de la figura.
    eje.legend(loc="best", fontsize=9)
    figura.tight_layout()

    return figura, datos

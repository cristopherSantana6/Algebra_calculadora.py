
"""
Método de Bisección - Programa 7.
Calculadora de Álgebra Lineal, Universidad Americana.

Implementa el algoritmo desde cero y registra sus iteraciones.
SymPy se utiliza para interpretar y validar las funciones.
SciPy se utiliza únicamente como comparación externa.
"""

import ast
import math
import operator

import sympy as sp
from sympy.calculus.util import continuous_domain


X = sp.Symbol("x", real=True)

FUNCIONES = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "exp": sp.exp,
    "log": sp.log,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
}

CONSTANTES = {
    "x": X,
    "pi": sp.pi,
    "e": sp.E,
}

OPERACIONES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def convertir_funcion(texto):
    """Interpreta una función usando únicamente operaciones permitidas."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Debe ingresar una función f(x).")

    if len(texto) > 200:
        raise ValueError("La función es demasiado larga.")

    try:
        arbol = ast.parse(texto, mode="eval")
    except SyntaxError:
        raise ValueError("La función está mal escrita.") from None

    if sum(1 for _ in ast.walk(arbol)) > 100:
        raise ValueError("La función es demasiado compleja.")

    def interpretar(nodo):
        if isinstance(nodo, ast.Expression):
            return interpretar(nodo.body)

        if isinstance(nodo, ast.Constant):
            if type(nodo.value) in (int, float):
                return sp.sympify(nodo.value)
            raise ValueError("Constante no permitida.")

        if isinstance(nodo, ast.Name):
            if nodo.id in CONSTANTES:
                return CONSTANTES[nodo.id]
            raise ValueError(f"Símbolo no permitido: {nodo.id}")

        if isinstance(nodo, ast.UnaryOp):
            valor = interpretar(nodo.operand)
            if isinstance(nodo.op, ast.USub):
                return -valor
            if isinstance(nodo.op, ast.UAdd):
                return valor
            raise ValueError("Operación no permitida.")

        if isinstance(nodo, ast.BinOp):
            operacion = OPERACIONES.get(type(nodo.op))
            if operacion is None:
                raise ValueError("Operación matemática no permitida.")
            izquierda = interpretar(nodo.left)
            derecha = interpretar(nodo.right)
            return operacion(izquierda, derecha)

        if isinstance(nodo, ast.Call):
            if not isinstance(nodo.func, ast.Name):
                raise ValueError("Llamada no permitida.")

            funcion = FUNCIONES.get(nodo.func.id)
            if funcion is None or len(nodo.args) != 1 or nodo.keywords:
                raise ValueError("Función matemática no permitida.")

            return funcion(interpretar(nodo.args[0]))

        raise ValueError("La expresión contiene elementos no permitidos.")

    try:
        return interpretar(arbol)
    except (ZeroDivisionError, OverflowError, TypeError) as error:
        raise ValueError(f"Función inválida: {error}") from error


def evaluar_funcion(expresion, valor):
    """Evalúa f(x) y comprueba que el resultado sea real y finito."""
    try:
        resultado = complex(sp.N(expresion.subs(X, valor), 16))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        raise ValueError(
            f"La función no está definida en x = {valor}."
        ) from None

    if not math.isfinite(resultado.real):
        raise ValueError("Se obtuvo un resultado no finito.")

    if not math.isfinite(resultado.imag) or abs(resultado.imag) > 1e-12:
        raise ValueError("La función produce un resultado no real.")

    return resultado.real


def verificar_continuidad(expresion, a, b):
    """Comprueba que el intervalo esté dentro del dominio continuo."""
    try:
        dominio = continuous_domain(expresion, X, sp.S.Reals)
        intervalo = sp.Interval(a, b)
        comprobacion = intervalo.is_subset(dominio)
    except (TypeError, ValueError, NotImplementedError):
        comprobacion = None

    if comprobacion is not True:
        raise ValueError(
            "No se pudo garantizar la continuidad en [a, b]. "
            "Revise discontinuidades, asíntotas o restricciones de dominio."
        )


def metodo_biseccion(funcion, a, b, tolerancia, max_iteraciones):
    """Calcula una raíz aproximada y registra el procedimiento iterativo."""
    try:
        a = float(a)
        b = float(b)
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Los límites y parámetros deben ser numéricos.") from None

    if not all(math.isfinite(v) for v in (a, b, tolerancia)):
        raise ValueError("Los valores deben ser finitos.")

    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el superior.")

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    if max_iteraciones < 1:
        raise ValueError("Debe permitir al menos una iteración.")

    expresion = convertir_funcion(funcion)

    verificar_continuidad(expresion, a, b)

    fa = evaluar_funcion(expresion, a)
    fb = evaluar_funcion(expresion, b)

    ancho_inicial = b - a
    n_teorico = max(0, math.ceil(math.log2(ancho_inicial / tolerancia)))

    resultado = {
        "funcion": funcion,
        "intervalo_inicial": (a, b),
        "tolerancia": tolerancia,
        "iteraciones_teoricas": n_teorico,
        "iteraciones_realizadas": 0,
        "tabla": [],
        "raiz": None,
        "valor_funcion": None,
        "error": None,
        "estado": "",
        "comparacion_scipy": None,
        "diferencia_scipy": None,
    }

    if fa == 0 or fb == 0:
        raiz = a if fa == 0 else b
        resultado.update({
            "raiz": raiz,
            "valor_funcion": 0.0,
            "error": 0.0,
            "estado": "Raíz exacta encontrada en un extremo.",
        })
        return resultado

    if (fa < 0) == (fb < 0):
        raise ValueError(
            "No existe cambio de signo entre f(a) y f(b). "
            "Seleccione otro intervalo; esto no significa "
            "que la función no tenga raíces."
        )

    # SciPy solo se emplea para contrastar el algoritmo propio.
    try:
        from scipy.optimize import bisect

        referencia = bisect(
            lambda valor: evaluar_funcion(expresion, valor),
            a, b, xtol=1e-12
        )
        resultado["comparacion_scipy"] = referencia
    except (ImportError, ValueError, RuntimeError, OverflowError):
        pass

    xr_anterior = None

    for k in range(1, max_iteraciones + 1):
        # Guardamos el intervalo ANTES de actualizar sus extremos.
        xr = a + (b - a) / 2
        eb = (b - a) / 2

        if xr == a or xr == b:
            resultado["estado"] = (
                "La precisión de máquina impide seguir reduciendo el intervalo."
            )
            break

        fr = evaluar_funcion(expresion, xr)

        error_aproximado = (
            None if xr_anterior is None else abs(xr - xr_anterior)
        )

        error_relativo = (
            None if xr_anterior is None or xr == 0
            else abs((xr - xr_anterior) / xr)
        )

        resultado["tabla"].append({
            "k": k,
            "a": a,
            "b": b,
            "xr": xr,
            "fa": fa,
            "fb": fb,
            "fr": fr,
            "eb": eb,
            "ea": error_aproximado,
            "error_relativo": error_relativo,
        })

        resultado["raiz"] = xr
        resultado["valor_funcion"] = fr
        resultado["error"] = eb
        resultado["iteraciones_realizadas"] = k

        if fr == 0:
            resultado["estado"] = "Raíz exacta encontrada."
            break

        if eb <= tolerancia:
            resultado["estado"] = "Tolerancia alcanzada correctamente."
            break

        # Conservamos la mitad donde se mantiene el cambio de signo.
        if (fa < 0) != (fr < 0):
            b, fb = xr, fr
        else:
            a, fa = xr, fr

        xr_anterior = xr

    if not resultado["estado"]:
        resultado["estado"] = (
            "Se alcanzó el máximo de iteraciones sin garantizar "
            "la tolerancia solicitada."
        )

    referencia = resultado["comparacion_scipy"]
    if referencia is not None and resultado["raiz"] is not None:
        resultado["diferencia_scipy"] = abs(
            resultado["raiz"] - referencia
        )

    resultado["intervalo_final"] = (a, b)
    return resultado

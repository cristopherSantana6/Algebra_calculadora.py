"""Implementación del método de Newton-Raphson para una función real f(x)."""
import math
import sympy as sp


def resolver_newton_raphson(expresion, x0, tolerancia=1e-6, max_iteraciones=100):
    """Calcula una raíz aproximada y devuelve el procedimiento de cada iteración."""
    # Validación de entradas: x0 finito, tolerancia y límite positivos.
    try:
        inicial, tol, limite = float(x0), float(tolerancia), int(max_iteraciones)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Revise el valor inicial, la tolerancia y las iteraciones.") from None
    if not all(math.isfinite(v) for v in (inicial, tol)) or tol <= 0 or limite <= 0:
        raise ValueError("La tolerancia y el máximo de iteraciones deben ser positivos; x0 debe ser finito.")

    # Interpretación simbólica de f(x); solo se aceptan funciones conocidas y la variable x.
    x = sp.Symbol("x", real=True)
    permitidos = {"x": x, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
                  "exp": sp.exp, "log": sp.log, "ln": sp.log, "sqrt": sp.sqrt,
                  "pi": sp.pi, "E": sp.E, "abs": sp.Abs}
    try:
        f_expr = sp.sympify(str(expresion).replace("^", "**"), locals=permitidos)
        if not isinstance(f_expr, sp.Expr) or (f_expr.free_symbols - {x}):
            raise ValueError
        # Derivada analítica f'(x) obtenida con SymPy.
        df_expr = sp.diff(f_expr, x)
        # Se convierten f y f' en funciones numéricas para evaluarlas rápido.
        f, df = sp.lambdify(x, f_expr, modules=["math"]), sp.lambdify(x, df_expr, modules=["math"])
    except Exception:
        raise ValueError("No se pudo interpretar f(x). Use una expresión válida en x.") from None

    # Evalúa una función y garantiza que el resultado sea un número finito.
    def evaluar(funcion, valor):
        try:
            resultado = float(funcion(valor))
        except Exception:
            raise ValueError(f"No se pudo evaluar la función en x = {valor:g}.") from None
        if not math.isfinite(resultado):
            raise ValueError(f"Se obtuvo un valor no finito en x = {valor:g}.")
        return resultado

    # Si x0 ya cumple |f(x0)| <= tolerancia, no hace falta iterar.
    actual, filas = inicial, []
    residuo = abs(evaluar(f, actual))
    convergio = residuo <= tol
    estado = ("Convergencia alcanzada desde el valor inicial." if convergio else
              f"No se alcanzó el criterio de convergencia: se llegó al máximo de iteraciones ({limite}).")
    if not convergio:
        for i in range(1, limite + 1):
            fx, dfx = evaluar(f, actual), evaluar(df, actual)
            # Antes de dividir: una derivada nula o casi nula detiene el método.
            if abs(dfx) <= 1e-12:
                estado = "Detenido: la derivada es cero o demasiado cercana a cero."
                break
            # Fórmula de Newton-Raphson: x(i+1) = x(i) - f(x(i)) / f'(x(i)).
            siguiente = actual - fx / dfx
            if not math.isfinite(siguiente):
                estado = "Detenido: la aproximación no es finita."
                break
            # Error relativo porcentual; si x(i+1) = 0 se usa el absoluto para no dividir entre cero.
            error = abs(siguiente - actual)
            tipo_error = "Absoluto"
            if siguiente != 0:
                error, tipo_error = error / abs(siguiente) * 100, "Relativo (%)"
            # Residuo |f(x(i+1))|: comprueba qué tan cerca de cero queda la función.
            residuo = abs(evaluar(f, siguiente))
            # Fila de la tabla de iteraciones.
            filas.append({"i": i, "xi": actual, "fx": fx, "dfx": dfx,
                          "xnext": siguiente, "error": error,
                          "tipo": tipo_error, "residuo": residuo})
            actual = siguiente
            # Criterio de parada: error y residuo deben cumplir la tolerancia a la vez.
            if error <= tol and residuo <= tol:
                convergio = True
                estado = "Convergencia alcanzada."
                break
    # Resultado completo para el resumen, la tabla y la gráfica.
    return {
        "funcion": f_expr,
        "derivada": df_expr,
        "x": x,
        "aproximacion": actual,
        "iteraciones": len(filas),
        "max_iteraciones": limite,
        "error": filas[-1]["error"] if filas else None,
        "tipo_error": filas[-1]["tipo"] if filas else "No calculado",
        "residuo": abs(evaluar(f, actual)),
        "estado": estado,
        "convergio": convergio,
        "historial": filas,
        "tolerancia": tol,
    }


def graficar_newton_raphson(resultado, ax=None):
    """Dibuja f(x), el eje x y las aproximaciones de Newton."""
    import numpy as np
    import matplotlib.pyplot as plt
    x = resultado["x"]
    funcion = sp.lambdify(x, resultado["funcion"], modules=["numpy"])
    # Rango del eje x: abarca todas las aproximaciones con un margen alrededor.
    puntos = [resultado["aproximacion"]]
    for fila in resultado["historial"]:
        puntos.extend((fila["xi"], fila["xnext"]))
    centro = sum(puntos) / len(puntos)
    ancho = max(max(puntos) - min(puntos), abs(centro) * 0.5, 2.0)
    malla = np.linspace(min(puntos) - ancho, max(puntos) + ancho, 500)
    # Se evalúa f sobre la malla; los valores no finitos se ocultan (NaN).
    with np.errstate(all="ignore"):
        valores = np.asarray(funcion(malla), dtype=float)
    if valores.ndim == 0:
        valores = np.full_like(malla, float(valores))
    valores = np.where(np.isfinite(valores), valores, np.nan)
    if ax is None:
        figura, ax = plt.subplots(figsize=(7, 4))
    else:
        figura = ax.figure
    ax.plot(malla, valores, label="f(x)")
    ax.axhline(0, color="black", linewidth=0.8)
    # Recta tangente de cada iteración, desde (xi, f(xi)) hasta su corte con el eje x.
    for fila in resultado["historial"]:
        xx = np.linspace(fila["xi"], fila["xnext"], 30)
        ax.plot(xx, fila["fx"] + fila["dfx"] * (xx - fila["xi"]), "--", alpha=0.5)
        ax.scatter([fila["xi"]], [fila["fx"]], s=18)
    # Solo se rotula como raíz aproximada si el método convergió.
    if resultado["convergio"]:
        ax.scatter([resultado["aproximacion"]], [0], color="red", zorder=4, label="Raíz aproximada")
    else:
        ax.scatter([resultado["aproximacion"]], [0], color="gray", marker="x", zorder=4,
                   label="Última aproximación (sin convergencia)")
    ax.set_title("Método de Newton-Raphson")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    figura.tight_layout()
    return figura, ax

"""Implementación del método de Newton-Raphson para una función real f(x)."""
import math
import sympy as sp


def resolver_newton_raphson(expresion, x0, tolerancia=1e-6, max_iteraciones=100):
    """Calcula una raíz aproximada y devuelve el procedimiento de cada iteración."""
    try:
        inicial, tol, limite = float(x0), float(tolerancia), int(max_iteraciones)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Revise el valor inicial, la tolerancia y las iteraciones.") from None
    if not all(math.isfinite(v) for v in (inicial, tol)) or tol <= 0 or limite <= 0:
        raise ValueError("La tolerancia y el máximo de iteraciones deben ser positivos; x0 debe ser finito.")

    x = sp.Symbol("x", real=True)
    permitidos = {"x": x, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
                  "exp": sp.exp, "log": sp.log, "ln": sp.log, "sqrt": sp.sqrt,
                  "pi": sp.pi, "E": sp.E, "abs": sp.Abs}
    try:
        f_expr = sp.sympify(str(expresion).replace("^", "**"), locals=permitidos)
        if not isinstance(f_expr, sp.Expr) or (f_expr.free_symbols - {x}):
            raise ValueError
        df_expr = sp.diff(f_expr, x)
        f, df = sp.lambdify(x, f_expr, modules=["math"]), sp.lambdify(x, df_expr, modules=["math"])
    except Exception:
        raise ValueError("No se pudo interpretar f(x). Use una expresión válida en x.") from None

    def evaluar(funcion, valor):
        try:
            resultado = float(funcion(valor))
        except Exception:
            raise ValueError(f"No se pudo evaluar la función en x = {valor:g}.") from None
        if not math.isfinite(resultado):
            raise ValueError(f"Se obtuvo un valor no finito en x = {valor:g}.")
        return resultado

    actual, filas = inicial, []
    residuo = abs(evaluar(f, actual))
    estado = "Convergencia alcanzada desde el valor inicial." if residuo <= tol else "Se alcanzó el máximo de iteraciones."
    if residuo > tol:
        for i in range(1, limite + 1):
            fx, dfx = evaluar(f, actual), evaluar(df, actual)
            if abs(dfx) <= 1e-12:
                estado = "Detenido: la derivada es cero o demasiado cercana a cero."
                break
            siguiente = actual - fx / dfx
            if not math.isfinite(siguiente):
                estado = "Detenido: la aproximación no es finita."
                break
            error = abs(siguiente - actual)
            tipo_error = "Absoluto"
            if siguiente != 0:
                error, tipo_error = error / abs(siguiente) * 100, "Relativo (%)"
            residuo = abs(evaluar(f, siguiente))
            filas.append({"i": i, "xi": actual, "fx": fx, "dfx": dfx,
                          "xnext": siguiente, "error": error,
                          "tipo": tipo_error, "residuo": residuo})
            actual = siguiente
            if error <= tol and residuo <= tol:
                estado = "Convergencia alcanzada."
                break
    return {"funcion": f_expr, "derivada": df_expr, "x": x, "aproximacion": actual,
            "iteraciones": len(filas), "residuo": abs(evaluar(f, actual)),
            "estado": estado, "historial": filas, "tolerancia": tol}


def graficar_newton_raphson(resultado, ax=None):
    """Dibuja f(x), el eje x y las aproximaciones de Newton."""
    import numpy as np
    import matplotlib.pyplot as plt
    x = resultado["x"]
    funcion = sp.lambdify(x, resultado["funcion"], modules=["numpy"])
    puntos = [resultado["aproximacion"]]
    for fila in resultado["historial"]:
        puntos.extend((fila["xi"], fila["xnext"]))
    centro = sum(puntos) / len(puntos)
    ancho = max(max(puntos) - min(puntos), abs(centro) * 0.5, 2.0)
    malla = np.linspace(min(puntos) - ancho, max(puntos) + ancho, 500)
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
    for fila in resultado["historial"]:
        xx = np.linspace(fila["xi"], fila["xnext"], 30)
        ax.plot(xx, fila["fx"] + fila["dfx"] * (xx - fila["xi"]), "--", alpha=0.5)
        ax.scatter([fila["xi"]], [fila["fx"]], s=18)
    ax.scatter([resultado["aproximacion"]], [0], color="red", zorder=4, label="Raíz aproximada")
    ax.set_title("Método de Newton-Raphson")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    figura.tight_layout()
    return figura, ax

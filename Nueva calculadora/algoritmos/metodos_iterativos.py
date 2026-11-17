"""Métodos de Jacobi y Gauss-Seidel para sistemas lineales."""

from itertools import permutations
import math


def preparar_sistema(A, b, x0, tolerancia, max_iteraciones, reordenar=True):
    """Valida entradas y, si se solicita, busca un orden de filas conveniente."""
    n = len(A)
    if n == 0 or any(len(fila) != n for fila in A):
        raise ValueError("A debe ser una matriz cuadrada no vacía.")
    if len(b) != n or len(x0) != n:
        raise ValueError("A, b y x⁽⁰⁾ deben tener la misma dimensión.")
    try:
        A = [[float(v) for v in fila] for fila in A]
        b = [float(v) for v in b]
        x0 = [float(v) for v in x0]
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Todos los datos deben ser numéricos.") from None
    if not all(math.isfinite(v) for fila in A for v in fila) or not all(math.isfinite(v) for v in b + x0):
        raise ValueError("No se permiten valores no finitos.")
    if not math.isfinite(tolerancia) or tolerancia <= 0:
        raise ValueError("La tolerancia debe ser positiva y finita.")
    if max_iteraciones <= 0:
        raise ValueError("El máximo de iteraciones debe ser un entero positivo.")

    permutacion = tuple(range(n))
    dominante = lambda M: all(abs(M[i][i]) > sum(abs(M[i][j]) for j in range(n) if j != i) for i in range(n))
    dominante_inicial = dominante(A)
    necesita_orden = any(A[i][i] == 0 for i in range(n)) or not dominante(A)
    if reordenar and necesita_orden:
        candidatos = []
        for orden in permutations(range(n)):
            if all(A[orden[i]][i] != 0 for i in range(n)):
                candidatos.append(orden)
                if dominante([A[k] for k in orden]):
                    permutacion = orden
                    break
        else:
            if candidatos:
                permutacion = candidatos[0]
    A = [A[i] for i in permutacion]
    b = [b[i] for i in permutacion]
    if any(A[i][i] == 0 for i in range(n)):
        raise ValueError("La diagonal contiene ceros y no se encontró un reordenamiento de ecuaciones con diagonal no nula.")
    return A, b, x0, tolerancia, max_iteraciones, permutacion, dominante_inicial, dominante(A)


def _resolver(A, b, x0, tolerancia, max_iteraciones, metodo):
    n = len(A)
    x = x0[:]
    historial = [{"k": 0, "x": x[:], "error": None}]
    error_anterior = None
    crecientes = 0
    estado = "Máximo de iteraciones"
    for k in range(1, max_iteraciones + 1):
        anterior = x[:]
        nuevo = anterior[:] if metodo == "Jacobi" else x[:]
        for i in range(n):
            base = anterior if metodo == "Jacobi" else nuevo
            suma = sum(A[i][j] * base[j] for j in range(n) if j != i)
            nuevo[i] = (b[i] - suma) / A[i][i]
        if not all(math.isfinite(v) for v in nuevo):
            estado = "Detenido: se generaron valores no finitos"
            break
        error = max(abs(nuevo[i] - anterior[i]) for i in range(n))
        historial.append({"k": k, "x": nuevo[:], "error": error})
        x = nuevo
        if error <= tolerancia:
            estado = "Convergencia alcanzada"
            break
        if error_anterior is not None and error > error_anterior:
            crecientes += 1
        else:
            crecientes = 0
        if crecientes >= 8:
            estado = "Advertencia: el error creció repetidamente; posible no convergencia"
            break
        error_anterior = error
    residuo = max(abs(sum(A[i][j] * x[j] for j in range(n)) - b[i]) for i in range(n))
    return {"metodo": metodo, "x": x, "historial": historial, "iteraciones": len(historial) - 1,
            "estado": estado, "residuo": residuo}


def resolver_iterativos(A, b, x0, tolerancia=1e-6, max_iteraciones=100, reordenar=True):
    """Ejecuta ambos métodos con el mismo criterio y devuelve diagnóstico y resultados."""
    A, b, x0, tolerancia, max_iteraciones, permutacion, dominante_inicial, dominante = preparar_sistema(
        A, b, x0, tolerancia, max_iteraciones, reordenar
    )
    return {"A": A, "b": b, "x0": x0, "permutacion": permutacion,
            "diagonal_dominante_inicial": dominante_inicial,
            "diagonal_dominante": dominante,
            "jacobi": _resolver(A, b, x0, tolerancia, max_iteraciones, "Jacobi"),
            "gauss_seidel": _resolver(A, b, x0, tolerancia, max_iteraciones, "Gauss-Seidel")}

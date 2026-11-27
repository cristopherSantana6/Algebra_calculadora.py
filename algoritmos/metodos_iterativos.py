"""
Métodos iterativos de Jacobi y Gauss-Seidel para sistemas Ax = b.
La implementación usa listas y aritmética de punto flotante; no delega
la solución en bibliotecas externas.
"""

import math
from fractions import Fraction


def _numero(valor, nombre):
    """Convierte enteros, decimales y fracciones a un real finito."""
    try:
        if isinstance(valor, str):
            texto = valor.strip().replace(",", ".")
            if not texto:
                raise ValueError
            numero = float(Fraction(texto))
        else:
            numero = float(valor)
    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        raise ValueError(f"{nombre} debe ser un número válido.") from None
    if not math.isfinite(numero):
        raise ValueError(f"{nombre} debe ser un número finito.")
    return numero


def preparar_sistema(matriz, vector, aproximacion_inicial=None):
    """
    Valida y convierte Ax=b. La matriz debe ser cuadrada y tener
    diagonal no nula; no cambia el orden de las ecuaciones.
    """
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError("Debe ingresar una matriz de coeficientes.")

    n = len(matriz)
    if not isinstance(vector, (list, tuple)) or len(vector) != n:
        raise ValueError("El vector b debe tener la misma cantidad de filas que A.")

    A = []
    for i, fila in enumerate(matriz):
        if not isinstance(fila, (list, tuple)) or len(fila) != n:
            raise ValueError("La matriz A debe ser cuadrada.")
        A.append([
            _numero(valor, f"A[{i + 1},{j + 1}]")
            for j, valor in enumerate(fila)
        ])

    b = [_numero(valor, f"b[{i + 1}]") for i, valor in enumerate(vector)]

    if aproximacion_inicial is None:
        x0 = [0.0] * n
    else:
        if not isinstance(aproximacion_inicial, (list, tuple)) or len(aproximacion_inicial) != n:
            raise ValueError("La aproximación inicial debe tener una entrada por incógnita.")
        x0 = [
            _numero(valor, f"x0[{i + 1}]")
            for i, valor in enumerate(aproximacion_inicial)
        ]

    for i in range(n):
        if abs(A[i][i]) <= 1e-15:
            raise ValueError(
                f"El elemento diagonal A[{i + 1},{i + 1}] es cero o demasiado pequeño. "
                "Reordene las ecuaciones para obtener una diagonal no nula."
            )

    return A, b, x0


def _residuo_infinito(A, b, x):
    """Calcula ||Ax-b||_infinito."""
    return max(
        abs(sum(A[i][j] * x[j] for j in range(len(x))) - b[i])
        for i in range(len(x))
    )


def _dominancia_diagonal(A):
    """Comprueba dominancia diagonal estricta por filas."""
    return all(
        abs(A[i][i]) > sum(abs(A[i][j]) for j in range(len(A)) if j != i)
        for i in range(len(A))
    )


def resolver_iterativos(
    matriz,
    vector,
    aproximacion_inicial=None,
    tolerancia=1e-6,
    max_iteraciones=100,
    metodo="jacobi",
):
    """
    Resuelve Ax=b mediante Jacobi o Gauss-Seidel.

    Criterio de parada: max_i |x_i^(k+1)-x_i^k| <= tolerancia.
    También registra el residuo infinito ||Ax-b||_infinito en cada paso.
    """
    A, b, anterior = preparar_sistema(
        matriz, vector, aproximacion_inicial
    )
    tolerancia = _numero(tolerancia, "La tolerancia")
    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    try:
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("El máximo de iteraciones debe ser un entero.") from None
    if max_iteraciones < 1:
        raise ValueError("El máximo de iteraciones debe ser al menos 1.")

    clave = str(metodo).strip().lower().replace("_", "-")
    if clave in ("jacobi", "j"):
        clave = "jacobi"
        nombre = "Jacobi"
    elif clave in ("gauss-seidel", "gauss seidel", "seidel", "gs"):
        clave = "gauss-seidel"
        nombre = "Gauss-Seidel"
    else:
        raise ValueError("Método no reconocido. Use 'jacobi' o 'gauss-seidel'.")

    n = len(A)
    dominante = _dominancia_diagonal(A)
    historial = [{
        "iteracion": 0,
        "aproximacion": anterior.copy(),
        "error": None,
        "residuo": _residuo_infinito(A, b, anterior),
    }]
    convergio = False
    error = None

    for k in range(1, max_iteraciones + 1):
        if clave == "jacobi":
            nuevo = [0.0] * n
            for i in range(n):
                suma = sum(
                    A[i][j] * anterior[j]
                    for j in range(n) if j != i
                )
                nuevo[i] = (b[i] - suma) / A[i][i]
        else:
            # Los componentes ya actualizados se usan inmediatamente.
            nuevo = anterior.copy()
            for i in range(n):
                suma_inferior = sum(
                    A[i][j] * nuevo[j] for j in range(i)
                )
                suma_superior = sum(
                    A[i][j] * anterior[j] for j in range(i + 1, n)
                )
                nuevo[i] = (
                    b[i] - suma_inferior - suma_superior
                ) / A[i][i]

        if not all(math.isfinite(valor) for valor in nuevo):
            raise ValueError(
                "El cálculo produjo valores no finitos. El método puede estar divergiendo."
            )

        error = max(abs(nuevo[i] - anterior[i]) for i in range(n))
        residuo = _residuo_infinito(A, b, nuevo)
        historial.append({
            "iteracion": k,
            "aproximacion": nuevo.copy(),
            "error": error,
            "residuo": residuo,
        })
        anterior = nuevo

        if error <= tolerancia:
            convergio = True
            break

    if convergio:
        estado = "Convergencia alcanzada: el cambio máximo es menor o igual que la tolerancia."
    else:
        estado = (
            "No se alcanzó la tolerancia dentro del máximo de iteraciones. "
            "La aproximación final no debe considerarse convergida."
        )

    if dominante:
        diagnostico = (
            "La matriz tiene dominancia diagonal estricta por filas, "
            "condición suficiente de convergencia para ambos métodos."
        )
    else:
        diagnostico = (
            "La matriz no presenta dominancia diagonal estricta por filas. "
            "Esto no demuestra divergencia; la convergencia debe comprobarse con los resultados."
        )

    return {
        "metodo": nombre,
        "solucion": anterior.copy(),
        "iteraciones": len(historial) - 1,
        "convergio": convergio,
        "estado": estado,
        "tolerancia": tolerancia,
        "error": error,
        "residuo": _residuo_infinito(A, b, anterior),
        "dominancia_diagonal": dominante,
        "diagnostico": diagnostico,
        "historial": historial,
    }


def resolver_jacobi(matriz, vector, aproximacion_inicial=None,
                    tolerancia=1e-6, max_iteraciones=100):
    """Atajo para ejecutar el método de Jacobi."""
    return resolver_iterativos(
        matriz, vector, aproximacion_inicial,
        tolerancia, max_iteraciones, metodo="jacobi"
    )


def resolver_gauss_seidel(matriz, vector, aproximacion_inicial=None,
                          tolerancia=1e-6, max_iteraciones=100):
    """Atajo para ejecutar el método de Gauss-Seidel."""
    return resolver_iterativos(
        matriz, vector, aproximacion_inicial,
        tolerancia, max_iteraciones, metodo="gauss-seidel"
    )

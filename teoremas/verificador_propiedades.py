"""Verificador de teoremas de matrices, inversas y determinantes (Módulo III y Programa 6).

Calcula ambos miembros de cada igualdad con las funciones de modulos/ y emite el diagnóstico
«Se cumple» o «No se cumple». Los resultados intermedios se calculan una sola vez y se reutilizan.
Unidad: Álgebra Lineal (MTM0120), Universidad Americana.
Elaborado por: Patricia del Carmen Oquist Talavera, Cristopher Rafael Santana Ríos y Rafael Antonio Arauz Navarro
"""

from fractions import Fraction

from modulos.modulo_gauss import copiar_matriz, intercambiar_filas
from modulos.modulo_matrices import (
    determinante_cofactores,
    inversa,
    matriz_cero,
    matriz_identidad,
    multiplicar_matriz_escalar,
    multiplicar_matrices,
    son_iguales,
    sumar_matrices,
    trasponer_matriz,
    validar_matriz,
)


def _calcular_una_vez(calculo):
    """Devuelve una función que ejecuta `calculo` solo la primera vez y reutiliza su resultado o su ValueError."""
    memoria = {}

    def obtener():
        if not memoria:
            try:
                memoria["valor"] = calculo()
            except ValueError as error:
                memoria["error"] = error
        if "error" in memoria:
            raise memoria["error"]
        return memoria["valor"]

    return obtener


def _como_fracciones(matriz):
    """Devuelve una copia de la matriz con todas sus entradas como Fraction (None se conserva)."""
    return None if matriz is None else [[Fraction(valor) for valor in fila] for fila in matriz]


def _matriz_triangular_superior(matriz):
    """Devuelve A con ceros bajo la diagonal principal; ValueError si A no es cuadrada."""
    determinante_cofactores(matriz)
    return [[valor if columna >= fila else Fraction(0) for columna, valor in enumerate(fila_valores)]
            for fila, fila_valores in enumerate(matriz)]


def _determinante_y_producto_diagonal(matriz_triangular):
    """Devuelve (det de una matriz triangular, producto de sus entradas diagonales)."""
    producto_diagonal = Fraction(1)
    for indice, fila in enumerate(matriz_triangular):
        producto_diagonal *= fila[indice]
    return determinante_cofactores(matriz_triangular), producto_diagonal


def _reemplazar_fila_0(matriz, multiplicador):
    """En sitio: F₀ ← F₀ + multiplicador · F₁."""
    matriz[0] = [x + multiplicador * y for x, y in zip(matriz[0], matriz[1])]


def _escalar_fila_0(matriz, escalar):
    """En sitio: F₀ ← escalar · F₀."""
    matriz[0] = [escalar * x for x in matriz[0]]


def _efecto_de_fila(matriz, operacion, factor_esperado):
    """Devuelve (det de A tras `operacion` de fila, factor_esperado · det(A)); exige A cuadrada de 2×2 o más."""
    determinante_original = determinante_cofactores(matriz)
    if len(matriz) < 2:
        raise ValueError("Se necesitan al menos 2 filas para operar entre ellas.")
    matriz_operada = copiar_matriz(matriz)
    operacion(matriz_operada)
    return determinante_cofactores(matriz_operada), factor_esperado * determinante_original


def verificar_propiedades(matriz_a, matriz_b=None, matriz_c=None, escalar_r=2, escalar_s=3):
    """Calcula ambos miembros de 26 igualdades de matrices, inversas y determinantes.
    Devuelve una lista de diccionarios (nombre, aplica, izquierda, derecha, cumple, diagnostico, informativa, motivo).
    Si falta una matriz o una condición (dimensiones, cuadrada, det ≠ 0), aplica = False y motivo lo explica.
    """
    validar_matriz(matriz_a)
    for otra in (matriz_b, matriz_c):
        if otra is not None:
            validar_matriz(otra)
    a, b, c = _como_fracciones(matriz_a), _como_fracciones(matriz_b), _como_fracciones(matriz_c)
    r, s = Fraction(escalar_r), Fraction(escalar_s)
    resultados = []

    # Cada intermedio se calcula una vez y alimenta a todas las propiedades que lo usan.
    a_t = _calcular_una_vez(lambda: trasponer_matriz(a))
    b_t = _calcular_una_vez(lambda: trasponer_matriz(b))
    a_b = _calcular_una_vez(lambda: multiplicar_matrices(a, b))
    b_a = _calcular_una_vez(lambda: multiplicar_matrices(b, a))
    b_mas_c = _calcular_una_vez(lambda: sumar_matrices(b, c))
    a_inversa = _calcular_una_vez(lambda: inversa(a))
    b_inversa = _calcular_una_vez(lambda: inversa(b))
    det_a = _calcular_una_vez(lambda: determinante_cofactores(a))

    def propiedad(nombre, calcular, usa="", informativa=False):
        """Evalúa `calcular()` → (izquierda, derecha) y registra el diagnóstico de la igualdad."""
        faltan = [letra for letra, matriz in zip("BC", (b, c)) if letra in usa and matriz is None]
        registro = {"nombre": nombre, "aplica": False, "izquierda": None, "derecha": None,
                    "cumple": None, "diagnostico": None, "informativa": informativa, "motivo": None}
        if faltan:
            registro["motivo"] = f"Falta la matriz {faltan[0]}."
        else:
            try:
                izquierda, derecha = calcular()
            except ValueError as error:
                registro["motivo"] = str(error)
            else:
                if isinstance(izquierda, list):
                    cumple = son_iguales(izquierda, derecha)
                else:
                    cumple = izquierda == derecha
                registro.update(aplica=True, izquierda=izquierda, derecha=derecha, cumple=cumple,
                                diagnostico="Se cumple" if cumple else "No se cumple")
        resultados.append(registro)

    propiedad("A + B = B + A", lambda: (sumar_matrices(a, b), sumar_matrices(b, a)), "B")
    propiedad("(A + B) + C = A + (B + C)",
              lambda: (sumar_matrices(sumar_matrices(a, b), c), sumar_matrices(a, b_mas_c())), "BC")
    propiedad("A + 0 = A", lambda: (sumar_matrices(a, matriz_cero(len(a), len(a[0]))), a))
    propiedad("r(A + B) = rA + rB",
              lambda: (multiplicar_matriz_escalar(sumar_matrices(a, b), r),
                       sumar_matrices(multiplicar_matriz_escalar(a, r), multiplicar_matriz_escalar(b, r))), "B")
    propiedad("(r + s)A = rA + sA",
              lambda: (multiplicar_matriz_escalar(a, r + s),
                       sumar_matrices(multiplicar_matriz_escalar(a, r), multiplicar_matriz_escalar(a, s))))
    propiedad("r(sA) = (rs)A",
              lambda: (multiplicar_matriz_escalar(multiplicar_matriz_escalar(a, s), r),
                       multiplicar_matriz_escalar(a, r * s)))
    propiedad("(AB)C = A(BC)",
              lambda: (multiplicar_matrices(a_b(), c), multiplicar_matrices(a, multiplicar_matrices(b, c))), "BC")
    propiedad("A(B + C) = AB + AC",
              lambda: (multiplicar_matrices(a, b_mas_c()), sumar_matrices(a_b(), multiplicar_matrices(a, c))), "BC")
    propiedad("A · I = A", lambda: (multiplicar_matrices(a, matriz_identidad(len(a[0]))), a))
    propiedad("A · B = B · A  (el producto NO es conmutativo)",
              lambda: (a_b(), b_a()), "B", informativa=True)
    propiedad("(Aᵀ)ᵀ = A", lambda: (trasponer_matriz(a_t()), a))
    propiedad("(A + B)ᵀ = Aᵀ + Bᵀ",
              lambda: (trasponer_matriz(sumar_matrices(a, b)), sumar_matrices(a_t(), b_t())), "B")
    propiedad("(kA)ᵀ = kAᵀ",
              lambda: (trasponer_matriz(multiplicar_matriz_escalar(a, r)), multiplicar_matriz_escalar(a_t(), r)))
    propiedad("(AB)ᵀ = BᵀAᵀ",
              lambda: (trasponer_matriz(a_b()), multiplicar_matrices(b_t(), a_t())), "B")
    propiedad("(A⁻¹)⁻¹ = A", lambda: (inversa(a_inversa()), a))
    propiedad("(AB)⁻¹ = B⁻¹A⁻¹",
              lambda: (inversa(a_b()), multiplicar_matrices(b_inversa(), a_inversa())), "B")
    propiedad("(Aᵀ)⁻¹ = (A⁻¹)ᵀ", lambda: (inversa(a_t()), trasponer_matriz(a_inversa())))
    propiedad("A · A⁻¹ = I", lambda: (multiplicar_matrices(a, a_inversa()), matriz_identidad(len(a))))
    propiedad("det(Aᵀ) = det(A)", lambda: (determinante_cofactores(a_t()), det_a()))
    propiedad("det(AB) = det(A) · det(B)",
              lambda: (determinante_cofactores(a_b()), det_a() * determinante_cofactores(b)), "B")
    propiedad("det(A⁻¹) = 1/det(A)", lambda: (determinante_cofactores(a_inversa()), 1 / det_a()))
    propiedad("det(kA) = kⁿ · det(A)",
              lambda: (determinante_cofactores(multiplicar_matriz_escalar(a, r)), r ** len(a) * det_a()))
    propiedad("Intercambiar dos filas cambia el signo del det",
              lambda: _efecto_de_fila(a, lambda matriz: intercambiar_filas(matriz, 0, 1), -1))
    propiedad("Reemplazar F₀ por F₀ + r·F₁ conserva el det",
              lambda: _efecto_de_fila(a, lambda matriz: _reemplazar_fila_0(matriz, r), 1))
    propiedad("Multiplicar una fila por r escala el det por r",
              lambda: _efecto_de_fila(a, lambda matriz: _escalar_fila_0(matriz, r), r))
    propiedad("det(triangular) = producto de la diagonal",
              lambda: _determinante_y_producto_diagonal(_matriz_triangular_superior(a)))
    return resultados


"""Módulo para realizar operaciones básicas con matrices.
Implementa contenidos de Álgebra Lineal relacionados con operaciones matriciales.
Utiliza únicamente herramientas de la biblioteca estándar de Python.
Elaborado por: Patricia del Carmen Oquist Talavera y Cristopher Rafael Santana Ríos
"""


from fractions import Fraction

from utilidades.formato import formatear_operacion_eliminacion


def validar_matriz(matriz):
    """Valida que la matriz sea rectangular y no esté vacía.
       Recibe una lista de filas y no devuelve un valor; genera ValueError si es inválida.
       """
    if not matriz or not matriz[0]:
        raise ValueError("La matriz no puede estar vacía.")
    columnas = len(matriz[0])
    if any(len(fila) != columnas for fila in matriz):
        raise ValueError("La matriz debe ser rectangular.")


def validar_mismas_dimensiones(a, b):
    """Comprueba que dos matrices tengan las mismas dimensiones.
    Recibe las matrices A y B y no devuelve un valor; genera ValueError si difieren.
    """
    validar_matriz(a)
    validar_matriz(b)
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones.")


def sumar_matrices(a, b):
    """Suma dos matrices de igual dimensión.
        Recibe A y B y devuelve una matriz con la suma de sus entradas correspondientes.
        """
    validar_mismas_dimensiones(a, b)
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def restar_matrices(a, b):
    """Resta dos matrices de igual dimensión.
        Recibe A y B y devuelve una matriz con las diferencias de sus entradas correspondientes.
        """
    validar_mismas_dimensiones(a, b)
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def multiplicar_matriz_escalar(a, escalar):
    """Multiplica una matriz por un escalar.
       Recibe una matriz A y un número; devuelve la matriz cA.
       """
    validar_matriz(a)
    return [[escalar * valor for valor in fila] for fila in a]


def multiplicar_matrices(a, b):
    """Calcula el producto matricial AB mediante productos fila por columna.
        Recibe A y B compatibles y devuelve una matriz de dimensión filas(A) × columnas(B).
        """
    validar_matriz(a)
    validar_matriz(b)
    filas_a, columnas_a = len(a), len(a[0])
    filas_b, columnas_b = len(b), len(b[0])

    # El producto matricial solo está definido cuando las dimensiones internas coinciden.
    if columnas_a != filas_b:
        raise ValueError(
            "No se pueden multiplicar: las columnas de A deben ser iguales a las filas de B."
        )

    resultado = []
    for i in range(filas_a):
        fila_resultado = []
        for j in range(columnas_b):
            suma = Fraction(0)
            for k in range(columnas_a):
                suma += a[i][k] * b[k][j]
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado


def trasponer_matriz(a):
    """Calcula la transpuesta de una matriz.
       Recibe una matriz A de dimensión m × n y devuelve Aᵀ de dimensión n × m.
       """
    validar_matriz(a)
    filas, columnas = len(a), len(a[0])
    return [[a[i][j] for i in range(filas)] for j in range(columnas)]


def validar_cuadrada(a):
    """Comprueba que A sea cuadrada; requisito para el determinante y la inversa."""
    validar_matriz(a)
    if len(a) != len(a[0]):
        raise ValueError("La matriz debe ser cuadrada (n×n).")


def menor(a, i, j):
    """Devuelve la submatriz M_ij: A sin la fila i ni la columna j."""
    return [
        [a[f][c] for c in range(len(a[0])) if c != j]
        for f in range(len(a)) if f != i
    ]


def determinante(a):
    """Calcula det(A) por eliminación por filas con fracciones exactas."""
    # Atajo usado por la adjunta: det(M_ij) por reducción de filas.
    if not a:
        return Fraction(1)  # Convención: el menor de una matriz 1×1 es vacío.
    return determinante_reduccion(a)["determinante"]


def determinante_reduccion(a):
    """Calcula det(A) llevando A a forma triangular superior y guarda cada paso.

    Reglas usadas:
    - Intercambiar dos filas cambia el signo del determinante.
    - Sumar a una fila un múltiplo de otra NO cambia el determinante.
    - El determinante de una matriz triangular es el producto de su diagonal.
    Si una columna queda sin pivote, la matriz es singular y det(A) = 0.
    """
    validar_cuadrada(a)
    m = [[Fraction(valor) for valor in fila] for fila in a]
    n = len(m)
    signo = 1
    pasos = [{
        "titulo": "Matriz inicial",
        "operacion": "Se busca llevar A a forma triangular superior.",
        "nota": None,
        "matriz": [fila[:] for fila in m],
    }]

    for col in range(n):
        # Se toma como pivote el primer valor distinto de cero, como en papel.
        fila_pivote = next((f for f in range(col, n) if m[f][col] != 0), None)
        if fila_pivote is None:
            pasos.append({
                "titulo": f"Columna {col + 1} sin pivote",
                "operacion": f"Desde la fila {col + 1} hacia abajo, la columna {col + 1} solo tiene ceros.",
                "nota": "La matriz es singular: su determinante es 0.",
                "matriz": [fila[:] for fila in m],
            })
            return {"determinante": Fraction(0), "signo": signo, "triangular": m,
                    "diagonal": None, "pasos": pasos}

        if fila_pivote != col:
            m[col], m[fila_pivote] = m[fila_pivote], m[col]
            signo = -signo
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{col + 1} ↔ R{fila_pivote + 1}",
                "nota": f"Intercambiar filas cambia el signo del determinante (signo acumulado: {signo}).",
                "matriz": [fila[:] for fila in m],
            })

        # Se anula cada entrada bajo el pivote: Rf ← Rf − factor·Rcol (no cambia det).
        for f in range(col + 1, n):
            factor = m[f][col] / m[col][col]
            if factor == 0:
                continue
            m[f] = [x - factor * y for x, y in zip(m[f], m[col])]
            pasos.append({
                "titulo": "Eliminación debajo del pivote",
                "operacion": formatear_operacion_eliminacion(f + 1, col + 1, factor),
                "nota": "Sumar a una fila un múltiplo de otra no cambia el determinante.",
                "matriz": [fila[:] for fila in m],
            })

    # det = (±1 por los intercambios) · producto de la diagonal triangular.
    diagonal = [m[k][k] for k in range(n)]
    resultado = Fraction(signo)
    for valor in diagonal:
        resultado *= valor
    return {"determinante": resultado, "signo": signo, "triangular": m,
            "diagonal": diagonal, "pasos": pasos}


def _fila_con_mas_ceros(a):
    """Índice de la fila con más ceros; desarrollar por ella ahorra cálculos."""
    return max(range(len(a)), key=lambda f: sum(1 for x in a[f] if x == 0))


def determinante_cofactores(a):
    """Calcula det(A) por desarrollo de cofactores (Laplace), de forma recursiva.

    1×1 → a₁₁;  2×2 → ad − bc;  n×n → Σⱼ a_fj · (−1)^(f+j) · det(M_fj),
    desarrollando por la fila f con más ceros (los términos con a_fj = 0 valen 0).
    """
    n = len(a)
    # Casos base de la recursión: 1×1 y 2×2.
    if n == 1:
        return Fraction(a[0][0])
    if n == 2:
        return Fraction(a[0][0]) * a[1][1] - Fraction(a[0][1]) * a[1][0]
    f = _fila_con_mas_ceros(a)
    total = Fraction(0)
    for j in range(n):
        if a[f][j] == 0:
            continue
        # Signo del cofactor: tablero de ajedrez (−1)^(f+j).
        signo = 1 if (f + j) % 2 == 0 else -1
        total += a[f][j] * signo * determinante_cofactores(menor(a, f, j))
    return total


def desarrollo_cofactores(a):
    """Devuelve el primer nivel del desarrollo por cofactores para mostrarlo paso a paso.

    Cada término guarda la entrada a_fj, el signo (−1)^(f+j), el menor M_fj,
    su determinante y el producto a_fj · C_fj.
    """
    validar_cuadrada(a)
    n = len(a)
    # Misma fila que usa determinante_cofactores; aquí solo se guarda el primer nivel para mostrarlo.
    f = _fila_con_mas_ceros(a) if n > 1 else 0
    terminos = []
    for j in range(n):
        signo = 1 if (f + j) % 2 == 0 else -1
        sub = menor(a, f, j)
        # Si la entrada es 0, el término vale 0 y no hace falta calcular su menor.
        det_menor = None if a[f][j] == 0 else (determinante_cofactores(sub) if sub else Fraction(1))
        producto = Fraction(0) if det_menor is None else Fraction(a[f][j]) * signo * det_menor
        terminos.append({
            "columna": j, "valor": a[f][j], "signo": signo,
            "menor": sub, "det_menor": det_menor, "producto": producto,
        })
    return {
        "fila": f,
        "terminos": terminos,
        "determinante": sum((t["producto"] for t in terminos), Fraction(0)),
    }


def determinante_sarrus(a):
    """Calcula det(A) de una matriz 3×3 con la regla de Sarrus.

    Suma los productos de las tres diagonales descendentes y resta los de las
    tres ascendentes (al repetir las dos primeras columnas a la derecha de A).
    Devuelve las entradas y el producto de cada diagonal para mostrarlas.
    """
    validar_cuadrada(a)
    if len(a) != 3:
        raise ValueError("La regla de Sarrus solo aplica a matrices 3×3.")
    a = [[Fraction(valor) for valor in fila] for fila in a]
    principales, secundarias = [], []
    for k in range(3):
        # El "% 3" equivale a repetir las dos primeras columnas, sin armar una matriz 3×5.
        # Diagonal descendente que empieza en la columna k y ascendente que empieza en la k.
        principales.append([a[i][(k + i) % 3] for i in range(3)])
        secundarias.append([a[2 - i][(k + i) % 3] for i in range(3)])

    def producto(entradas):
        return entradas[0] * entradas[1] * entradas[2]

    prod_principales = [producto(d) for d in principales]
    prod_secundarias = [producto(d) for d in secundarias]
    # det(A) = suma de las diagonales ↘ menos suma de las diagonales ↗.
    return {
        "principales": principales, "secundarias": secundarias,
        "prod_principales": prod_principales, "prod_secundarias": prod_secundarias,
        "suma_principales": sum(prod_principales, Fraction(0)),
        "suma_secundarias": sum(prod_secundarias, Fraction(0)),
        "determinante": sum(prod_principales, Fraction(0)) - sum(prod_secundarias, Fraction(0)),
    }


def resolver_cramer(a, b):
    """Resuelve Ax = b con la regla de Cramer: xᵢ = det(Aᵢ) / det(A).

    A debe ser cuadrada n×n con det(A) ≠ 0 y b una lista de n valores.
    Aᵢ es A con su columna i sustituida por b. Devuelve det(A), cada Aᵢ con su
    determinante y la solución x.
    """
    validar_cuadrada(a)
    n = len(a)
    if len(b) != n:
        raise ValueError("El vector b debe tener tantas entradas como filas tiene A.")
    det_a = determinante_cofactores(a)
    if det_a == 0:
        # Sin det(A) ≠ 0 no hay solución única y no se puede dividir.
        raise ValueError(
            "det(A) = 0: la regla de Cramer no aplica (el sistema no tiene solución única)."
        )
    pasos = []
    for i in range(n):
        # Aᵢ: copia de A con la columna i reemplazada por b.
        a_i = [fila[:i] + [b[f]] + fila[i + 1:] for f, fila in enumerate(a)]
        det_i = determinante_cofactores(a_i)
        pasos.append({"columna": i, "matriz": a_i, "determinante": det_i, "x": det_i / det_a})
    return {"determinante": det_a, "pasos": pasos, "solucion": [p["x"] for p in pasos]}


def matriz_cofactores(a):
    """Calcula la matriz de cofactores: C_ij = (-1)^(i+j) · det(M_ij)."""
    validar_cuadrada(a)
    n = len(a)
    # Un cofactor por entrada: signo de ajedrez por el determinante de su menor.
    return [
        [(1 if (i + j) % 2 == 0 else -1) * determinante(menor(a, i, j)) for j in range(n)]
        for i in range(n)
    ]


def matriz_adjunta(a):
    """La adjunta es la traspuesta de la matriz de cofactores: adj(A) = Cᵀ."""
    return trasponer_matriz(matriz_cofactores(a))


def inversa_por_adjunta(a):
    """Calcula A⁻¹ = (1/det A) · adj(A) y devuelve también los pasos intermedios."""
    validar_cuadrada(a)
    det = determinante(a)
    if det == 0:
        raise ValueError("La matriz es singular (det = 0): no tiene inversa.")
    cofactores = matriz_cofactores(a)
    # adj(A) = Cᵀ; A⁻¹ = adj(A) / det(A).
    adjunta = trasponer_matriz(cofactores)
    return {
        "determinante": det,
        "cofactores": cofactores,
        "adjunta": adjunta,
        "inversa": multiplicar_matriz_escalar(adjunta, Fraction(1) / det),
    }


def multiplicar_matriz_vector(matriz, vector):
    """Calcula el producto de una matriz por un vector.
       Recibe una matriz A y un vector compatible; devuelve un vector de longitud filas(A).
       """
    validar_matriz(matriz)

    if not vector:
        raise ValueError("El vector no puede estar vacío.")

    if len(matriz[0]) != len(vector):
        raise ValueError(
            "No se puede calcular A·v: las columnas de A deben coincidir con la dimensión del vector."
        )

    return [
        sum(
            (matriz[i][j] * vector[j] for j in range(len(vector))),
            Fraction(0)
        )
        for i in range(len(matriz))
    ]


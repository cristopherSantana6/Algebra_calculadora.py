
"""Módulo para realizar operaciones básicas con matrices.
Implementa contenidos de Álgebra Lineal relacionados con operaciones matriciales.
Utiliza únicamente herramientas de la biblioteca estándar de Python.
Elaborado por: Patricia del Carmen Oquist Talavera y Cristopher Rafael Santana Ríos
"""


from fractions import Fraction


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
        raise ValueError("La matriz debe ser cuadrada (n×n) para calcular su inversa.")


def menor(a, i, j):
    """Devuelve la submatriz M_ij: A sin la fila i ni la columna j."""
    return [
        [a[f][c] for c in range(len(a[0])) if c != j]
        for f in range(len(a)) if f != i
    ]


def determinante(a):
    """Calcula det(A) por eliminación por filas con fracciones exactas.

    Cada intercambio de filas cambia el signo del determinante; al final,
    det(A) es el producto de la diagonal de la matriz triangular obtenida.
    """
    if not a:
        return Fraction(1)  # Convención: el menor de una matriz 1×1 es vacío.
    m = [[Fraction(valor) for valor in fila] for fila in a]
    n = len(m)
    signo = 1
    for col in range(n):
        fila_pivote = next((f for f in range(col, n) if m[f][col] != 0), None)
        if fila_pivote is None:
            return Fraction(0)  # Columna sin pivote: la matriz es singular.
        if fila_pivote != col:
            m[col], m[fila_pivote] = m[fila_pivote], m[col]
            signo = -signo
        for f in range(col + 1, n):
            factor = m[f][col] / m[col][col]
            for c in range(col, n):
                m[f][c] -= factor * m[col][c]
    resultado = Fraction(signo)
    for k in range(n):
        resultado *= m[k][k]
    return resultado


def matriz_cofactores(a):
    """Calcula la matriz de cofactores: C_ij = (-1)^(i+j) · det(M_ij)."""
    validar_cuadrada(a)
    n = len(a)
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


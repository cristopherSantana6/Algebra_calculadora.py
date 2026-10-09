
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


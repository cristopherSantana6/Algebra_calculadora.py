"""Módulo III de la Calculadora: operaciones con matrices en un solo lugar reutilizable.

Reúne suma, resta, multiplicación por un escalar, producto matricial, transposición,
determinantes (cofactores, reducción de filas y Sarrus), regla de Cramer, inversa por la
matriz adjunta y por Gauss-Jordan, y un verificador de propiedades con el que el propio
programa comprueba las igualdades vistas en clase.

Antes de operar se validan las condiciones de cada operación: dimensiones compatibles,
matriz cuadrada y determinante distinto de cero. Todo se calcula con listas, bucles y
Fraction (aritmética exacta); no usa NumPy, SciPy ni funciones de álgebra lineal de math.
Unidad: Módulo III (matrices) de Álgebra Lineal (MTM0120), Universidad Americana.
Elaborado por: Patricia del Carmen Oquist Talavera, Cristopher Rafael Santana Ríos y Rafael Antonio Arauz Navarro
"""

from fractions import Fraction

from utilidades.formato import formatear_operacion_eliminacion
from utilidades.fracciones import formatear_fraccion


def validar_matriz(matriz):
    """Valida que la matriz sea rectangular y no esté vacía.
       Recibe una lista de filas y no devuelve un valor; genera ValueError si es inválida.
       """
    if not matriz or not matriz[0]:
        raise ValueError("La matriz no puede estar vacía.")
    columnas = len(matriz[0])
    if any(len(fila) != columnas for fila in matriz):
        raise ValueError("La matriz debe ser rectangular.")
    if any(isinstance(valor, bool) or not isinstance(valor, (int, Fraction)) for fila in matriz for valor in fila):
        raise ValueError("Todas las entradas de la matriz deben ser números enteros o fracciones.")


def son_iguales(matriz_a, matriz_b):
    """Devuelve True si ambas matrices tienen las mismas dimensiones y entradas iguales."""
    return len(matriz_a) == len(matriz_b) and all(
        len(fila_a) == len(fila_b) and all(x == y for x, y in zip(fila_a, fila_b))
        for fila_a, fila_b in zip(matriz_a, matriz_b)
    )


def validar_mismas_dimensiones(matriz_a, matriz_b):
    """Comprueba que dos matrices tengan las mismas dimensiones.
    Recibe las matrices A y B y no devuelve un valor; genera ValueError si difieren.
    """
    validar_matriz(matriz_a)
    validar_matriz(matriz_b)
    if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones.")


def sumar_matrices(matriz_a, matriz_b):
    """Suma dos matrices de igual dimensión.
        Recibe A y B y devuelve una matriz con la suma de sus entradas correspondientes.
        """
    validar_mismas_dimensiones(matriz_a, matriz_b)
    return [[matriz_a[i][j] + matriz_b[i][j] for j in range(len(matriz_a[0]))] for i in range(len(matriz_a))]


def restar_matrices(matriz_a, matriz_b):
    """Resta dos matrices de igual dimensión.
        Recibe A y B y devuelve una matriz con las diferencias de sus entradas correspondientes.
        """
    validar_mismas_dimensiones(matriz_a, matriz_b)
    return [[matriz_a[i][j] - matriz_b[i][j] for j in range(len(matriz_a[0]))] for i in range(len(matriz_a))]


def multiplicar_matriz_escalar(matriz, escalar):
    """Multiplica una matriz por un escalar.
       Recibe una matriz A y un número; devuelve la matriz cA.
       """
    validar_matriz(matriz)
    return [[escalar * valor for valor in fila] for fila in matriz]


def multiplicar_matrices(matriz_a, matriz_b):
    """Calcula el producto matricial AB mediante productos fila por columna.
        Recibe A y B compatibles y devuelve una matriz de dimensión filas(A) × columnas(B).
        """
    validar_matriz(matriz_a)
    validar_matriz(matriz_b)
    filas_a, columnas_a = len(matriz_a), len(matriz_a[0])
    filas_b, columnas_b = len(matriz_b), len(matriz_b[0])

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
                suma += matriz_a[i][k] * matriz_b[k][j]
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado


def trasponer_matriz(matriz):
    """Calcula la transpuesta de una matriz.
       Recibe una matriz A de dimensión m × n y devuelve Aᵀ de dimensión n × m.
       """
    validar_matriz(matriz)
    filas, columnas = len(matriz), len(matriz[0])
    return [[matriz[i][j] for i in range(filas)] for j in range(columnas)]


def validar_cuadrada(matriz):
    """Comprueba que A sea cuadrada; requisito para el determinante y la inversa."""
    validar_matriz(matriz)
    if len(matriz) != len(matriz[0]):
        raise ValueError("La matriz debe ser cuadrada (n×n).")


def menor(matriz, i, j):
    """Devuelve la submatriz M_ij: A sin la fila i ni la columna j."""
    return [
        [matriz[f][c] for c in range(len(matriz[0])) if c != j]
        for f in range(len(matriz)) if f != i
    ]


def determinante(matriz):
    """Calcula det(A) por eliminación por filas con fracciones exactas."""
    if not matriz:
        return Fraction(1)  # Convención: el menor de una matriz 1×1 es vacío.
    return determinante_reduccion(matriz)["determinante"]


def determinante_reduccion(matriz):
    """Calcula det(A) triangularizando una copia de A con operaciones de fila y guarda cada paso.
    Recibe una matriz cuadrada; devuelve un diccionario con determinante, signo, triangular, diagonal y pasos.
    """
    validar_cuadrada(matriz)
    matriz_trabajo = [[Fraction(valor) for valor in fila] for fila in matriz]
    orden = len(matriz_trabajo)
    signo = 1
    pasos = [{
        "titulo": "Matriz inicial",
        "operacion": "Se busca llevar A a forma triangular superior.",
        "nota": None,
        "matriz": [fila[:] for fila in matriz_trabajo],
    }]

    for col in range(orden):
        # Sin intercambio no hay pivote nulo: el primer valor no nulo de la columna sirve de pivote.
        fila_pivote = next((fila for fila in range(col, orden) if matriz_trabajo[fila][col] != 0), None)
        if fila_pivote is None:
            pasos.append({
                "titulo": f"Columna {col + 1} sin pivote",
                "operacion": f"Desde la fila {col + 1} hacia abajo, la columna {col + 1} solo tiene ceros.",
                "nota": "La matriz es singular: su determinante es 0.",
                "matriz": [fila[:] for fila in matriz_trabajo],
            })
            return {"determinante": Fraction(0), "signo": signo, "triangular": matriz_trabajo,
                    "diagonal": None, "pasos": pasos}

        if fila_pivote != col:
            matriz_trabajo[col], matriz_trabajo[fila_pivote] = matriz_trabajo[fila_pivote], matriz_trabajo[col]
            signo = -signo
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{col + 1} ↔ R{fila_pivote + 1}",
                "nota": f"Intercambiar filas cambia el signo del determinante (signo acumulado: {signo}).",
                "matriz": [fila[:] for fila in matriz_trabajo],
            })

        # Se anula cada entrada bajo el pivote: Rf ← Rf − factor·Rcol (no cambia det).
        for fila in range(col + 1, orden):
            factor = matriz_trabajo[fila][col] / matriz_trabajo[col][col]
            if factor == 0:
                continue
            matriz_trabajo[fila] = [x - factor * y for x, y in zip(matriz_trabajo[fila], matriz_trabajo[col])]
            pasos.append({
                "titulo": "Eliminación debajo del pivote",
                "operacion": formatear_operacion_eliminacion(fila + 1, col + 1, factor),
                "nota": "Sumar a una fila un múltiplo de otra no cambia el determinante.",
                "matriz": [fila[:] for fila in matriz_trabajo],
            })

    # det = (±1 por los intercambios) · producto de la diagonal triangular.
    diagonal = [matriz_trabajo[k][k] for k in range(orden)]
    resultado = Fraction(signo)
    for valor in diagonal:
        resultado *= valor
    return {"determinante": resultado, "signo": signo, "triangular": matriz_trabajo,
            "diagonal": diagonal, "pasos": pasos}


def _fila_con_mas_ceros(matriz):
    """Índice de la fila con más ceros; desarrollar por ella ahorra cálculos."""
    return max(range(len(matriz)), key=lambda f: sum(1 for x in matriz[f] if x == 0))


def determinante_cofactores(matriz):
    """Calcula det(A) por cofactores (Laplace) recursivamente, desarrollando por la fila con más ceros.
    Recibe una matriz cuadrada y devuelve un Fraction.
    """
    validar_cuadrada(matriz)
    orden = len(matriz)
    # Casos base de la recursión: 1×1 y 2×2.
    if orden == 1:
        return Fraction(matriz[0][0])
    if orden == 2:
        return Fraction(matriz[0][0]) * matriz[1][1] - Fraction(matriz[0][1]) * matriz[1][0]
    fila_desarrollo = _fila_con_mas_ceros(matriz)
    total = Fraction(0)
    for j in range(orden):
        if matriz[fila_desarrollo][j] == 0:
            continue
        # Signo del cofactor: tablero de ajedrez (−1)^(fila+columna).
        signo = 1 if (fila_desarrollo + j) % 2 == 0 else -1
        total += matriz[fila_desarrollo][j] * signo * determinante_cofactores(menor(matriz, fila_desarrollo, j))
    return total


def desarrollo_cofactores(matriz):
    """Devuelve el primer nivel del desarrollo por cofactores (entrada, signo, menor y producto de cada término).
    Recibe una matriz cuadrada; devuelve un diccionario con fila, terminos y determinante.
    """
    validar_cuadrada(matriz)
    orden = len(matriz)
    fila_desarrollo = _fila_con_mas_ceros(matriz) if orden > 1 else 0
    terminos = []
    for j in range(orden):
        signo = 1 if (fila_desarrollo + j) % 2 == 0 else -1
        sub = menor(matriz, fila_desarrollo, j)
        # Si la entrada es 0, el término vale 0 y no hace falta calcular su menor.
        det_menor = None if matriz[fila_desarrollo][j] == 0 else (determinante_cofactores(sub) if sub else Fraction(1))
        producto = Fraction(0) if det_menor is None else Fraction(matriz[fila_desarrollo][j]) * signo * det_menor
        terminos.append({
            "columna": j, "valor": matriz[fila_desarrollo][j], "signo": signo,
            "menor": sub, "det_menor": det_menor, "producto": producto,
        })
    return {
        "fila": fila_desarrollo,
        "terminos": terminos,
        "determinante": sum((t["producto"] for t in terminos), Fraction(0)),
    }


def determinante_sarrus(matriz):
    """Calcula det(A) de una matriz 3×3 con la regla de Sarrus.
    Devuelve las entradas y el producto de cada diagonal, sus sumas y el determinante.
    """
    validar_cuadrada(matriz)
    if len(matriz) != 3:
        raise ValueError("La regla de Sarrus solo aplica a matrices 3×3.")
    matriz = [[Fraction(valor) for valor in fila] for fila in matriz]
    principales, secundarias = [], []
    for k in range(3):
        # El "% 3" equivale a repetir las dos primeras columnas, sin armar una matriz 3×5.
        # Diagonal descendente que empieza en la columna k y ascendente que empieza en la k.
        principales.append([matriz[i][(k + i) % 3] for i in range(3)])
        secundarias.append([matriz[2 - i][(k + i) % 3] for i in range(3)])

    def producto(entradas):
        """Multiplica las tres entradas de una diagonal."""
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


def resolver_cramer(matriz_a, vector_b):
    """Resuelve Ax = b con la regla de Cramer: xᵢ = det(Aᵢ) / det(A), con A cuadrada y det(A) ≠ 0.
    Recibe A y b; devuelve det(A), cada Aᵢ con su determinante y la solución x.
    """
    validar_cuadrada(matriz_a)
    orden = len(matriz_a)
    if len(vector_b) != orden:
        raise ValueError("El vector b debe tener tantas entradas como filas tiene A.")
    determinante_a = determinante_cofactores(matriz_a)
    if determinante_a == 0:
        # Sin det(A) ≠ 0 no hay solución única y no se puede dividir.
        raise ValueError(
            "det(A) = 0: la regla de Cramer no aplica (el sistema no tiene solución única)."
        )
    pasos = []
    for i in range(orden):
        # Aᵢ: copia de A con la columna i reemplazada por b.
        matriz_ai = [fila[:i] + [vector_b[indice_fila]] + fila[i + 1:] for indice_fila, fila in enumerate(matriz_a)]
        determinante_ai = determinante_cofactores(matriz_ai)
        pasos.append({"columna": i, "matriz": matriz_ai, "determinante": determinante_ai, "x": determinante_ai / determinante_a})
    return {"determinante": determinante_a, "pasos": pasos, "solucion": [p["x"] for p in pasos]}


def matriz_cofactores(matriz):
    """Calcula la matriz de cofactores: C_ij = (-1)^(i+j) · det(M_ij)."""
    validar_cuadrada(matriz)
    orden = len(matriz)
    # Un cofactor por entrada: signo de ajedrez por el determinante de su menor.
    return [
        [(1 if (i + j) % 2 == 0 else -1) * determinante(menor(matriz, i, j)) for j in range(orden)]
        for i in range(orden)
    ]


def matriz_adjunta(matriz):
    """La adjunta es la traspuesta de la matriz de cofactores: adj(A) = Cᵀ."""
    return trasponer_matriz(matriz_cofactores(matriz))


def inversa_por_adjunta(matriz):
    """Calcula A⁻¹ = (1/det A) · adj(A) y devuelve también los pasos intermedios."""
    validar_cuadrada(matriz)
    det = determinante(matriz)
    if det == 0:
        raise ValueError("La matriz es singular (det = 0): no tiene inversa.")
    cofactores = matriz_cofactores(matriz)
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


def inversa_gauss_jordan(matriz):
    """Calcula A⁻¹ reduciendo [A | I] hasta [I | A⁻¹] con operaciones elementales de fila.
    Recibe A cuadrada y no singular; devuelve la inversa, la matriz aumentada final y los pasos.
    """
    validar_cuadrada(matriz)

    orden = len(matriz)
    matriz_aumentada = [
        [Fraction(valor) for valor in matriz[i]] + [Fraction(1 if i == j else 0) for j in range(orden)]
        for i in range(orden)
    ]
    pasos = [{
        "titulo": "Matriz aumentada [A | I]",
        "operacion": "Se escribe A a la izquierda y la identidad a la derecha.",
        "matriz": [fila[:] for fila in matriz_aumentada],
    }]

    for col in range(orden):
        # Pivote: el mayor valor absoluto de la columna (de la diagonal hacia abajo).
        fila_mejor = col
        for fila in range(col + 1, orden):
            if abs(matriz_aumentada[fila][col]) > abs(matriz_aumentada[fila_mejor][col]):
                fila_mejor = fila

        # Sin pivote en la columna, A es singular y no hay inversa.
        if matriz_aumentada[fila_mejor][col] == 0:
            raise ValueError(
                f"La matriz es singular (det = 0): no tiene inversa "
                f"(la columna {col + 1} no tiene pivote)."
            )

        if fila_mejor != col:
            matriz_aumentada[fila_mejor], matriz_aumentada[col] = matriz_aumentada[col], matriz_aumentada[fila_mejor]
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{col + 1} ↔ R{fila_mejor + 1}",
                "matriz": [fila[:] for fila in matriz_aumentada],
            })

        # Se normaliza la fila para que el pivote valga 1 (también afecta la parte de I).
        pivote = matriz_aumentada[col][col]
        if pivote != 1:
            matriz_aumentada[col] = [valor / pivote for valor in matriz_aumentada[col]]
            pasos.append({
                "titulo": "División de la fila pivote",
                "operacion": f"R{col + 1} ÷ ({formatear_fraccion(pivote)}) → R{col + 1}",
                "matriz": [fila[:] for fila in matriz_aumentada],
            })

        # Se hacen ceros arriba y abajo del pivote en toda la fila de 2n columnas.
        for fila in range(orden):
            if fila == col:
                continue
            factor = matriz_aumentada[fila][col]
            if factor == 0:
                continue
            matriz_aumentada[fila] = [x - factor * y for x, y in zip(matriz_aumentada[fila], matriz_aumentada[col])]
            pasos.append({
                "titulo": "Eliminación de la columna pivote",
                "operacion": formatear_operacion_eliminacion(fila + 1, col + 1, factor),
                "matriz": [fila[:] for fila in matriz_aumentada],
            })

    pasos.append({
        "titulo": "Resultado [I | A⁻¹]",
        "operacion": "A la izquierda quedó la identidad; a la derecha está A⁻¹.",
        "matriz": [fila[:] for fila in matriz_aumentada],
    })
    return {
        "inversa": [fila[orden:] for fila in matriz_aumentada],
        "aumentada_final": matriz_aumentada,
        "pasos": pasos,
    }


def matriz_identidad(n):
    """Devuelve la matriz identidad Iₙ de dimensión n × n."""
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def matriz_cero(filas, columnas):
    """Devuelve la matriz nula de dimensión filas × columnas."""
    return [[Fraction(0) for _ in range(columnas)] for _ in range(filas)]


def inversa(matriz):
    """Atajo: A⁻¹ por la matriz adjunta; ValueError si A no es cuadrada o det(A) = 0."""
    return inversa_por_adjunta(matriz)["inversa"]


def comprobar_traspuesta_del_producto(a, b):
    """Verifica (A·B)ᵀ = Bᵀ·Aᵀ y muestra Aᵀ·Bᵀ como contraejemplo de la igualdad falsa.
    Devuelve los lados de cada igualdad y si se cumplen; el contraejemplo es None si sus dimensiones no encajan.
    """
    izquierda = trasponer_matriz(multiplicar_matrices(a, b))
    correcta = multiplicar_matrices(trasponer_matriz(b), trasponer_matriz(a))
    try:
        incorrecta = multiplicar_matrices(trasponer_matriz(a), trasponer_matriz(b))
    except ValueError:
        incorrecta = None
    return {
        "izquierda": izquierda,
        "correcta": correcta,
        "se_cumple": izquierda == correcta,
        "incorrecta": incorrecta,
        "incorrecta_se_cumple": incorrecta is not None and izquierda == incorrecta,
    }


"""Módulo para realizar eliminación Gaussiana y Gauss-Jordan en matrices.
Implementa contenidos de Álgebra Lineal relacionados con sistemas de ecuaciones.
Utiliza Fraction para conservar los resultados racionales de forma exacta.
Elaborado por: "Patricia del Carmen Oquist Talavera y Rafael Antonio Arauz Navarro"""


from fractions import Fraction

from utilidades.fracciones import formatear_fraccion
from utilidades.formato import formatear_operacion_eliminacion


ZERO = Fraction(0, 1)


def es_cero(valor):
    """Determina si un valor es exactamente cero y devuelve True o False."""
    return valor == ZERO


def copiar_matriz(matriz):
    """Recibe una matriz y devuelve una copia independiente de sus filas."""
    return [fila[:] for fila in matriz]


def intercambiar_filas(matriz, fila_a, fila_b):
    """Recibe una matriz y dos índices de fila; intercambia ambas filas."""
    matriz[fila_a], matriz[fila_b] = matriz[fila_b], matriz[fila_a]


def limpiar_ceros(matriz, numero_variables):
    """Normaliza los valores cero de una matriz aumentada."""
    for i in range(len(matriz)):
        for j in range(numero_variables + 1):
            if es_cero(matriz[i][j]):
                matriz[i][j] = ZERO


def eliminacion_gaussiana(matriz, numero_variables):
    """Reduce la matriz aumentada a forma escalonada y guarda cada paso."""
    matriz_trabajo = [[Fraction(valor) for valor in fila] for fila in matriz]
    filas = len(matriz_trabajo)
    fila_pivote = 0
    pivotes = []
    pasos = [
        {
            "titulo": "Matriz inicial",
            "operacion": "Inicio del proceso de eliminación por filas.",
            "matriz": copiar_matriz(matriz_trabajo),
        }
    ]

    for columna in range(numero_variables):
        if fila_pivote >= filas:
            break

        # Se busca el mayor pivote disponible para evitar divisiones innecesarias
        # y reducir problemas numéricos durante la eliminación.
        fila_mejor = fila_pivote
        for fila in range(fila_pivote + 1, filas):
            if abs(matriz_trabajo[fila][columna]) > abs(matriz_trabajo[fila_mejor][columna]):
                fila_mejor = fila

        if es_cero(matriz_trabajo[fila_mejor][columna]):
            pasos.append({
                "titulo": f"Columna {columna + 1} sin pivote",
                "operacion": (
                    f"No se encontró pivote distinto de cero en la columna {columna + 1}; "
                    "se continúa."
                ),
                "matriz": copiar_matriz(matriz_trabajo),
            })
            continue

        if fila_mejor != fila_pivote:
            intercambiar_filas(matriz_trabajo, fila_mejor, fila_pivote)
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{fila_pivote + 1} ↔ R{fila_mejor + 1}",
                "matriz": copiar_matriz(matriz_trabajo),
            })

        pivote = matriz_trabajo[fila_pivote][columna]
        # Si el pivote ya vale 1, dividir entre 1 sería un paso innecesario.
        if pivote != 1:
            for j in range(columna, numero_variables + 1):
                matriz_trabajo[fila_pivote][j] /= pivote

            limpiar_ceros(matriz_trabajo, numero_variables)
            pasos.append({
                "titulo": "Normalización del pivote",
                "operacion": f"R{fila_pivote + 1} ← R{fila_pivote + 1} / ({formatear_fraccion(pivote)})",
                "matriz": copiar_matriz(matriz_trabajo),
            })

        for fila in range(fila_pivote + 1, filas):
            factor = matriz_trabajo[fila][columna]
            if es_cero(factor):
                continue

            for j in range(columna, numero_variables + 1):
                matriz_trabajo[fila][j] -= factor * matriz_trabajo[fila_pivote][j]

            limpiar_ceros(matriz_trabajo, numero_variables)
            pasos.append({
                "titulo": "Eliminación debajo del pivote",
                "operacion": formatear_operacion_eliminacion(
                    fila + 1,
                    fila_pivote + 1,
                    factor,
                ),
                "matriz": copiar_matriz(matriz_trabajo),
            })

        pivotes.append((fila_pivote, columna))
        fila_pivote += 1

    limpiar_ceros(matriz_trabajo, numero_variables)

    return (
        matriz_trabajo,
        pivotes,
        detectar_inconsistencia(matriz_trabajo, numero_variables),
        pasos,
    )


def formatear_operacion_division(fila, divisor):
    """Formato de división de fila como se escribe en papel."""
    return f"R{fila} ÷ ({formatear_fraccion(divisor)}) → R{fila}"


def gauss_jordan(matriz, numero_variables):
    """Reduce una matriz aumentada a su forma escalonada reducida.
       Recibe la matriz y el número de variables; devuelve la matriz
       reducida, las posiciones pivote, la inconsistencia y los pasos.
       """
    matriz_trabajo = [[Fraction(valor) for valor in fila] for fila in matriz]
    filas = len(matriz_trabajo)
    fila_pivote = 0
    pivotes = []
    pasos = [{
        "titulo": "Matriz inicial",
        "operacion": "Inicio del proceso de Gauss-Jordan.",
        "matriz": copiar_matriz(matriz_trabajo),
    }]

    for columna in range(numero_variables):
        if fila_pivote >= filas:
            break

        fila_mejor = fila_pivote
        for fila in range(fila_pivote + 1, filas):
            if abs(matriz_trabajo[fila][columna]) > abs(matriz_trabajo[fila_mejor][columna]):
                fila_mejor = fila

        if es_cero(matriz_trabajo[fila_mejor][columna]):
            pasos.append({
                "titulo": f"Columna {columna + 1} sin pivote",
                "operacion": f"No hay pivote distinto de cero en la columna {columna + 1}; se continúa.",
                "matriz": copiar_matriz(matriz_trabajo),
            })
            continue

        if fila_mejor != fila_pivote:
            intercambiar_filas(matriz_trabajo, fila_mejor, fila_pivote)
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{fila_pivote + 1} ↔ R{fila_mejor + 1}",
                "matriz": copiar_matriz(matriz_trabajo),
            })

        pivote = matriz_trabajo[fila_pivote][columna]
        if pivote != 1:
            for j in range(columna, numero_variables + 1):
                matriz_trabajo[fila_pivote][j] /= pivote
            limpiar_ceros(matriz_trabajo, numero_variables)
            pasos.append({
                "titulo": "División de la fila pivote",
                "operacion": formatear_operacion_division(fila_pivote + 1, pivote),
                "matriz": copiar_matriz(matriz_trabajo),
            })

        # Gauss-Jordan elimina tanto debajo como encima del pivote.
        for fila in range(filas):
            if fila == fila_pivote:
                continue
            factor = matriz_trabajo[fila][columna]
            if es_cero(factor):
                continue
            for j in range(columna, numero_variables + 1):
                matriz_trabajo[fila][j] -= factor * matriz_trabajo[fila_pivote][j]
            limpiar_ceros(matriz_trabajo, numero_variables)
            pasos.append({
                "titulo": "Eliminación de la columna pivote",
                "operacion": formatear_operacion_eliminacion(fila + 1, fila_pivote + 1, factor),
                "matriz": copiar_matriz(matriz_trabajo),
            })

        pivotes.append((fila_pivote, columna))
        fila_pivote += 1

    limpiar_ceros(matriz_trabajo, numero_variables)
    inconsistente = detectar_inconsistencia(matriz_trabajo, numero_variables)
    return matriz_trabajo, pivotes, inconsistente, pasos


def inversa_gauss_jordan(a):
    """Calcula A⁻¹ reduciendo la matriz aumentada [A | I] hasta [I | A⁻¹].

    Aplica las mismas operaciones elementales que gauss_jordan, pero sobre
    las 2n columnas de [A | I]. Si alguna columna de A no tiene pivote, la
    matriz es singular y no tiene inversa. Devuelve la inversa y los pasos.
    """
    if not a or not a[0] or any(len(fila) != len(a) for fila in a):
        raise ValueError("La matriz debe ser cuadrada (n×n) para calcular su inversa.")

    n = len(a)
    # Matriz aumentada [A | I]: cada fila de A seguida de la fila de la identidad.
    m = [
        [Fraction(valor) for valor in a[i]] + [Fraction(1 if i == j else 0) for j in range(n)]
        for i in range(n)
    ]
    pasos = [{
        "titulo": "Matriz aumentada [A | I]",
        "operacion": "Se escribe A a la izquierda y la identidad a la derecha.",
        "matriz": copiar_matriz(m),
    }]

    for col in range(n):
        # Pivote: el mayor valor absoluto de la columna (de la diagonal hacia abajo).
        fila_mejor = col
        for fila in range(col + 1, n):
            if abs(m[fila][col]) > abs(m[fila_mejor][col]):
                fila_mejor = fila

        # Sin pivote en la columna, A es singular y no hay inversa.
        if es_cero(m[fila_mejor][col]):
            raise ValueError(
                f"La matriz es singular: la columna {col + 1} no tiene pivote, "
                "por lo que no tiene inversa."
            )

        if fila_mejor != col:
            intercambiar_filas(m, fila_mejor, col)
            pasos.append({
                "titulo": "Intercambio de filas",
                "operacion": f"R{col + 1} ↔ R{fila_mejor + 1}",
                "matriz": copiar_matriz(m),
            })

        # Se normaliza la fila para que el pivote valga 1 (también afecta la parte de I).
        pivote = m[col][col]
        if pivote != 1:
            m[col] = [valor / pivote for valor in m[col]]
            pasos.append({
                "titulo": "División de la fila pivote",
                "operacion": formatear_operacion_division(col + 1, pivote),
                "matriz": copiar_matriz(m),
            })

        # Se hacen ceros arriba y abajo del pivote en toda la fila de 2n columnas.
        for fila in range(n):
            if fila == col:
                continue
            factor = m[fila][col]
            if es_cero(factor):
                continue
            m[fila] = [x - factor * y for x, y in zip(m[fila], m[col])]
            pasos.append({
                "titulo": "Eliminación de la columna pivote",
                "operacion": formatear_operacion_eliminacion(fila + 1, col + 1, factor),
                "matriz": copiar_matriz(m),
            })

    pasos.append({
        "titulo": "Resultado [I | A⁻¹]",
        "operacion": "A la izquierda quedó la identidad; a la derecha está A⁻¹.",
        "matriz": copiar_matriz(m),
    })
    # La inversa son las últimas n columnas de [I | A⁻¹].
    return {
        "inversa": [fila[n:] for fila in m],
        "aumentada_final": m,
        "pasos": pasos,
    }


def detectar_inconsistencia(matriz, numero_variables):
    """Detecta si un sistema tiene una fila de coeficientes cero
       con término independiente distinto de cero. Recibe la matriz
       aumentada y el número de variables; devuelve True o False.
       """
    for fila in matriz:
        coeficientes_cero = all(
            es_cero(fila[j]) for j in range(numero_variables)
        )
        if coeficientes_cero and not es_cero(fila[numero_variables]):
            return True
    return False


def es_homogeneo(matriz, numero_variables):
    """Determina si todos los términos independientes del sistema son cero."""
    return all(es_cero(fila[numero_variables]) for fila in matriz)


def obtener_clasificacion(matriz_escalonada, numero_variables, pivotes, inconsistente):
    """Clasifica el sistema según sus pivotes y filas inconsistentes."""
    if inconsistente:
        return "inconsistente", []

    if len(pivotes) == numero_variables:
        return "unica", []

    columnas_pivote = {columna for _, columna in pivotes}
    variables_libres = [
        columna
        for columna in range(numero_variables)
        if columna not in columnas_pivote
    ]
    return "infinita", variables_libres


def resolver_solucion_unica(matriz_escalonada, numero_variables, pivotes):
    """Resuelve por sustitución regresiva usando aritmética racional exacta."""
    solucion = [ZERO] * numero_variables

    for fila_pivote, columna_pivote in reversed(pivotes):
        valor = matriz_escalonada[fila_pivote][numero_variables]

        for columna in range(columna_pivote + 1, numero_variables):
            valor -= matriz_escalonada[fila_pivote][columna] * solucion[columna]

        coeficiente = matriz_escalonada[fila_pivote][columna_pivote]
        solucion[columna_pivote] = valor / coeficiente

    return solucion


def verificar_solucion(matriz_original, solucion):
    """Comprueba la solución sustituyéndola en el sistema original."""
    for fila in matriz_original:
        suma = ZERO
        for i, valor in enumerate(solucion):
            suma += fila[i] * valor
        if suma != fila[-1]:
            return False
    return True
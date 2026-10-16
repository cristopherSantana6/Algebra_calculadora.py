"""Módulo para construir y evaluar expresiones matriciales armadas con clics.
Una expresión es una lista de tokens («A», «+», «T», «(» ...) que la interfaz va agregando;
aquí se decide qué token puede venir después, se convierte la lista en un árbol y se evalúa
reutilizando las operaciones de modulos/modulo_matrices.py. No usa NumPy ni funciones de álgebra lineal de math.
"""

from modulos.modulo_matrices import (  # noqa: F401
    comprobar_traspuesta_del_producto,
    inversa_por_adjunta,
    multiplicar_matrices,
    restar_matrices,
    sumar_matrices,
    trasponer_matriz,
)

CAPACIDAD_PILA = 7
BASES = ("A", "B")
GUARDADOS = tuple(f"R{i}" for i in range(1, CAPACIDAD_PILA + 1))
OPERANDOS = BASES + GUARDADOS
BINARIOS = ("+", "-", "*")
POSTFIJOS = ("T", "INV")
TODOS_LOS_TOKENS = OPERANDOS + BINARIOS + POSTFIJOS + ("(", ")")

# Cómo se escribe cada token en la tira de la expresión.
_TEXTO = {"+": " + ", "-": " − ", "*": " · ", "T": "ᵀ", "INV": "⁻¹"}


def abiertos(tokens):
    """Cuenta los paréntesis «(» que todavía no se han cerrado."""
    return sum(1 for t in tokens if t == "(") - sum(1 for t in tokens if t == ")")


def siguientes_permitidos(tokens):
    """Devuelve el conjunto de tokens que se pueden agregar después de `tokens`.

    Tras un operando, «)» o un postfijo solo caben un operador, un postfijo o «)»;
    al inicio, tras un operador binario o tras «(» solo caben un operando o «(».
    """
    if not tokens or tokens[-1] in BINARIOS or tokens[-1] == "(":
        return set(OPERANDOS) | {"("}
    permitidos = set(BINARIOS) | set(POSTFIJOS)
    if abiertos(tokens) > 0:
        permitidos.add(")")
    return permitidos


def esta_completa(tokens):
    """Una expresión se puede evaluar si termina en operando, postfijo o «)» y está balanceada."""
    return bool(tokens) and tokens[-1] not in BINARIOS and tokens[-1] != "(" and abiertos(tokens) == 0


def texto_expresion(tokens):
    """Convierte los tokens en el texto de solo lectura, por ejemplo «(A · Bᵀ) − (A⁻¹ · B)»."""
    return "".join(_TEXTO.get(t, t) for t in tokens)


def nombres_usados(tokens):
    """Devuelve los operandos distintos que aparecen en la expresión, en orden."""
    vistos = []
    for t in tokens:
        if t in OPERANDOS and t not in vistos:
            vistos.append(t)
    return vistos


def parsear(tokens):
    """Convierte los tokens en un árbol de tuplas por descenso recursivo.

    Precedencia: postfijos (ᵀ, ⁻¹) > producto > suma y resta. Nodos:
    ("op", nombre), ("post", token, hijo) y ("bin", token, izquierda, derecha).
    """
    if not esta_completa(tokens):
        raise ValueError("La expresión está incompleta.")
    posicion = 0

    def actual():
        return tokens[posicion] if posicion < len(tokens) else None

    def sumas():
        nonlocal posicion
        nodo = productos()
        while actual() in ("+", "-"):
            operador = tokens[posicion]
            posicion += 1
            nodo = ("bin", operador, nodo, productos())
        return nodo

    def productos():
        nonlocal posicion
        nodo = postfijos()
        while actual() == "*":
            posicion += 1
            nodo = ("bin", "*", nodo, postfijos())
        return nodo

    def postfijos():
        nonlocal posicion
        nodo = base()
        while actual() in POSTFIJOS:
            nodo = ("post", tokens[posicion], nodo)
            posicion += 1
        return nodo

    def base():
        nonlocal posicion
        token = actual()
        posicion += 1
        if token == "(":
            nodo = sumas()
            posicion += 1  # consume «)»
            return nodo
        return ("op", token)

    return sumas()


def evaluar(arbol, contexto):
    """Evalúa el árbol con `contexto` (nombre → matriz) y devuelve una matriz nueva.

    Genera ValueError cuando una operación no es posible (dimensiones o matriz singular)
    o cuando un operando no tiene valor, por ejemplo un R3 vacío.
    """
    tipo = arbol[0]
    if tipo == "op":
        if arbol[1] not in contexto:
            raise ValueError(f"{arbol[1]} no tiene ningún resultado guardado.")
        return [fila[:] for fila in contexto[arbol[1]]]
    if tipo == "post":
        interior = evaluar(arbol[2], contexto)
        if arbol[1] == "T":
            return trasponer_matriz(interior)
        return inversa_por_adjunta(interior)["inversa"]
    izquierda, derecha = evaluar(arbol[2], contexto), evaluar(arbol[3], contexto)
    if arbol[1] == "+":
        return sumar_matrices(izquierda, derecha)
    if arbol[1] == "-":
        return restar_matrices(izquierda, derecha)
    return multiplicar_matrices(izquierda, derecha)


def evaluar_tokens(tokens, contexto):
    """Atajo: parsea y evalúa una lista de tokens. Devuelve la matriz resultante."""
    return evaluar(parsear(tokens), contexto)

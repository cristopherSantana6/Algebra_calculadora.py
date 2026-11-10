
"""
Implementa el algoritmo de Bisección para aproximar raíces de funciones.
Registra las iteraciones, calcula errores y verifica la continuidad.
Utiliza SymPy para interpretar funciones y SciPy como referencia externa.
Elaborado por: Patricia del Carmen Oquist Talavera y Rafael Antonio Arauz Navarro
"""

import ast
import math
import operator

import sympy as sp
from sympy.calculus.util import continuous_domain


# Variable simbólica utilizada para representar las funciones f(x).
X = sp.Symbol("x", real=True)

# Funciones matemáticas que el usuario puede utilizar.
# Se restringen las funciones permitidas para interpretar las expresiones.
FUNCIONES = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "exp": sp.exp,
    "log": sp.log,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
}

# Símbolos y constantes matemáticas reconocidos por el programa.
CONSTANTES = {
    "x": X,
    "pi": sp.pi,
    "e": sp.E,
}

# Operaciones aritméticas permitidas al interpretar una expresión.
OPERACIONES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def convertir_funcion(texto):
    """Convierte el texto ingresado en una expresión de SymPy.
    Permite únicamente funciones, constantes y operaciones autorizadas.
    Valida la sintaxis y evita expresiones no permitidas.
    """
    # Comprobar que el usuario haya ingresado una función válida.
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Debe ingresar una función f(x).")

    # Limitar la longitud para evitar expresiones demasiado extensas.
    if len(texto) > 200:
        raise ValueError("La función es demasiado larga.")

    # Analizar la estructura de la expresión mediante AST.
    try:
        arbol = ast.parse(texto, mode="eval")
    except SyntaxError:
        raise ValueError("La función está mal escrita.") from None

    # Evitar expresiones con una cantidad excesiva de elementos.
    if sum(1 for _ in ast.walk(arbol)) > 100:
        raise ValueError("La función es demasiado compleja.")

    def interpretar(nodo):
        """Interpreta cada elemento del árbol de expresión.
        Acepta números, símbolos, operaciones y funciones autorizadas.
        Rechaza cualquier estructura que no esté permitida.
        """
        # Procesar el contenido principal de la expresión.
        if isinstance(nodo, ast.Expression):
            return interpretar(nodo.body)

        # Aceptar únicamente constantes numéricas.
        if isinstance(nodo, ast.Constant):
            if type(nodo.value) in (int, float):
                return sp.sympify(nodo.value)
            raise ValueError("Constante no permitida.")

        # Identificar variables y constantes conocidas.
        if isinstance(nodo, ast.Name):
            if nodo.id in CONSTANTES:
                return CONSTANTES[nodo.id]
            raise ValueError(f"Símbolo no permitido: {nodo.id}")

        # Interpretar los signos positivo y negativo.
        if isinstance(nodo, ast.UnaryOp):
            valor = interpretar(nodo.operand)
            if isinstance(nodo.op, ast.USub):
                return -valor
            if isinstance(nodo.op, ast.UAdd):
                return valor
            raise ValueError("Operación no permitida.")

        # Resolver las operaciones entre dos expresiones.
        if isinstance(nodo, ast.BinOp):
            operacion = OPERACIONES.get(type(nodo.op))
            if operacion is None:
                raise ValueError("Operación matemática no permitida.")
            izquierda = interpretar(nodo.left)
            derecha = interpretar(nodo.right)
            return operacion(izquierda, derecha)

        # Validar que la función matemática esté autorizada.
        if isinstance(nodo, ast.Call):
            if not isinstance(nodo.func, ast.Name):
                raise ValueError("Llamada no permitida.")

            funcion = FUNCIONES.get(nodo.func.id)
            if funcion is None or len(nodo.args) != 1 or nodo.keywords:
                raise ValueError("Función matemática no permitida.")

            return funcion(interpretar(nodo.args[0]))

        raise ValueError("La expresión contiene elementos no permitidos.")

    # Convertir la expresión y controlar errores matemáticos.
    try:
        return interpretar(arbol)
    except (ZeroDivisionError, OverflowError, TypeError) as error:
        raise ValueError(f"Función inválida: {error}") from error


def evaluar_funcion(expresion, valor):
    """Evalúa la expresión matemática en un valor de x.
    Comprueba que el resultado sea real y finito.
    Genera un error cuando la función no puede evaluarse.
    """
    # Sustituir x por el valor recibido y obtener el resultado numérico.
    try:
        resultado = complex(sp.N(expresion.subs(X, valor), 16))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        raise ValueError(
            f"La función no está definida en x = {valor}."
        ) from None

    # Evitar resultados infinitos o no definidos.
    if not math.isfinite(resultado.real):
        raise ValueError("Se obtuvo un resultado no finito.")

    # Verificar que el resultado pertenezca a los números reales.
    if not math.isfinite(resultado.imag) or abs(resultado.imag) > 1e-12:
        raise ValueError("La función produce un resultado no real.")

    return resultado.real


def verificar_continuidad(expresion, a, b):
    """Verifica la continuidad de la función en el intervalo [a, b].
    Utiliza SymPy para comprobar su dominio real.
    Rechaza intervalos donde no se garantiza la continuidad.
    """
    # Obtener el dominio continuo de la función.
    try:
        dominio = continuous_domain(expresion, X, sp.S.Reals)
        intervalo = sp.Interval(a, b)
        comprobacion = intervalo.is_subset(dominio)
    except (TypeError, ValueError, NotImplementedError):
        comprobacion = None

    # El método requiere continuidad en todo el intervalo.
    if comprobacion is not True:
        raise ValueError(
            "No se pudo garantizar la continuidad en [a, b]. "
            "Revise discontinuidades, asíntotas o restricciones de dominio."
        )


def metodo_biseccion(funcion, a, b, tolerancia, max_iteraciones):
    """Aproxima una raíz mediante el Método de Bisección.
    Divide el intervalo y conserva la mitad con cambio de signo.
    Registra iteraciones, errores y comparación con SciPy.
    """
    # Convertir los parámetros ingresados a sus tipos numéricos.
    try:
        a = float(a)
        b = float(b)
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Los límites y parámetros deben ser numéricos.") from None

    if not all(math.isfinite(v) for v in (a, b, tolerancia)):
        raise ValueError("Los valores deben ser finitos.")

    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el superior.")

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    if max_iteraciones < 1:
        raise ValueError("Debe permitir al menos una iteración.")

    # Interpretar la función y comprobar su continuidad.
    expresion = convertir_funcion(funcion)
    verificar_continuidad(expresion, a, b)

    # Calcular los valores de la función en ambos extremos.
    fa = evaluar_funcion(expresion, a)
    fb = evaluar_funcion(expresion, b)

    # Calcular la cantidad teórica de iteraciones necesarias.
    # Fórmula: n = ceil(log2((b - a) / tolerancia)).
    ancho_inicial = b - a
    n_teorico = max(0, math.ceil(math.log2(ancho_inicial / tolerancia)))

    # Almacenar los datos que utilizará la interfaz para mostrar resultados.
    resultado = {
        "funcion": funcion,
        "intervalo_inicial": (a, b),
        "tolerancia": tolerancia,
        "iteraciones_teoricas": n_teorico,
        "iteraciones_realizadas": 0,
        "tabla": [],
        "raiz": None,
        "valor_funcion": None,
        "error": None,
        "estado": "",
        "comparacion_scipy": None,
        "diferencia_scipy": None,
    }

    # Comprobar si alguno de los extremos ya es una raíz exacta.
    if fa == 0 or fb == 0:
        raiz = a if fa == 0 else b
        resultado.update({
            "raiz": raiz,
            "valor_funcion": 0.0,
            "error": 0.0,
            "estado": "Raíz exacta encontrada en un extremo.",
        })
        return resultado

    # Verificar la condición inicial: f(a) y f(b) deben tener signos opuestos.
    if (fa < 0) == (fb < 0):
        raise ValueError(
            "No existe cambio de signo entre f(a) y f(b). "
            "Seleccione otro intervalo; esto no significa "
            "que la función no tenga raíces."
        )

    # Obtener una raíz de referencia con SciPy.
    # Esta librería no sustituye al algoritmo implementado.
    try:
        from scipy.optimize import bisect

        referencia = bisect(
            lambda valor: evaluar_funcion(expresion, valor),
            a, b, xtol=1e-12
        )
        resultado["comparacion_scipy"] = referencia
    except (ImportError, ValueError, RuntimeError, OverflowError):
        pass

    # Guardar el punto medio anterior para calcular los errores.
    xr_anterior = None

    # Repetir el proceso hasta alcanzar la tolerancia o el límite establecido.
    for k in range(1, max_iteraciones + 1):

        # Calcular el punto medio del intervalo.
        # Fórmula: xr = (a + b) / 2, expresada de forma equivalente.
        xr = a + (b - a) / 2

        # Calcular la cota del error: Eb = (b - a) / 2.
        eb = (b - a) / 2

        # Detener el proceso si la precisión de máquina impide avanzar.
        if xr == a or xr == b:
            resultado["estado"] = (
                "La precisión de máquina impide seguir reduciendo el intervalo."
            )
            break

        # Evaluar la función en el punto medio.
        fr = evaluar_funcion(expresion, xr)

        # Calcular el error aproximado entre dos puntos medios consecutivos.
        error_aproximado = (
            None if xr_anterior is None else abs(xr - xr_anterior)
        )

        # Calcular el error relativo cuando se encuentra definido.
        error_relativo = (
            None if xr_anterior is None or xr == 0
            else abs((xr - xr_anterior) / xr)
        )

        # Registrar los valores de la iteración antes de modificar el intervalo.
        resultado["tabla"].append({
            "k": k,
            "a": a,
            "b": b,
            "xr": xr,
            "fa": fa,
            "fb": fb,
            "fr": fr,
            "eb": eb,
            "ea": error_aproximado,
            "error_relativo": error_relativo,
        })

        # Actualizar la aproximación y los resultados de la iteración.
        resultado["raiz"] = xr
        resultado["valor_funcion"] = fr
        resultado["error"] = eb
        resultado["iteraciones_realizadas"] = k

        # Criterio de parada 1: se encontró una raíz exacta.
        if fr == 0:
            resultado["estado"] = "Raíz exacta encontrada."
            break

        # Criterio de parada 2: la cota del error cumple la tolerancia.
        if eb <= tolerancia:
            resultado["estado"] = "Tolerancia alcanzada correctamente."
            break

        # Mantener la mitad del intervalo donde existe cambio de signo.
        if (fa < 0) != (fr < 0):
            b, fb = xr, fr
        else:
            a, fa = xr, fr

        # Conservar el punto medio para el siguiente cálculo del error.
        xr_anterior = xr

    # Informar si se agotaron las iteraciones sin cumplir la tolerancia.
    if not resultado["estado"]:
        resultado["estado"] = (
            "Se alcanzó el máximo de iteraciones sin garantizar "
            "la tolerancia solicitada."
        )

    # Comparar la aproximación propia con la referencia de SciPy.
    referencia = resultado["comparacion_scipy"]
    if referencia is not None and resultado["raiz"] is not None:
        resultado["diferencia_scipy"] = abs(
            resultado["raiz"] - referencia
        )

    # Guardar el intervalo final y devolver los resultados a la interfaz.
    resultado["intervalo_final"] = (a, b)
    return resultado

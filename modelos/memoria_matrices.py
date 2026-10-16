"""
Modelos de estado del constructor visual de expresiones matriciales.
Contiene las matrices base A y B (de solo lectura tras definirse), la pila de resultados
guardados R1–R7 con límite estricto y el constructor que acumula los tokens de la expresión.
"""

from collections import deque

from algoritmos.expresiones import (
    CAPACIDAD_PILA,
    GUARDADOS,
    esta_completa,
    siguientes_permitidos,
    texto_expresion,
)


def _congelar(matriz):
    """Copia una matriz a tuplas de tuplas para que nadie pueda modificarla."""
    return tuple(tuple(fila) for fila in matriz)


def _como_listas(matriz):
    """Devuelve una copia en listas, que es lo que esperan las funciones de algoritmos/."""
    return [list(fila) for fila in matriz]


class MatricesBase:
    """Guarda A y B: se definen una sola vez y después solo se pueden leer."""

    def __init__(self):
        self._a = None
        self._b = None

    @property
    def definidas(self):
        """True cuando A y B ya fueron definidas (y quedaron bloqueadas)."""
        return self._a is not None

    def definir(self, a, b):
        """Fija A y B por primera y única vez; una segunda llamada genera RuntimeError."""
        if self.definidas:
            raise RuntimeError("Las matrices A y B son de solo lectura: ya fueron definidas.")
        self._a, self._b = _congelar(a), _congelar(b)

    @property
    def a(self):
        """Copia de A (modificar la copia no altera la original)."""
        return _como_listas(self._a)

    @property
    def b(self):
        """Copia de B (modificar la copia no altera la original)."""
        return _como_listas(self._b)

    def contexto(self):
        """Devuelve {'A': ..., 'B': ...} para evaluar expresiones."""
        return {"A": self.a, "B": self.b} if self.definidas else {}


class PilaResultados:
    """Siete ranuras fijas (R1–R7). Al llenarse, se reemplaza la más antigua con confirmación."""

    def __init__(self):
        self._ranuras = [None] * CAPACIDAD_PILA
        self._orden = deque()  # índices ocupados, del más antiguo al más reciente

    @property
    def cantidad(self):
        """Cuántas ranuras están ocupadas (para mostrar «n/7»)."""
        return len(self._orden)

    @property
    def esta_llena(self):
        """True cuando las 7 ranuras están ocupadas."""
        return self.cantidad == CAPACIDAD_PILA

    @property
    def indice_mas_antiguo(self):
        """Índice (0–6) de la ranura que se reemplazaría, o None si hay espacio libre."""
        return self._orden[0] if self.esta_llena else None

    def guardar(self, matriz, reemplazar=False):
        """Guarda una copia de `matriz` y devuelve el índice de la ranura usada.

        Con espacio libre usa la ranura vacía de menor índice. Si está llena y
        reemplazar=False genera OverflowError; con reemplazar=True sobrescribe la más antigua.
        """
        if self.esta_llena:
            if not reemplazar:
                raise OverflowError("Memoria llena (7/7): elimina un resultado o confirma el reemplazo.")
            indice = self._orden.popleft()
        else:
            indice = self._ranuras.index(None)
        self._ranuras[indice] = _congelar(matriz)
        self._orden.append(indice)
        return indice

    def eliminar(self, indice):
        """Vacía la ranura `indice` (0–6); si ya estaba vacía no hace nada."""
        if self._ranuras[indice] is not None:
            self._ranuras[indice] = None
            self._orden.remove(indice)

    def obtener(self, indice):
        """Devuelve una copia de la matriz de la ranura, o None si está vacía."""
        valor = self._ranuras[indice]
        return None if valor is None else _como_listas(valor)

    def contexto(self):
        """Devuelve {'R1': matriz, ...} solo con las ranuras ocupadas."""
        return {nombre: self.obtener(i) for i, nombre in enumerate(GUARDADOS) if self._ranuras[i] is not None}


class ConstructorExpresion:
    """Acumula los tokens que el usuario pulsa y dice qué botones están disponibles."""

    def __init__(self):
        self.tokens = []

    def agregar(self, token):
        """Agrega un token; si no es válido en este punto genera ValueError."""
        if token not in siguientes_permitidos(self.tokens):
            raise ValueError(f"«{token}» no se puede agregar después de «{self.texto or 'el inicio'}».")
        self.tokens.append(token)

    def deshacer(self):
        """Quita el último token."""
        if self.tokens:
            self.tokens.pop()

    def limpiar(self):
        """Borra toda la expresión."""
        self.tokens.clear()

    @property
    def permitidos(self):
        """Tokens cuyo botón debe estar habilitado ahora."""
        return siguientes_permitidos(self.tokens)

    @property
    def completa(self):
        """True si la expresión se puede evaluar."""
        return esta_completa(self.tokens)

    @property
    def texto(self):
        """Texto de solo lectura de la expresión armada."""
        return texto_expresion(self.tokens)

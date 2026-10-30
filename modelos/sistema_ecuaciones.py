"""
Modelo de datos para representar sistemas de ecuaciones lineales.
Almacena los coeficientes y términos independientes en una matriz aumentada [A | b].
Facilita el acceso a las dimensiones del sistema y la copia de sus datos.
"""


class SistemaEcuaciones:
    """Representa un sistema mediante su matriz aumentada [A | b]."""

    def __init__(self, matriz_aumentada, numero_variables):
        """Inicializa el sistema con su matriz aumentada y número de variables.
        Recibe una matriz y un entero; almacena una copia de sus filas.
        """
        self.matriz_aumentada = [fila[:] for fila in matriz_aumentada]
        self.numero_variables = numero_variables

    @property
    def numero_ecuaciones(self):
        """Devuelve el número de ecuaciones representadas en la matriz.
        No recibe parámetros adicionales y devuelve un entero.
        """
        return len(self.matriz_aumentada)

    def copiar_matriz(self):
        """Crea una copia independiente de las filas de la matriz aumentada.
        No recibe parámetros adicionales y devuelve una nueva lista de filas.
        """
        return [fila[:] for fila in self.matriz_aumentada]

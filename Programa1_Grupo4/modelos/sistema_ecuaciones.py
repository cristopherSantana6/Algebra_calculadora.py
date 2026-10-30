"""Modelo de datos para representar un sistema de ecuaciones."""


class SistemaEcuaciones:
    """Representa un sistema mediante su matriz aumentada [A | b]."""

    def __init__(self, matriz_aumentada, numero_variables):
        self.matriz_aumentada = [fila[:] for fila in matriz_aumentada]
        self.numero_variables = numero_variables

    @property
    def numero_ecuaciones(self):
        return len(self.matriz_aumentada)

    def copiar_matriz(self):
        return [fila[:] for fila in self.matriz_aumentada]

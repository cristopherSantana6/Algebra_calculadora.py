
"""
Componentes visuales reutilizables para la interfaz de la calculadora.
Define tarjetas con títulos y subtítulos opcionales.
Utiliza Tkinter y ttk para mantener un estilo visual uniforme.
"""
import tkinter as tk
from tkinter import ttk


class Tarjeta(ttk.Frame):
    """Contenedor visual estilo tarjeta."""

    def __init__(self, master, titulo, subtitulo=None, **kwargs):
        """Inicializa una tarjeta con título y subtítulo opcional.
            Recibe el contenedor principal, los textos y opciones adicionales
            de configuración del componente.
        """
        super().__init__(master, style="Card.TFrame", padding=18, **kwargs)
        encabezado = ttk.Frame(self, style="Card.TFrame")
        encabezado.pack(fill="x")

        ttk.Label(
            encabezado,
            text=titulo,
            style="CardTitle.TLabel",
        ).pack(anchor="w")

        if subtitulo:
            ttk.Label(
                encabezado,
                text=subtitulo,
                style="CardSubtitle.TLabel",
            ).pack(anchor="w", pady=(3, 0))

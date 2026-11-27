"""
Contenedor con barra de desplazamiento vertical.
El contenido se construye dentro de `interior`; la barra solo aparece
cuando el contenido no cabe en la pantalla.
"""

import tkinter as tk
from tkinter import ttk


class MarcoDesplazable(ttk.Frame):
    """Marco con Canvas y Scrollbar que envuelve el contenido de un módulo."""

    # Widgets que ya manejan su propia rueda del mouse.
    _CON_SCROLL_PROPIO = ("Text", "Treeview", "Listbox", "Canvas")

    def __init__(self, padre, app=None, **opciones):
        super().__init__(padre, **opciones)
        self.app = app
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        fondo = getattr(app, "BACKGROUND", None)
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        if fondo:
            self.canvas.configure(bg=fondo)
        self.barra = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.barra.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.interior = ttk.Frame(self.canvas)
        self._ventana = self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        # Recalcular tamaño cuando cambia la ventana o el contenido.
        self.canvas.bind("<Configure>", self._ajustar)
        self.interior.bind("<Configure>", self._ajustar)

        # La rueda del mouse solo actúa mientras el puntero está sobre el módulo.
        self.bind("<Enter>", lambda _e: self.bind_all("<MouseWheel>", self._rueda))
        self.bind("<Leave>", lambda _e: self.unbind_all("<MouseWheel>"))

        # Permite actualizar el fondo al cambiar de tema.
        if app is not None:
            if not hasattr(app, "canvas_desplazables"):
                app.canvas_desplazables = []
            app.canvas_desplazables.append(self.canvas)

    def _ajustar(self, _event=None):
        """Ancho igual al visible; alto = el mayor entre contenido y pantalla."""
        ancho = self.canvas.winfo_width()
        alto_visible = self.canvas.winfo_height()
        alto_contenido = self.interior.winfo_reqheight()
        self.canvas.itemconfigure(
            self._ventana, width=ancho, height=max(alto_contenido, alto_visible)
        )
        self.canvas.configure(scrollregion=(0, 0, ancho, max(alto_contenido, alto_visible)))

        # Mostrar la barra solo si el contenido no cabe.
        if alto_contenido > alto_visible + 1:
            if not self.barra.winfo_ismapped():
                self.barra.grid(row=0, column=1, sticky="ns")
        elif self.barra.winfo_ismapped():
            self.barra.grid_remove()
            self.canvas.yview_moveto(0)

    def _rueda(self, event):
        if not self.barra.winfo_ismapped():
            return
        # Si el puntero está sobre una tabla, texto o gráfica, ese widget se desplaza solo.
        widget = event.widget
        if not isinstance(widget, tk.Misc):
            return
        while widget is not None and widget is not self.canvas:
            if widget.winfo_class() in self._CON_SCROLL_PROPIO:
                return
            widget = widget.master
        if widget is None:
            return
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

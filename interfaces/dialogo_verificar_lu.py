"""Diálogo para ingresar manualmente L y U y comprobar que L · U = A."""

import tkinter as tk
from tkinter import ttk, messagebox

from interfaces.ventana_matriz import crear_matriz_visual
from modulos.modulo_lu import verificar_factorizacion
from utilidades.fracciones import leer_fraccion, formatear_fraccion


class DialogoVerificarLU:
    """Permite escribir L y U, multiplicarlas y compararlas exactamente con A."""

    def __init__(self, app, matriz_a):
        self.app = app
        self.matriz_a = [[valor for valor in fila] for fila in matriz_a]
        self.m = len(self.matriz_a)
        self.n = len(self.matriz_a[0])
        self.ventana = tk.Toplevel(app.root)
        self.ventana.title("Verificación manual • L · U = A")
        self.ventana.geometry("920x760")
        self.ventana.minsize(760, 620)
        self.ventana.transient(app.root)
        self.ventana.grab_set()
        self.ventana.configure(bg=getattr(app, "BACKGROUND", "#EEF3F1"))

        self.entradas_l = []
        self.entradas_u = []
        self._construir()

    def _construir(self):
        """Crea pestañas para L, U, la matriz A de referencia y el resultado."""
        contenedor = ttk.Frame(self.ventana, padding=16)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Comprobar la factorización L · U = A",
            style="Header.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text=(
                f"A tiene dimensión {self.m}×{self.n}. Ingrese L ({self.m}×{self.m}) "
                f"y U ({self.m}×{self.n}). Se aceptan enteros, decimales y fracciones."
            ),
            style="CardSubtitle.TLabel",
            wraplength=850,
        ).pack(anchor="w", pady=(4, 12))

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.pack(fill="both", expand=True)

        tab_l = ttk.Frame(self.notebook, padding=12)
        tab_u = ttk.Frame(self.notebook, padding=12)
        tab_a = ttk.Frame(self.notebook, padding=12)
        tab_resultado = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(tab_l, text=f"Matriz L ({self.m}×{self.m})")
        self.notebook.add(tab_u, text=f"Matriz U ({self.m}×{self.n})")
        self.notebook.add(tab_a, text=f"Matriz A ({self.m}×{self.n})")
        self.notebook.add(tab_resultado, text="Comprobación")

        self._crear_entradas(tab_l, self.m, self.m, self.entradas_l, "L")
        self._crear_entradas(tab_u, self.m, self.n, self.entradas_u, "U")

        ttk.Label(
            tab_a,
            text="Esta es la matriz A que se ingresó en la pantalla de Factorización LU.",
            style="CardSubtitle.TLabel",
        ).pack(anchor="w", pady=(0, 10))
        crear_matriz_visual(tab_a, self.matriz_a, cell_width=72, pad=3).pack(anchor="center")

        self.resultado_frame = ttk.Frame(tab_resultado)
        self.resultado_frame.pack(fill="both", expand=True)
        ttk.Label(
            self.resultado_frame,
            text="Ingrese L y U, luego presione «Calcular L · U y comparar con A».",
            style="CardSubtitle.TLabel",
            wraplength=780,
        ).pack(anchor="w", pady=8)

        pie = ttk.Frame(contenedor)
        pie.pack(fill="x", pady=(12, 0))
        ttk.Button(
            pie,
            text="Calcular L · U y comparar con A",
            style="Accent.TButton",
            command=self.comprobar,
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(
            pie,
            text="Limpiar L y U",
            style="Coral.TButton",
            command=self.limpiar,
        ).pack(side="left", padx=6)
        ttk.Button(
            pie,
            text="Cerrar",
            command=self.ventana.destroy,
        ).pack(side="right", padx=(6, 0))

    def _crear_entradas(self, padre, filas, columnas, destino, nombre):
        """Construye una cuadrícula editable y enlaza Enter para avanzar."""
        ttk.Label(
            padre,
            text=f"Ingrese los coeficientes de la matriz {nombre}:",
            style="SectionTitle.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        area = ttk.Frame(padre)
        area.pack(anchor="center", pady=8)
        for i in range(filas):
            fila = []
            for j in range(columnas):
                entrada = ttk.Entry(area, width=10, justify="center")
                entrada.insert(0, "0")
                entrada.grid(row=i, column=j, padx=4, pady=4)
                entrada.bind("<FocusIn>", self._seleccionar_cero)
                entrada.bind(
                    "<Return>",
                    lambda event, campo=entrada, campos=destino:
                        self._avanzar(event, campo, campos),
                )
                fila.append(entrada)
            destino.append(fila)

        ttk.Label(
            padre,
            text="Consejo: al entrar en una casilla, el 0 inicial se selecciona. Presione Enter para avanzar.",
            style="CardSubtitle.TLabel",
            wraplength=780,
        ).pack(anchor="w", pady=(8, 0))

    @staticmethod
    def _seleccionar_cero(event):
        entrada = event.widget
        if entrada.get().strip() == "0":
            entrada.selection_range(0, "end")

    @staticmethod
    def _avanzar(event, entrada_actual, matriz_entradas):
        campos = [entrada for fila in matriz_entradas for entrada in fila]
        try:
            indice = campos.index(entrada_actual)
        except ValueError:
            return "break"
        if indice + 1 < len(campos):
            campos[indice + 1].focus_set()
            if campos[indice + 1].get().strip() == "0":
                campos[indice + 1].selection_range(0, "end")
        return "break"

    def _leer_matriz(self, entradas, nombre):
        matriz = []
        for i, fila in enumerate(entradas):
            valores = []
            for j, entrada in enumerate(fila):
                try:
                    valores.append(leer_fraccion(entrada.get()))
                except (ValueError, ZeroDivisionError) as error:
                    mensaje = str(error) if str(error) else "El denominador no puede ser cero."
                    messagebox.showerror(
                        "Dato inválido",
                        f"Matriz {nombre}, fila {i + 1}, columna {j + 1}: {mensaje}",
                        parent=self.ventana,
                    )
                    entrada.focus_set()
                    entrada.selection_range(0, "end")
                    return None
            matriz.append(valores)
        return matriz

    def limpiar(self):
        """Restablece las casillas de L y U a cero y limpia el resultado."""
        for entradas in (self.entradas_l, self.entradas_u):
            for fila in entradas:
                for entrada in fila:
                    entrada.delete(0, "end")
                    entrada.insert(0, "0")
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()
        ttk.Label(
            self.resultado_frame,
            text="Las matrices L y U se han limpiado.",
            style="CardSubtitle.TLabel",
        ).pack(anchor="w", pady=8)

    def comprobar(self):
        """Calcula L·U con aritmética exacta y verifica si coincide con A."""
        matriz_l = self._leer_matriz(self.entradas_l, "L")
        if matriz_l is None:
            return
        matriz_u = self._leer_matriz(self.entradas_u, "U")
        if matriz_u is None:
            return

        try:
            verificacion = verificar_factorizacion(
                self.matriz_a,
                matriz_l,
                matriz_u,
            )
        except ValueError as error:
            messagebox.showerror(
                "No se pudo multiplicar",
                str(error),
                parent=self.ventana,
            )
            return

        producto = verificacion["producto"]
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()

        if verificacion["es_correcta"]:
            estilo = "Status.TLabel"
            mensaje = "✓ Correcto: L · U = A. La factorización coincide exactamente."
        else:
            estilo = "StatusBad.TLabel"
            mensaje = "✗ Incorrecto: L · U no coincide con la matriz A."

        ttk.Label(
            self.resultado_frame,
            text=mensaje,
            style=estilo,
            padding=10,
            wraplength=790,
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            self.resultado_frame,
            text="Producto calculado L · U:",
            style="SectionTitle.TLabel",
        ).pack(anchor="w", pady=(4, 6))
        crear_matriz_visual(
            self.resultado_frame,
            producto,
            cell_width=72,
            pad=3,
        ).pack(anchor="center", pady=(0, 8))

        if not verificacion["es_correcta"]:
            diferencias = []
            for i in range(self.m):
                for j in range(self.n):
                    if producto[i][j] != self.matriz_a[i][j]:
                        diferencias.append(
                            f"Fila {i + 1}, columna {j + 1}: "
                            f"L·U = {formatear_fraccion(producto[i][j])}; "
                            f"A = {formatear_fraccion(self.matriz_a[i][j])}."
                        )
            ttk.Label(
                self.resultado_frame,
                text="Diferencias encontradas:",
                style="SectionTitle.TLabel",
            ).pack(anchor="w", pady=(4, 3))
            for diferencia in diferencias[:12]:
                ttk.Label(
                    self.resultado_frame,
                    text="• " + diferencia,
                    style="AnalysisBody.TLabel",
                    wraplength=790,
                ).pack(anchor="w", pady=1)
            if len(diferencias) > 12:
                ttk.Label(
                    self.resultado_frame,
                    text=f"Se muestran 12 de {len(diferencias)} diferencias.",
                    style="CardSubtitle.TLabel",
                ).pack(anchor="w", pady=(4, 0))

        self.notebook.select(3)

"""
Interfaz gráfica del método abierto de Newton-Raphson.
Permite introducir f(x), x0, tolerancia y límite de iteraciones;
muestra el historial de cálculo y la gráfica con las tangentes.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from interfaces.componentes.tarjeta import Tarjeta
from algoritmos.newton_raphson import (
    resolver_newton_raphson,
    graficar_newton_raphson,
)


class VistaNewtonRaphson:
    """Vista para ejecutar y estudiar el método de Newton-Raphson."""

    def __init__(self, padre):
        self.padre = padre
        self.app = padre.app
        self.marco = ttk.Frame(padre.marco)
        self.marco.grid(row=1, column=0, sticky="nsew")

        self.funcion = tk.StringVar(master=self.app.root, value="x**2 - 2")
        self.x0 = tk.StringVar(master=self.app.root, value="1.5")
        self.tolerancia = tk.StringVar(master=self.app.root, value="0.000001")
        self.max_iteraciones = tk.StringVar(master=self.app.root, value="100")
        self.ultimo_resultado = None
        self.canvas_grafica = None
        self._construir()

    def _construir(self):
        self.marco.columnconfigure(0, weight=1, minsize=280)
        self.marco.columnconfigure(1, weight=2)
        self.marco.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.marco,
            "Newton-Raphson",
            "Método abierto para aproximar raíces de f(x) = 0."
        )
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        derecha = Tarjeta(
            self.marco,
            "Resultado y procedimiento",
            "Derivada simbólica, iteraciones, error y residuo."
        )
        derecha.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(
            izquierda, text="Función f(x)", style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(12, 5))
        ttk.Entry(
            izquierda, textvariable=self.funcion, font=("Consolas", 11)
        ).pack(fill="x")
        ttk.Label(
            izquierda,
            text="Ejemplos: x**2 - 2, x**3 - x - 2, cos(x) - x",
            style="CardSubtitle.TLabel",
            wraplength=300,
            justify="left"
        ).pack(anchor="w", pady=(4, 10))

        self._campo(izquierda, "Valor inicial (x₀)", self.x0)
        self._campo(izquierda, "Tolerancia", self.tolerancia)
        self._campo(izquierda, "Máximo de iteraciones", self.max_iteraciones)

        ttk.Label(
            izquierda,
            text="Criterio de parada",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(14, 4))
        ttk.Label(
            izquierda,
            text="Error aproximado ≤ tolerancia y |f(x)| ≤ tolerancia. "
                 "Si x siguiente es cero, se informa error absoluto.",
            style="CardSubtitle.TLabel",
            wraplength=300,
            justify="left"
        ).pack(anchor="w")

        ttk.Button(
            izquierda,
            text="Calcular raíz aproximada",
            style="Accent.TButton",
            command=self.calcular
        ).pack(fill="x", pady=(18, 6))
        ttk.Button(
            izquierda,
            text="Graficar función y tangentes",
            style="Op.TButton",
            command=self.mostrar_grafica
        ).pack(fill="x", pady=3)
        ttk.Button(
            izquierda,
            text="Limpiar",
            style="Coral.TButton",
            command=self.limpiar
        ).pack(fill="x", pady=3)

        self.notebook = ttk.Notebook(derecha)
        self.notebook.pack(fill="both", expand=True, pady=(12, 0))
        self.pestana_resumen = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.pestana_tabla = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.pestana_grafica = ttk.Frame(self.notebook, style="Card.TFrame", padding=8)
        self.notebook.add(self.pestana_resumen, text="Resumen")
        self.notebook.add(self.pestana_tabla, text="Iteraciones")
        self.notebook.add(self.pestana_grafica, text="Gráfica")

        self._mostrar_inicio()

    @staticmethod
    def _campo(padre, etiqueta, variable):
        ttk.Label(
            padre, text=etiqueta, style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(9, 3))
        ttk.Entry(padre, textvariable=variable).pack(fill="x")

    @staticmethod
    def _fmt(valor):
        if valor is None:
            return "—"
        if isinstance(valor, (int, float)):
            return f"{valor:.10g}"
        return str(valor)

    def _limpiar_pestana(self, pestaña):
        for widget in pestaña.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self):
        for pestaña in (
            self.pestana_resumen,
            self.pestana_tabla,
            self.pestana_grafica,
        ):
            self._limpiar_pestana(pestaña)

        ttk.Label(
            self.pestana_resumen,
            text="Aproximar una raíz por Newton-Raphson",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(8, 10))
        ttk.Label(
            self.pestana_resumen,
            text=(
                "1. Escriba la función f(x).\n"
                "2. Indique el valor inicial x₀.\n"
                "3. Configure la tolerancia y el máximo de iteraciones.\n"
                "4. Presione «Calcular raíz aproximada».\n\n"
                "El programa obtiene f'(x) simbólicamente con SymPy y "
                "muestra el desarrollo de cada iteración. La derivada "
                "nula o muy pequeña detiene el cálculo con un mensaje."
            ),
            style="AnalysisBody.TLabel",
            justify="left",
            wraplength=560
        ).pack(anchor="w")
        ttk.Label(
            self.pestana_resumen,
            text="Fórmula iterativa",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(22, 6))
        ttk.Label(
            self.pestana_resumen,
            text="x₍ᵢ₊₁₎ = xᵢ − f(xᵢ) / f′(xᵢ)",
            style="Operation.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            self.pestana_tabla,
            text="La tabla de iteraciones aparecerá después del cálculo.",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=10)
        ttk.Label(
            self.pestana_grafica,
            text="La gráfica de la función y sus tangentes aparecerá aquí.",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=10)

    def calcular(self):
        try:
            resultado = resolver_newton_raphson(
                self.funcion.get().strip(),
                self.x0.get().strip(),
                self.tolerancia.get().strip(),
                self.max_iteraciones.get().strip()
            )
        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror(
                "No se pudo calcular",
                str(error),
                parent=self.app.root
            )
            return

        self.ultimo_resultado = resultado
        self._mostrar_resumen(resultado)
        self._mostrar_tabla(resultado)
        self._limpiar_pestana(self.pestana_grafica)
        ttk.Label(
            self.pestana_grafica,
            text="Presione «Graficar función y tangentes» para generar la representación.",
            style="CardSubtitle.TLabel",
            wraplength=540
        ).pack(anchor="w", pady=10)
        self.notebook.select(self.pestana_resumen)

    def _mostrar_resumen(self, datos):
        self._limpiar_pestana(self.pestana_resumen)
        estado_ok = datos["residuo"] <= datos["tolerancia"] and (
            "Convergencia alcanzada" in datos["estado"]
        )
        ttk.Label(
            self.pestana_resumen,
            text=datos["estado"],
            style="Status.TLabel" if estado_ok else "StatusBad.TLabel",
            padding=9,
            wraplength=540
        ).pack(fill="x", pady=(0, 12))

        informacion = [
            ("Función", str(datos["funcion"])),
            ("Derivada", str(datos["derivada"])),
            ("Raíz aproximada", self._fmt(datos["aproximacion"])),
            ("Iteraciones realizadas", str(datos["iteraciones"])),
            ("Error aproximado", (
                f'{self._fmt(datos["error"])} ({datos["tipo_error"]})'
                if datos["error"] is not None else "No calculado"
            )),
            ("Residuo |f(x)|", self._fmt(datos["residuo"])),
            ("Tolerancia", self._fmt(datos["tolerancia"])),
        ]
        for etiqueta, valor in informacion:
            fila = ttk.Frame(self.pestana_resumen, style="Card.TFrame")
            fila.pack(fill="x", pady=4)
            ttk.Label(
                fila, text=etiqueta, style="CardSubtitle.TLabel"
            ).pack(side="left", anchor="nw")
            ttk.Label(
                fila, text=valor, style="MetricValue.TLabel",
                wraplength=360, justify="right"
            ).pack(side="right", anchor="ne")

        ttk.Label(
            self.pestana_resumen,
            text=(
                "El residuo comprueba la función original en la aproximación final. "
                "Una aproximación no se presenta como raíz exacta."
            ),
            style="CardSubtitle.TLabel",
            wraplength=540,
            justify="left"
        ).pack(anchor="w", pady=(16, 0))

    def _mostrar_tabla(self, datos):
        self._limpiar_pestana(self.pestana_tabla)
        ttk.Label(
            self.pestana_tabla,
            text="Historial de Newton-Raphson",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        columnas = ("i", "xi", "fx", "dfx", "xnext", "error", "tipo", "residuo")
        contenedor = ttk.Frame(self.pestana_tabla, style="Card.TFrame")
        contenedor.pack(fill="both", expand=True)
        tabla = ttk.Treeview(
            contenedor, columns=columnas,
            show="headings", height=13
        )
        encabezados = {
            "i": "i", "xi": "xᵢ", "fx": "f(xᵢ)",
            "dfx": "f′(xᵢ)", "xnext": "xᵢ₊₁",
            "error": "Error", "tipo": "Tipo", "residuo": "|f(xᵢ₊₁)|"
        }
        anchos = {
            "i": 42, "xi": 90, "fx": 90, "dfx": 90,
            "xnext": 100, "error": 100, "tipo": 105, "residuo": 105
        }
        for col in columnas:
            tabla.heading(col, text=encabezados[col])
            tabla.column(
                col, width=anchos[col], minwidth=55,
                anchor="center", stretch=True
            )

        for fila in datos["historial"]:
            tabla.insert(
                "", "end",
                values=(
                    fila["i"], self._fmt(fila["xi"]),
                    self._fmt(fila["fx"]), self._fmt(fila["dfx"]),
                    self._fmt(fila["xnext"]), self._fmt(fila["error"]),
                    fila["tipo"], self._fmt(fila["residuo"])
                )
            )

        barra_y = ttk.Scrollbar(
            contenedor, orient="vertical", command=tabla.yview
        )
        barra_x = ttk.Scrollbar(
            self.pestana_tabla, orient="horizontal", command=tabla.xview
        )
        tabla.configure(
            yscrollcommand=barra_y.set,
            xscrollcommand=barra_x.set
        )
        tabla.pack(side="left", fill="both", expand=True)
        barra_y.pack(side="right", fill="y")
        barra_x.pack(fill="x")
        ttk.Label(
            self.pestana_tabla,
            text="El error es relativo porcentual, salvo cuando xᵢ₊₁ = 0; en ese caso se presenta el absoluto.",
            style="CardSubtitle.TLabel",
            wraplength=540
        ).pack(anchor="w", pady=(8, 0))

        if not datos["historial"]:
            ttk.Label(
                self.pestana_tabla,
                text="No hubo iteraciones: la aproximación inicial ya satisface la tolerancia o el método se detuvo antes de avanzar.",
                style="CardSubtitle.TLabel",
                wraplength=540
            ).pack(anchor="w", pady=8)

    def mostrar_grafica(self):
        if self.ultimo_resultado is None:
            messagebox.showwarning(
                "Sin cálculo",
                "Primero calcule una aproximación con Newton-Raphson.",
                parent=self.app.root
            )
            return
        try:
            figura, _ax = graficar_newton_raphson(self.ultimo_resultado)
        except (ValueError, TypeError, OverflowError, RuntimeError) as error:
            messagebox.showerror(
                "No se pudo generar la gráfica",
                str(error),
                parent=self.app.root
            )
            return

        self._limpiar_pestana(self.pestana_grafica)
        self.canvas_grafica = FigureCanvasTkAgg(
            figura, master=self.pestana_grafica
        )
        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().pack(
            fill="both", expand=True
        )
        self.notebook.select(self.pestana_grafica)

    def limpiar(self):
        self.funcion.set("x**2 - 2")
        self.x0.set("1.5")
        self.tolerancia.set("0.000001")
        self.max_iteraciones.set("100")
        self.ultimo_resultado = None
        self.canvas_grafica = None
        self._mostrar_inicio()

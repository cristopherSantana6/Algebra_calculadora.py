"""Interfaz para comparar Jacobi y Gauss-Seidel."""

import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction

from algoritmos.metodos_iterativos import resolver_iterativos
from modulos.modulo_gauss import gauss_jordan


class VistaIterativos:
    """Formulario, tabla de iteraciones y comparación gráfica."""

    def __init__(self, parent, app):
        self.app = app
        self.marco = ttk.Frame(parent)
        self.marco.grid(row=0, column=0, sticky="nsew")
        self.marco.columnconfigure(0, weight=1)
        self.marco.columnconfigure(1, weight=2)
        ttk.Label(self.marco, text="Jacobi y Gauss-Seidel", style="PageTitle.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
        self.entrada = ttk.Frame(self.marco, style="Card.TFrame", padding=14)
        self.entrada.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.salida = ttk.Frame(self.marco, style="Card.TFrame", padding=14)
        self.salida.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(self.entrada, text="Sistema Ax = b", style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(self.entrada, text="Una fila de A por línea; separe números con espacios o comas.",
                  style="CardSubtitle.TLabel", wraplength=350).pack(anchor="w", pady=(4, 8))
        caja_matriz = ttk.Frame(self.entrada)
        caja_matriz.pack(fill="x", pady=(0, 3))
        self.A = tk.Text(caja_matriz, height=6, width=35, wrap="none", font=("Consolas", 10))
        self.A.insert("1.0", "10 -1 2\n-1 11 -1\n2 -1 10")
        self.A.bind("<KeyRelease>", self._ajustar_editor_matriz)
        self._ajustar_editor_matriz()
        self.A.pack(anchor="w")
        self.b = self._campo("Vector b (separado por espacios o comas)", "6 25 -11")
        self.x0 = self._campo("Vector inicial x⁽⁰⁾", "0 0 0")
        fila = ttk.Frame(self.entrada, style="Card.TFrame")
        fila.pack(fill="x", pady=4)
        self.tol = ttk.Entry(fila, width=12)
        self.tol.insert(0, "0.000001")
        self.maxit = ttk.Entry(fila, width=8)
        self.maxit.insert(0, "100")
        ttk.Label(fila, text="Tolerancia ε", style="CardSubtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(fila, text="Máx. iteraciones", style="CardSubtitle.TLabel").grid(row=0, column=1, sticky="w", padx=(12, 0))
        self.tol.grid(row=1, column=0, sticky="w")
        self.maxit.grid(row=1, column=1, sticky="w", padx=(12, 0))
        self.auto_orden = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.entrada, text="Buscar reordenamiento de ecuaciones si ayuda", variable=self.auto_orden).pack(anchor="w", pady=8)
        ttk.Button(self.entrada, text="Calcular y comparar", style="Accent.TButton", command=self.calcular).pack(anchor="w", pady=(3, 8))
        ttk.Label(self.entrada, text="La dominancia estricta garantiza convergencia, pero su ausencia por sí sola no implica divergencia.",
                  style="CardSubtitle.TLabel", wraplength=350).pack(anchor="w", pady=(4, 0))
        ttk.Label(self.salida, text="Resultados y comparación", style="SectionTitle.TLabel").pack(anchor="w")
        self.resultado = ttk.Frame(self.salida, style="Card.TFrame")
        self.resultado.pack(fill="both", expand=True, pady=(8, 0))
        self._mensaje("Complete el sistema y pulse «Calcular y comparar».")

    def _campo(self, titulo, valor):
        ttk.Label(self.entrada, text=titulo, style="CardSubtitle.TLabel").pack(anchor="w", pady=(7, 3))
        campo = ttk.Entry(self.entrada)
        campo.insert(0, valor)
        campo.pack(fill="x")
        return campo

    def _ajustar_editor_matriz(self, _event=None):
        """Expande el editor hasta mostrar la matriz sin barras anidadas."""
        lineas = [linea for linea in self.A.get("1.0", "end-1c").splitlines()]
        self.A.configure(
            height=max(6, len(lineas)),
            width=max(35, max((len(linea) for linea in lineas), default=0) + 1),
        )

    @staticmethod
    def _vector(texto):
        return [float(v) for v in texto.replace(",", " ").split()]

    def _mensaje(self, texto):
        for w in self.resultado.winfo_children():
            w.destroy()
        ttk.Label(self.resultado, text=texto, style="AnalysisBody.TLabel", wraplength=700, justify="left").pack(anchor="w")

    def calcular(self):
        try:
            A = [[float(v) for v in fila.replace(",", " ").split()] for fila in self.A.get("1.0", "end").splitlines() if fila.strip()]
            datos = resolver_iterativos(A, self._vector(self.b.get()), self._vector(self.x0.get()),
                                        self.tol.get(), self.maxit.get(), self.auto_orden.get())
            vector_b = self._vector(self.b.get())
            aumentada = [[Fraction(str(v)) for v in fila] + [Fraction(str(vector_b[i]) )]
                         for i, fila in enumerate(A)]
            reducida, pivotes, inconsistente, _ = gauss_jordan(aumentada, len(A))
            if inconsistente or len(pivotes) != len(A):
                referencia = None
            else:
                referencia = [0.0] * len(A)
                for fila, columna in pivotes:
                    referencia[columna] = float(reducida[fila][-1])
        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror("Datos no válidos", str(error), parent=self.app.root)
            return
        self._mensaje("")
        perm = datos["permutacion"]
        original = ", ".join(str(i + 1) for i in perm)
        dom_inicio = "sí" if datos["diagonal_dominante_inicial"] else "no"
        dom = "sí" if datos["diagonal_dominante"] else "no"
        ttk.Label(self.resultado, text=f"Dominancia diagonal estricta: original {dom_inicio}; con filas usadas {dom}. Filas utilizadas en orden: {original}.",
                  style="AnalysisBody.TLabel", wraplength=720).pack(anchor="w", pady=(0, 8))
        for clave in ("jacobi", "gauss_seidel"):
            r = datos[clave]
            valores = ", ".join(f"{v:.10g}" for v in r["x"])
            ttk.Label(self.resultado, text=f"{r['metodo']}: x ≈ ({valores}) | {r['estado']} | iteraciones: {r['iteraciones']} | residuo ‖Ax−b‖∞ = {r['residuo']:.4g}",
                      style="AnalysisBody.TLabel", wraplength=720, justify="left").pack(anchor="w", pady=3)
        j, g = datos["jacobi"], datos["gauss_seidel"]
        diferencia = max(abs(a-b) for a, b in zip(j["x"], g["x"]))
        mas_rapido = "Jacobi" if j["iteraciones"] < g["iteraciones"] else "Gauss-Seidel" if g["iteraciones"] < j["iteraciones"] else "ambos igual"
        ttk.Label(self.resultado, text=f"Diferencia ‖xᴶ−xᴳˢ‖∞ = {diferencia:.4g}. Menos iteraciones: {mas_rapido}.",
                  style="AnalysisBody.TLabel", wraplength=720).pack(anchor="w", pady=(2, 8))
        if referencia is not None:
            for nombre, r in (("Jacobi", j), ("Gauss-Seidel", g)):
                diferencia_ref = max(abs(a-b) for a, b in zip(r["x"], referencia))
                ttk.Label(self.resultado, text=f"Validación de {nombre} contra Gauss-Jordan: x = ({', '.join(f'{v:.10g}' for v in referencia)}); ‖x−xref‖∞ = {diferencia_ref:.4g}.",
                          style="AnalysisBody.TLabel", wraplength=720).pack(anchor="w", pady=2)
        else:
            ttk.Label(self.resultado, text="Gauss-Jordan indica que el sistema no tiene solución única; no hay vector de referencia único para comparar.",
                      style="CardSubtitle.TLabel", wraplength=720).pack(anchor="w", pady=2)

        columnas = ("k", "x", "error")
        total_filas = len(j["historial"]) + len(g["historial"])
        tabla = ttk.Treeview(self.resultado, columns=columnas, show="headings", height=max(1, total_filas))
        for c, titulo in zip(columnas, ("Iteración", "Aproximaciones", "Error ‖xᵏ−xᵏ⁻¹‖∞")):
            tabla.heading(c, text=titulo)
            tabla.column(c, width=125 if c != "x" else 350, minwidth=70, stretch=True, anchor="center")
        for metodo, resultado in (("J", j), ("GS", g)):
            for paso in resultado["historial"]:
                vs = "(" + ", ".join(f"{v:.7g}" for v in paso["x"]) + ")"
                err = "—" if paso["error"] is None else f"{paso['error']:.5g}"
                tabla.insert("", "end", values=(f"{metodo} {paso['k']}", vs, err))
        tabla.pack(fill="both", expand=True, pady=(3, 0))
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig = Figure(figsize=(7, 2.8), dpi=90)
            ax = fig.add_subplot(111)
            for nombre, r in (("Jacobi", j), ("Gauss-Seidel", g)):
                xs = [p["k"] for p in r["historial"] if p["error"] is not None]
                ys = [p["error"] for p in r["historial"] if p["error"] is not None]
                if xs:
                    ax.semilogy(xs, ys, marker="o", markersize=3, label=nombre)
            ax.set(xlabel="Iteración", ylabel="Error ∞", title="Comparación del error por iteración")
            ax.grid(True, alpha=.3)
            ax.legend()
            fig.tight_layout()
            graf = FigureCanvasTkAgg(fig, master=self.resultado)
            graf.draw()
            graf.get_tk_widget().pack(fill="x", pady=(8, 0))
            self.grafica = graf
        except (ImportError, ValueError):
            ttk.Label(self.resultado, text="La gráfica requiere Matplotlib.", style="CardSubtitle.TLabel").pack(anchor="w")

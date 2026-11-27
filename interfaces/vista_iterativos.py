"""
Vista gráfica para los métodos iterativos de Jacobi y Gauss-Seidel.
Se integra como una pestaña de Métodos Numéricos.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from interfaces.componentes.tarjeta import Tarjeta
from algoritmos.metodos_iterativos import resolver_iterativos


class VistaIterativos:
    """Formulario, resultados e historial de iteraciones de Ax=b."""

    EJEMPLO_A = [
        ["10", "-1", "2"],
        ["-1", "11", "-1"],
        ["2", "-1", "10"],
    ]
    EJEMPLO_B = ["6", "22", "-10"]
    EJEMPLO_X0 = ["0", "0", "0"]

    def __init__(self, padre):
        self.padre = padre
        self.app = padre.app
        self.marco = ttk.Frame(padre.marco)
        self.marco.grid(row=1, column=0, sticky="nsew")

        self.dimension = tk.IntVar(master=self.app.root, value=3)
        self.metodo = tk.StringVar(master=self.app.root, value="Jacobi")
        self.tolerancia = tk.StringVar(master=self.app.root, value="0.000001")
        self.max_iteraciones = tk.StringVar(master=self.app.root, value="100")
        self.matriz_vars = []
        self.vector_vars = []
        self.inicial_vars = []
        self.ultimo_resultado = None

        self._construir()

    def _construir(self):
        self.marco.columnconfigure(0, weight=1)
        self.marco.columnconfigure(1, weight=2)
        self.marco.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.marco,
            "Métodos Iterativos",
            "Configure el sistema Ax = b y seleccione el método."
        )
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        derecha = Tarjeta(
            self.marco,
            "Resultados y convergencia",
            "Aproximación final, error, residuo e historial de iteraciones."
        )
        derecha.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(
            izquierda, text="Método de solución",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(12, 5))

        self.selector = ttk.Combobox(
            izquierda,
            textvariable=self.metodo,
            values=("Jacobi", "Gauss-Seidel"),
            state="readonly"
        )
        self.selector.pack(fill="x")

        self.descripcion_metodo = ttk.Label(
            izquierda,
            text="Jacobi calcula cada componente usando únicamente la iteración anterior.",
            style="CardSubtitle.TLabel",
            wraplength=330,
            justify="left"
        )
        self.descripcion_metodo.pack(anchor="w", pady=(5, 8))
        self.selector.bind("<<ComboboxSelected>>", self._actualizar_descripcion)

        fila_dimension = ttk.Frame(izquierda, style="Card.TFrame")
        fila_dimension.pack(fill="x", pady=(7, 5))
        ttk.Label(
            fila_dimension, text="Número de incógnitas",
            style="CardSubtitle.TLabel"
        ).pack(side="left")
        self.spin_dimension = ttk.Spinbox(
            fila_dimension, from_=2, to=6, width=5,
            textvariable=self.dimension, command=self._cambiar_dimension
        )
        self.spin_dimension.pack(side="right")
        self.spin_dimension.bind("<Return>", self._cambiar_dimension)
        self.spin_dimension.bind("<FocusOut>", self._cambiar_dimension)

        ttk.Label(
            izquierda, text="Matriz de coeficientes A",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(8, 5))

        self.marco_matriz = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_matriz.pack(fill="x")

        ttk.Label(
            izquierda, text="Vector de términos independientes b",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(12, 5))
        self.marco_b = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_b.pack(fill="x")

        ttk.Label(
            izquierda, text="Aproximación inicial x⁽⁰⁾",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(12, 5))
        self.marco_x0 = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_x0.pack(fill="x")

        parametros = ttk.Frame(izquierda, style="Card.TFrame")
        parametros.pack(fill="x", pady=(12, 0))
        parametros.columnconfigure(0, weight=1)
        parametros.columnconfigure(1, weight=1)

        ttk.Label(
            parametros, text="Tolerancia",
            style="CardSubtitle.TLabel"
        ).grid(row=0, column=0, sticky="w", padx=(0, 6))
        ttk.Label(
            parametros, text="Máximo de iteraciones",
            style="CardSubtitle.TLabel"
        ).grid(row=0, column=1, sticky="w", padx=(6, 0))

        ttk.Entry(
            parametros, textvariable=self.tolerancia
        ).grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(3, 0))
        ttk.Entry(
            parametros, textvariable=self.max_iteraciones
        ).grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(3, 0))

        ttk.Button(
            izquierda, text="Resolver sistema",
            style="Accent.TButton", command=self.resolver
        ).pack(fill="x", pady=(14, 6))
        ttk.Button(
            izquierda, text="Restablecer ejemplo",
            style="Coral.TButton", command=self.restablecer
        ).pack(fill="x")

        self.panel_resultado = ttk.Frame(derecha, style="Card.TFrame")
        self.panel_resultado.pack(fill="both", expand=True, pady=(12, 0))

        self._crear_campos()
        self._mostrar_inicio()

    def _actualizar_descripcion(self, _event=None):
        if self.metodo.get() == "Jacobi":
            texto = (
                "Jacobi calcula todos los componentes nuevos usando "
                "exclusivamente los valores de la iteración anterior."
            )
        else:
            texto = (
                "Gauss-Seidel aprovecha inmediatamente cada componente "
                "nuevo calculado dentro de la misma iteración."
            )
        self.descripcion_metodo.configure(text=texto)

    def _crear_campos(self):
        n = max(2, min(6, int(self.dimension.get())))
        self.dimension.set(n)

        anterior_A = [
            [v.get() for v in fila] for fila in self.matriz_vars
        ]
        anterior_b = [v.get() for v in self.vector_vars]
        anterior_x0 = [v.get() for v in self.inicial_vars]

        for marco in (self.marco_matriz, self.marco_b, self.marco_x0):
            for widget in marco.winfo_children():
                widget.destroy()

        self.matriz_vars = []
        self.vector_vars = []
        self.inicial_vars = []

        for i in range(n):
            fila_vars = []
            for j in range(n):
                if i < len(anterior_A) and j < len(anterior_A[i]):
                    valor = anterior_A[i][j]
                elif i < 3 and j < 3:
                    valor = self.EJEMPLO_A[i][j]
                else:
                    valor = "0"
                variable = tk.StringVar(master=self.app.root, value=valor)
                fila_vars.append(variable)
                ttk.Entry(
                    self.marco_matriz, textvariable=variable,
                    width=7, justify="center"
                ).grid(row=i, column=j, padx=2, pady=2, sticky="ew")
            self.matriz_vars.append(fila_vars)

        for i in range(n):
            valor_b = anterior_b[i] if i < len(anterior_b) else (
                self.EJEMPLO_B[i] if i < 3 else "0"
            )
            valor_x = anterior_x0[i] if i < len(anterior_x0) else "0"

            vb = tk.StringVar(master=self.app.root, value=valor_b)
            vx = tk.StringVar(master=self.app.root, value=valor_x)
            self.vector_vars.append(vb)
            self.inicial_vars.append(vx)

            ttk.Entry(
                self.marco_b, textvariable=vb, width=7,
                justify="center"
            ).grid(row=0, column=i, padx=2, pady=2)
            ttk.Entry(
                self.marco_x0, textvariable=vx, width=7,
                justify="center"
            ).grid(row=0, column=i, padx=2, pady=2)

        ttk.Label(
            self.marco_matriz,
            text="Filas = ecuaciones  |  Columnas = incógnitas",
            style="CardSubtitle.TLabel"
        ).grid(row=n, column=0, columnspan=n, sticky="w", pady=(5, 0))

    def _cambiar_dimension(self, _event=None):
        try:
            n = int(self.dimension.get())
        except (ValueError, tk.TclError):
            n = 3
        self.dimension.set(max(2, min(6, n)))
        self._crear_campos()

    def _leer_entradas(self):
        A = [[v.get().strip() for v in fila] for fila in self.matriz_vars]
        b = [v.get().strip() for v in self.vector_vars]
        x0 = [v.get().strip() for v in self.inicial_vars]
        return A, b, x0

    def resolver(self):
        A, b, x0 = self._leer_entradas()
        try:
            resultado = resolver_iterativos(
                A, b, x0,
                tolerancia=self.tolerancia.get(),
                max_iteraciones=self.max_iteraciones.get(),
                metodo=self.metodo.get()
            )
        except (ValueError, OverflowError) as error:
            messagebox.showerror(
                "No se pudo resolver el sistema",
                str(error),
                parent=self.app.root
            )
            return

        self.ultimo_resultado = resultado
        self._mostrar_resultado(resultado)

    @staticmethod
    def _formato(valor):
        if valor is None:
            return "—"
        return f"{valor:.10g}"

    def _limpiar_resultado(self):
        for widget in self.panel_resultado.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self):
        self._limpiar_resultado()
        ttk.Label(
            self.panel_resultado,
            text="Resolver Ax = b mediante aproximaciones sucesivas",
            style="SectionTitle.TLabel",
            wraplength=560
        ).pack(anchor="w", pady=(12, 10))
        ttk.Label(
            self.panel_resultado,
            text=(
                "1. Ingrese los coeficientes de A.\n"
                "2. Complete el vector b y la aproximación inicial x⁽⁰⁾.\n"
                "3. Seleccione Jacobi o Gauss-Seidel.\n"
                "4. Indique la tolerancia y el máximo de iteraciones.\n"
                "5. Presione «Resolver sistema».\n\n"
                "El ejemplo inicial corresponde a una matriz con "
                "dominancia diagonal estricta y solución (1, 2, -1)."
            ),
            style="AnalysisBody.TLabel",
            justify="left",
            wraplength=560
        ).pack(anchor="w")

        ttk.Label(
            self.panel_resultado,
            text="Criterio de parada",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(24, 6))
        ttk.Label(
            self.panel_resultado,
            text="max |xᵢ⁽ᵏ⁺¹⁾ − xᵢ⁽ᵏ⁾| ≤ tolerancia",
            style="Operation.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            self.panel_resultado,
            text="Jacobi usa los valores anteriores; Gauss-Seidel usa los nuevos tan pronto se calculan.",
            style="CardSubtitle.TLabel",
            wraplength=560
        ).pack(anchor="w", pady=(10, 0))

    def _mostrar_resultado(self, datos):
        self._limpiar_resultado()

        ttk.Label(
            self.panel_resultado,
            text=f"Resultado: {datos['metodo']}",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(4, 8))

        estilo_estado = "Status.TLabel" if datos["convergio"] else "StatusBad.TLabel"
        ttk.Label(
            self.panel_resultado,
            text=datos["estado"],
            style=estilo_estado,
            padding=9,
            wraplength=560
        ).pack(fill="x", pady=(0, 10))

        resumen = ttk.Frame(self.panel_resultado, style="Card.TFrame")
        resumen.pack(fill="x", pady=(0, 10))
        columnas = (
            ("Aproximación final", "[" + ", ".join(
                self._formato(v) for v in datos["solucion"]
            ) + "]"),
            ("Iteraciones realizadas", str(datos["iteraciones"])),
            ("Error máximo final", self._formato(datos["error"])),
            ("Residuo ||Ax-b||∞", self._formato(datos["residuo"])),
            ("Tolerancia", self._formato(datos["tolerancia"])),
        )
        for etiqueta, valor in columnas:
            fila = ttk.Frame(resumen, style="Card.TFrame")
            fila.pack(fill="x", pady=2)
            ttk.Label(
                fila, text=etiqueta, style="CardSubtitle.TLabel"
            ).pack(side="left")
            ttk.Label(
                fila, text=valor, style="MetricValue.TLabel"
            ).pack(side="right")

        ttk.Label(
            self.panel_resultado,
            text="Diagnóstico de convergencia",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(6, 4))
        ttk.Label(
            self.panel_resultado,
            text=datos["diagnostico"],
            style="AnalysisBody.TLabel",
            wraplength=560,
            justify="left"
        ).pack(anchor="w", pady=(0, 8))

        ttk.Label(
            self.panel_resultado,
            text="Historial de iteraciones",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(4, 6))

        contenedor = ttk.Frame(self.panel_resultado, style="Card.TFrame")
        contenedor.pack(fill="both", expand=True)

        columnas_tabla = ("k", "aproximacion", "error", "residuo")
        tabla = ttk.Treeview(
            contenedor, columns=columnas_tabla,
            show="headings", height=10
        )
        encabezados = {
            "k": "Iteración",
            "aproximacion": "Vector x⁽ᵏ⁾",
            "error": "Error máximo",
            "residuo": "Residuo ∞",
        }
        anchos = {"k": 70, "aproximacion": 245, "error": 115, "residuo": 115}
        for col in columnas_tabla:
            tabla.heading(col, text=encabezados[col])
            tabla.column(
                col, width=anchos[col],
                anchor="center", stretch=True
            )

        for paso in datos["historial"]:
            aproximacion = "[" + ", ".join(
                self._formato(v) for v in paso["aproximacion"]
            ) + "]"
            tabla.insert(
                "", "end",
                values=(
                    paso["iteracion"],
                    aproximacion,
                    self._formato(paso["error"]),
                    self._formato(paso["residuo"]),
                )
            )

        barra = ttk.Scrollbar(
            contenedor, orient="vertical", command=tabla.yview
        )
        tabla.configure(yscrollcommand=barra.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        ttk.Label(
            self.panel_resultado,
            text=(
                "El error máximo mide el cambio entre dos aproximaciones consecutivas. "
                "El residuo mide cuánto se aleja la aproximación de satisfacer Ax = b."
            ),
            style="CardSubtitle.TLabel",
            wraplength=560,
            justify="left"
        ).pack(anchor="w", pady=(8, 0))

    def restablecer(self):
        self.dimension.set(3)
        self.metodo.set("Jacobi")
        self.tolerancia.set("0.000001")
        self.max_iteraciones.set("100")
        self.matriz_vars = []
        self.vector_vars = []
        self.inicial_vars = []
        self._actualizar_descripcion()
        self._crear_campos()
        self.ultimo_resultado = None
        self._mostrar_inicio()

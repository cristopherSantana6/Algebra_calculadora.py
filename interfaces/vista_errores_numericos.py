"""
Se integra como una subvista dentro de VistaMetodosNumericos y utiliza
los cálculos puros implementados en algoritmos.errores_numericos.
"""

import math
import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from interfaces.componentes.tarjeta import Tarjeta
from algoritmos.errores_numericos import (
    calcular_errores,
    calcular_propagacion,
    simular_truncamiento_redondeo,
    analizar_inestabilidad,
    analizar_punto_flotante,
    obtener_tipos_errores,
)



class VistaErroresNumericos:
    """Vista de errores numéricos con cinco ejercicios seleccionables."""

    OPCIONES = (
        "1. Cálculo directo",
        "2. Propagación del error",
        "3. Truncamiento vs. redondeo",
        "4. Inestabilidad numérica",
        "5. Punto flotante y tipos de error",
    )

    CONFIGURACION = {
        OPCIONES[0]: (
            ("Valor verdadero (xv)", "verdadero", "100"),
            ("Valor aproximado (xa)", "aproximado", "98"),
        ),
        OPCIONES[1]: (
            ("Valor de x", "x", "1"),
            ("Perturbación (Δx)", "delta", "0.01"),
        ),
        OPCIONES[2]: (
            ("Incremento por iteración", "incremento", "0.1666666667"),
            ("Cantidad de iteraciones", "repeticiones", "12"),
            ("Cifras decimales", "decimales", "2"),
        ),
        OPCIONES[3]: (
            ("Valor positivo de x", "x_inestable", "100000000"),
        ),
        OPCIONES[4]: (),
    }

    def __init__(self, padre):
        """Inicializa la vista de Errores Numéricos.
        Prepara los controles y crea la interfaz."""
        self.padre = padre  # instancia de VistaMetodosNumericos
        self.app = padre.app
        self.marco = ttk.Frame(padre.marco)
        self.marco.grid(row=1, column=0, sticky="nsew")
        self.modo = tk.StringVar(value=self.OPCIONES[0])
        self.campos = {}
        self.canvas_grafica = None
        self._construir()

    def _construir(self):
        """Construye los paneles de entrada y resultados.
        Agrega navegación, desplazamiento y botones de acción."""
        self.marco.columnconfigure(0, weight=1, minsize=325)
        self.marco.columnconfigure(1, weight=2)
        self.marco.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.marco, "Errores Numéricos",
            "Elija una actividad e interprete el procedimiento."
        )
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        derecha = Tarjeta(
            self.marco, "Resultados y explicación",
            "Valores, fórmulas y comparación de aproximaciones."
        )
        derecha.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(izquierda, text="Actividad", style="SectionTitle.TLabel").pack(
            anchor="w", pady=(16, 6)
        )
        selector = ttk.Combobox(
            izquierda, textvariable=self.modo,
            values=self.OPCIONES, state="readonly"
        )
        selector.pack(fill="x")
        selector.bind("<<ComboboxSelected>>", self._cambiar_actividad)

        self.marco_campos = ttk.Frame(izquierda, style="Card.TFrame")

        # Área desplazable del formulario
        zona = ttk.Frame(izquierda, style="Card.TFrame")
        zona.pack(fill="both", expand=True, pady=(12, 0))

        canvas = tk.Canvas(
            zona,
            bg=self.app.WHITE,
            highlightthickness=0,
            bd=0
        )

        barra_vertical = ttk.Scrollbar(
            zona,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=barra_vertical.set)

        interior = ttk.Frame(canvas, style="Card.TFrame")
        ventana = canvas.create_window(
            (0, 0), window=interior, anchor="nw"
        )

        interior.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                ventana, width=event.width
            )
        )

        canvas.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")

        self.marco_campos = ttk.Frame(
            interior, style="Card.TFrame"
        )
        self.marco_campos.pack(fill="x", pady=(3, 8))

        ttk.Button(
            interior,
            text="Calcular / Analizar",
            style="Accent.TButton",
            command=self.calcular
        ).pack(fill="x", pady=(8, 6))

        ttk.Button(
            interior,
            text="Limpiar",
            style="Coral.TButton",
            command=self.limpiar
        ).pack(fill="x")


        self.panel_resultado = ttk.Frame(derecha, style="Card.TFrame")
        self.panel_resultado.pack(fill="both", expand=True, pady=(14, 0))
        self._crear_campos()
        self._mostrar_inicio()

    def _cambiar_actividad(self, _event=None):
        """Actualiza el formulario al seleccionar otra actividad.
        Limpia la visualización anterior."""
        self._crear_campos()
        self._mostrar_inicio()

    def _crear_campos(self):
        """Crea los campos correspondientes al ejercicio seleccionado.
        Muestra ejemplos y avisos según la actividad."""
        for widget in self.marco_campos.winfo_children():
            widget.destroy()
        self.campos = {}
        for etiqueta, clave, ejemplo in self.CONFIGURACION[self.modo.get()]:
            ttk.Label(
                self.marco_campos, text=etiqueta, style="CardSubtitle.TLabel"
            ).pack(anchor="w", pady=(7, 3))
            variable = tk.StringVar(value="")
            self.campos[clave] = variable
            ttk.Entry(self.marco_campos, textvariable=variable).pack(fill="x")
            ttk.Label(
                self.marco_campos, text=f"Ejemplo: {ejemplo}",
                style="CardSubtitle.TLabel"
            ).pack(anchor="w", pady=(3, 5))

        if self.modo.get() == self.OPCIONES[1]:
            ttk.Label(
                self.marco_campos,
                text="Función del ejercicio: f(x) = sin(x) + x²",
                style="CardSubtitle.TLabel", wraplength=280
            ).pack(anchor="w", pady=(10, 4))
        if self.modo.get() == self.OPCIONES[4]:
            ttk.Label(
                self.marco_campos,
                text="Esta demostración utiliza ejemplos controlados; no requiere datos.",
                style="CardSubtitle.TLabel", wraplength=280
            ).pack(anchor="w", pady=8)

    def _limpiar_panel(self):
        """Elimina los elementos mostrados en el panel de resultados.
        Libera la referencia al lienzo de la gráfica anterior."""
        if self.canvas_grafica is not None:
            # Los widgets se eliminan al destruir el contenedor.
            self.canvas_grafica = None
        for widget in self.panel_resultado.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self):
        """Restablece el panel con las instrucciones iniciales.
        Invita a seleccionar una actividad e ingresar datos."""
        self._limpiar_panel()
        ttk.Label(
            self.panel_resultado,
            text="Seleccione la actividad e ingrese sus valores.",
            style="SectionTitle.TLabel", wraplength=520
        ).pack(anchor="w", pady=(10, 8))
        ttk.Label(
            self.panel_resultado,
            text="El programa mostrará las fórmulas utilizadas, los resultados "
                 "y una explicación. En la simulación también aparece una gráfica.",
            style="AnalysisBody.TLabel", wraplength=520, justify="left"
        ).pack(anchor="w")

    @staticmethod
    def _fmt(valor):
        """Convierte un resultado a texto para mostrarlo en pantalla.
        Controla valores indefinidos, booleanos y numéricos."""
        if valor is None:
            return "No definido"
        if isinstance(valor, bool):
            return str(valor)
        if isinstance(valor, (int, float)):
            return f"{valor:.12g}"
        return str(valor)


    def _mostrar(self, titulo, lineas, explicacion, figura=None):
        """Presenta el procedimiento y su explicación.
        Si existe una figura, la agrega al área desplazable."""

        self._limpiar_panel()

        ttk.Label(
            self.panel_resultado,
            text=titulo,
            style="SectionTitle.TLabel",
            wraplength=540
        ).pack(anchor="w", pady=(4, 10))

        # Contenedor principal desplazable
        contenedor = ttk.Frame(
            self.panel_resultado,
            style="Card.TFrame"
        )
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            contenedor,
            bg=self.app.WHITE,
            highlightthickness=0,
            bd=0
        )

        scrollbar = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=canvas.yview
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        interior = ttk.Frame(canvas, style="Card.TFrame")

        ventana = canvas.create_window(
            (0, 0), window=interior, anchor="nw"
        )

        interior.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                ventana, width=event.width
            )
        )

        canvas.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        # Área de procedimiento
        area = ttk.Frame(
            interior, style="Card.TFrame"
        )
        area.pack(fill="x", pady=(0, 10))

        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)

        texto = tk.Text(
            area,
            font=("Consolas", 10),
            wrap="word",
            height=13,
            bg=self.app.SURFACE_ALT,
            fg=self.app.DARK,
            relief="flat",
            padx=12,
            pady=10
        )

        barra_texto = ttk.Scrollbar(
            area,
            orient="vertical",
            command=texto.yview
        )
        texto.configure(yscrollcommand=barra_texto.set)

        texto.grid(row=0, column=0, sticky="nsew")
        barra_texto.grid(row=0, column=1, sticky="ns")

        contenido = (
            "\n".join(lineas)
            + "\n\nEXPLICACIÓN\n"
            + explicacion
        )

        texto.insert("1.0", contenido)
        texto.configure(state="disabled")

        # Gráfica independiente debajo del procedimiento
        if figura is not None:
            contenedor_grafica = ttk.Frame(
                interior,
                style="Card.TFrame",
                height=300
            )
            contenedor_grafica.pack(
                fill="x", pady=(8, 12)
            )
            contenedor_grafica.pack_propagate(False)

            lienzo = FigureCanvasTkAgg(
                figura, master=contenedor_grafica
            )
            lienzo.draw()

            lienzo.get_tk_widget().pack(
                fill="both", expand=True
            )

            self.canvas_grafica = lienzo

    def calcular(self):
        """Ejecuta el cálculo de la actividad seleccionada.
        Presenta resultados y muestra errores de datos si ocurren."""
        opcion = self.modo.get()
        try:
            if opcion == self.OPCIONES[0]:
                r = calcular_errores(
                    self.campos["verdadero"].get(),
                    self.campos["aproximado"].get()
                )
                lineas = [
                    f"Valor verdadero: {self._fmt(r['valor_verdadero'])}",
                    f"Valor aproximado: {self._fmt(r['valor_aproximado'])}",
                    "Error absoluto = |xv - xa|",
                    f"  = {self._fmt(r['error_absoluto'])}",
                    "Error relativo = Error absoluto / |xv|",
                    f"  = {self._fmt(r['error_relativo'])}",
                    "Error porcentual = Error relativo × 100",
                    f"  = {self._fmt(r['error_porcentual'])} %"
                    if r["error_porcentual"] is not None else "  = No definido",
                ]
                self._mostrar("Cálculo directo de errores", lineas, r["explicacion"])

            elif opcion == self.OPCIONES[1]:
                r = calcular_propagacion(
                    self.campos["x"].get(), self.campos["delta"].get()
                )
                lineas = [
                    "f(x) = sin(x) + x²", "f'(x) = cos(x) + 2x",
                    f"x = {self._fmt(r['x'])}",
                    f"Δx = {self._fmt(r['delta_x'])}",
                    f"f(x) = {self._fmt(r['fx'])}",
                    f"f(x+Δx) = {self._fmt(r['fx_perturbada'])}",
                    f"Derivada analítica = {self._fmt(r['derivada_exacta'])}",
                    f"Derivada numérica = {self._fmt(r['derivada_numerica'])}",
                    "Δy aproximado = f'(x) × Δx",
                    f"  = {self._fmt(r['delta_y_aproximado'])}",
                    f"Δy por derivada numérica = {self._fmt(r['delta_y_numerico'])}",
                    "Δy real = f(x+Δx) - f(x)",
                    f"  = {self._fmt(r['delta_y_real'])}",
                    f"Diferencia absoluta (analítica) = {self._fmt(r['diferencia'])}",
                    f"Diferencia absoluta (numérica) = {self._fmt(r['diferencia_numerica'])}",
                ]
                self._mostrar("Propagación del error", lineas, r["explicacion"])

            elif opcion == self.OPCIONES[2]:
                r = simular_truncamiento_redondeo(
                    self.campos["incremento"].get(),
                    self.campos["repeticiones"].get(),
                    self.campos["decimales"].get()
                )
                lineas = [
                    f"Incremento original: {r['incremento']}",
                    f"Incremento truncado: {r['incremento_truncado']}",
                    f"Incremento redondeado: {r['incremento_redondeado']}",
                    f"Repeticiones: {r['repeticiones']}",
                    f"Referencia final: {self._fmt(r['referencia_final'])}",
                    f"Total truncado: {self._fmt(r['resultado_truncado'])}",
                    f"Total redondeado: {self._fmt(r['resultado_redondeado'])}",
                    f"Error truncamiento: {self._fmt(r['error_truncamiento'])}",
                    f"Error redondeo: {self._fmt(r['error_redondeo'])}",
                    "", "La gráfica compara los errores absolutos en cada iteración.",
                ]
                figura = self._grafica_simulacion(r["pasos"])
                self._mostrar("Truncamiento vs. redondeo", lineas, r["explicacion"], figura)

            elif opcion == self.OPCIONES[3]:
                r = analizar_inestabilidad(self.campos["x_inestable"].get())
                lineas = [
                    f"x = {self._fmt(r['x'])}",
                    f"Forma directa: {r['expresion_directa']}",
                    f"  Resultado = {self._fmt(r['resultado_directo'])}",
                    f"Forma estable: {r['expresion_estable']}",
                    f"  Resultado = {self._fmt(r['resultado_estable'])}",
                    f"Diferencia absoluta = {self._fmt(r['diferencia'])}",
                ]
                self._mostrar("Inestabilidad numérica", lineas, r["explicacion"])

            else:
                r = analizar_punto_flotante()
                lineas = [
                    f"0.1 + 0.2 = {repr(r['suma'])}",
                    f"0.1 + 0.2 == 0.3 → {r['comparacion']}",
                    f"Épsilon de máquina (float64): {r['epsilon']}",
                    f"Overflow controlado: {r['overflow']}",
                    f"Menor subnormal positivo: {r['minimo_positivo']}",
                    f"Underflow controlado: {r['underflow']}",
                    "", "TIPOS DE ERROR",
                ]
                for e in obtener_tipos_errores():
                    lineas.extend([
                        "", e["tipo"],
                        "Definición: " + e["definicion"],
                        "Ejemplo: " + e["ejemplo"],
                    ])
                self._mostrar("Punto flotante y tipos de error", lineas, r["explicacion"])

        except (ValueError, TypeError, OverflowError, ArithmeticError) as error:
            self._mostrar_inicio()
            messagebox.showerror("Datos inválidos", str(error), parent=self.app.root)

    @staticmethod
    def _grafica_simulacion(pasos):
        """Genera la gráfica de errores por iteración.
        Compara el truncamiento y el redondeo."""
        figura = Figure(figsize=(7, 3.2), dpi=95, facecolor="white")
        eje = figura.add_subplot(111)
        k = [p["iteracion"] for p in pasos]
        eje.plot(
            k, [p["error_truncamiento"] for p in pasos],
            "o-", color="#B4514B", label="Truncamiento"
        )
        eje.plot(
            k, [p["error_redondeo"] for p in pasos],
            "s-", color="#7057B5", label="Redondeo"
        )
        eje.set_title("Evolución del error absoluto")
        eje.set_xlabel("Iteración")
        eje.set_ylabel("Error absoluto")
        eje.grid(alpha=0.3)
        eje.legend(fontsize=8)
        figura.tight_layout()
        return figura

    def limpiar(self):
        """Vacía los campos de la actividad actual.
        Restablece el mensaje inicial de resultados."""
        for variable in self.campos.values():
            variable.set("")
        self._mostrar_inicio()


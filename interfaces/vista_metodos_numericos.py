"""
Integra los algoritmos con la interfaz gráfica Tkinter.
Primera funcionalidad: Método de Bisección.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from interfaces.componentes.tarjeta import Tarjeta
from algoritmos.biseccion import metodo_biseccion
from algoritmos.graficador import crear_grafica
from algoritmos.notacion_posicional import (
    descomponer_numero,
    mostrar_procedimiento
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from interfaces.vista_errores_numericos import VistaErroresNumericos


class VistaMetodosNumericos:
    """Vista de Métodos Numéricos integrada a la calculadora."""

    def __init__(self, app):
        """Inicializa las variables de las cuatro funcionalidades.
        Crea el contenedor de la vista y construye su interfaz.
        """
        self.app = app
        self.marco = app.nueva_vista()

        self.funcion = tk.StringVar(value="")
        self.limite_a = tk.StringVar(value="")
        self.limite_b = tk.StringVar(value="")
        self.tolerancia = tk.StringVar(value="")
        self.iteraciones = tk.StringVar(value="")
        self.ultimo_resultado = None

        # Variables para Notación Posicional
        self.numero_posicional = tk.StringVar(value="")
        self.base_posicional = tk.StringVar(value="10")

        self.funcion_grafica = tk.StringVar(value="")
        self.x_min_grafica = tk.StringVar(value="")
        self.x_max_grafica = tk.StringVar(value="")

        self.construir()

    def construir(self):
        """Organiza el encabezado y las pantallas del Programa 7.
        Agrega navegación, formularios y paneles de resultados.
        """

        self.marco.columnconfigure(0, weight=1)
        self.marco.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self.marco)
        encabezado.grid(
            row=0, column=0, sticky="ew", pady=(0, 12)
        )

        ttk.Label(
            encabezado,
            text="Métodos Numéricos",
            style="PageTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            encabezado,
            text="Programa 7 | Bisección, Graficador, Notación Posicional y Errores Numéricos",
            style="PageSubtitle.TLabel"
        ).pack(anchor="w")


        # Navegación entre las funcionalidades
        navegacion = ttk.Frame(encabezado)
        navegacion.pack(fill="x", pady=(12, 0))


        # Botones de navegación del Programa 7
        self.botones_modulos = {}

        opciones = [
            ("biseccion", "Método de Bisección"),
            ("graficador", "Graficador"),
            ("posicional", "Notación Posicional"),
            ("errores", "Errores Numéricos")
        ]

        for nombre, texto in opciones:
            boton = ttk.Button(
                navegacion,
                text=texto,
                style="Op.TButton",
                command=lambda n=nombre: self.cambiar_modulo(n)
            )

            boton.pack(side="left", padx=(0, 8))

            self.botones_modulos[nombre] = boton

        # Pantalla para Bisección y Graficador
        self.vista_biseccion = ttk.Frame(self.marco)
        self.vista_biseccion.grid(
            row=1, column=0, sticky="nsew"
        )

        # Pantalla independiente de Notación Posicional
        self.vista_posicional = ttk.Frame(self.marco)
        self.vista_posicional.grid(
            row=1, column=0, sticky="nsew"
        )

        # Vista independiente para el Graficador
        self.vista_graficador = ttk.Frame(self.marco)
        self.vista_graficador.grid(
            row=1, column=0, sticky="nsew"
        )

        # Conservamos el nombre cuerpo para no alterar
        # los componentes que ya funcionan.
        cuerpo = self.vista_biseccion

        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            cuerpo,
            "Método de Bisección",
            "Ingrese la función y los parámetros del intervalo."
        )
        izquierda.grid(
            row=0, column=0, sticky="nsew", padx=(0, 8)
        )

        derecha = Tarjeta(
            cuerpo,
            "Resultados y procedimiento",
            "Iteraciones, errores y comparación con SciPy."
        )
        derecha.grid(
            row=0, column=1, sticky="nsew", padx=(8, 0)
        )


        # Área desplazable para mostrar todos los campos y botones
        contenedor_entradas = ttk.Frame(
            izquierda, style="Card.TFrame"
        )
        contenedor_entradas.pack(
            fill="both", expand=True, pady=(8, 0)
        )

        canvas_entradas = tk.Canvas(
            contenedor_entradas,
            bg=self.app.WHITE,
            highlightthickness=0,
            bd=0
        )

        scrollbar = ttk.Scrollbar(
            contenedor_entradas,
            orient="vertical",
            command=canvas_entradas.yview
        )

        contenido_entradas = ttk.Frame(
            canvas_entradas, style="Card.TFrame"
        )

        ventana_canvas = canvas_entradas.create_window(
            (0, 0),
            window=contenido_entradas,
            anchor="nw"
        )

        canvas_entradas.configure(
            yscrollcommand=scrollbar.set
        )

        contenido_entradas.bind(
            "<Configure>",
            lambda event: canvas_entradas.configure(
                scrollregion=canvas_entradas.bbox("all")
            )
        )

        canvas_entradas.bind(
            "<Configure>",
            lambda event: canvas_entradas.itemconfigure(
                ventana_canvas,
                width=event.width
            )
        )

        canvas_entradas.pack(
            side="left", fill="both", expand=True
        )

        scrollbar.pack(
            side="right", fill="y"
        )

        # Permite desplazarse con la rueda del mouse
        def desplazar(event):
            """Desplaza verticalmente el formulario con la rueda del mouse."""
            canvas_entradas.yview_scroll(
                int(-event.delta / 120), "units"
            )

        canvas_entradas.bind(
            "<MouseWheel>", desplazar
        )

        contenido_entradas.bind(
            "<MouseWheel>", desplazar
        )

        # Construir los controles dentro del área desplazable
        self.construir_entradas(contenido_entradas)


        self.panel_resultado = ttk.Frame(
            derecha, style="Card.TFrame"
        )
        self.panel_resultado.pack(
            fill="both", expand=True, pady=(12, 0)
        )

        self.mostrar_inicio()
        self.construir_vista_posicional()
        self.construir_vista_graficador()

        # Programa 7: vista de Errores Numéricos
        self.errores_numericos = VistaErroresNumericos(self)
        self.vista_errores = self.errores_numericos.marco

        self.cambiar_modulo("biseccion")



    def agregar_campo(self, padre, etiqueta, variable):
        """Crea una etiqueta y su campo de entrada asociado.
        Devuelve el control para utilizarlo desde la interfaz.
        """

        ttk.Label(
            padre,
            text=etiqueta,
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(10, 3))

        entrada = ttk.Entry(
            padre,
            textvariable=variable
        )
        entrada.pack(fill="x")

        return entrada

    def construir_entradas(self, padre):
        """Construye los campos y botones del Método de Bisección."""

        self.agregar_campo(
            padre, "Función f(x)", self.funcion
        )

        ttk.Label(
            padre,
            text="Ejemplo: x**3 - 2*x - 5",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(3, 8))

        self.agregar_campo(
            padre, "Extremo inferior (a)", self.limite_a
        )

        self.agregar_campo(
            padre, "Extremo superior (b)", self.limite_b
        )

        self.agregar_campo(
            padre, "Tolerancia absoluta (E)", self.tolerancia
        )

        self.agregar_campo(
            padre, "Iteraciones máximas", self.iteraciones
        )

        ttk.Button(
            padre,
            text="Calcular raíz",
            style="Accent.TButton",
            command=self.calcular
        ).pack(fill="x", pady=(22, 6))

        ttk.Button(
            padre,
            text="Limpiar",
            style="Coral.TButton",
            command=self.limpiar
        ).pack(fill="x")

        ttk.Button(
            padre,
            text="Graficar última raíz",
            style="Op.TButton",
            command=self.graficar_raiz
        ).pack(fill="x")


    def limpiar_panel(self):
        """Elimina los controles del panel de resultados de Bisección."""

        for widget in self.panel_resultado.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        """Muestra las instrucciones iniciales del Método de Bisección."""

        self.limpiar_panel()

        ttk.Label(
            self.panel_resultado,
            text="Encontrar una raíz aproximada",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(10, 8))

        instrucciones = (
            "El Método de Bisección permite aproximar "
            "una raíz dentro de un intervalo [a, b].\n\n"
            "1. Ingrese una función continua.\n"
            "2. Establezca los extremos a y b.\n"
            "3. Indique una tolerancia positiva.\n"
            "4. Presione Calcular raíz.\n\n"
            "El programa mostrará el procedimiento "
            "y los errores de cada iteración."
        )

        ttk.Label(
            self.panel_resultado,
            text=instrucciones,
            style="AnalysisBody.TLabel",
            justify="left",
            wraplength=470
        ).pack(anchor="w")

    def calcular(self):
        """Recoge los parámetros y ejecuta el Método de Bisección.
        Muestra los resultados o informa de datos inválidos.
        """

        try:
            resultado = metodo_biseccion(
                self.funcion.get(),
                self.limite_a.get(),
                self.limite_b.get(),
                self.tolerancia.get(),
                self.iteraciones.get()
            )

        except (ValueError, OverflowError) as error:
            messagebox.showerror(
                "Datos inválidos",
                str(error),
                parent=self.app.root
            )
            return

        self.ultimo_resultado = resultado
        self.mostrar_resultado(resultado)

    @staticmethod
    def formato(numero):
        """Presenta los valores numéricos con un formato legible.
        Representa los valores ausentes mediante un guion.
        """

        if numero is None:
            return "—"

        return f"{numero:.10g}"

    def mostrar_resultado(self, datos):
        """Muestra la raíz aproximada y el resumen del cálculo.
        Construye la tabla desplazable con las iteraciones.
        """

        self.limpiar_panel()

        ttk.Label(
            self.panel_resultado,
            text="Resultado del Método de Bisección",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(5, 10))

        resumen = ttk.Frame(
            self.panel_resultado,
            style="Card.TFrame"
        )
        resumen.pack(fill="x")

        informacion = [
            ("Raíz aproximada", self.formato(datos["raiz"])),
            ("f(xr)", self.formato(datos["valor_funcion"])),
            ("Cota del error", self.formato(datos["error"])),
            ("Iteraciones realizadas", str(datos["iteraciones_realizadas"])),
            ("Iteraciones teóricas", str(datos["iteraciones_teoricas"])),
            ("Referencia SciPy", self.formato(datos["comparacion_scipy"])),
            ("Diferencia absoluta", self.formato(datos["diferencia_scipy"]))
        ]

        for etiqueta, valor in informacion:
            fila = ttk.Frame(
                resumen, style="Card.TFrame"
            )
            fila.pack(fill="x", pady=2)

            ttk.Label(
                fila,
                text=etiqueta,
                style="CardSubtitle.TLabel"
            ).pack(side="left")

            ttk.Label(
                fila,
                text=valor,
                style="MetricValue.TLabel"
            ).pack(side="right")

        ttk.Label(
            self.panel_resultado,
            text=datos["estado"],
            style=(
                "StatusBad.TLabel"
                if "sin garantizar" in datos["estado"].lower()
                or "impide" in datos["estado"].lower()
                else "Status.TLabel"
            ),
            padding=8,
            wraplength=490
        ).pack(fill="x", pady=(12, 10))

        ttk.Label(
            self.panel_resultado,
            text="Tabla de iteraciones",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(5, 8))

        contenedor = ttk.Frame(
            self.panel_resultado,
            style="Card.TFrame"
        )
        contenedor.pack(fill="both", expand=True)

        columnas = (
            "k", "a", "b", "xr",
            "fa", "fb", "fr", "eb", "er"
        )

        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=9
        )

        encabezados = {
            "k": "k",
            "a": "a",
            "b": "b",
            "xr": "xr",
            "fa": "f(a)",
            "fb": "f(b)",
            "fr": "f(xr)",
            "eb": "Eb",
            "er": "Error relativo"
        }

        for columna in columnas:
            tabla.heading(
                columna,
                text=encabezados[columna]
            )

            # Anchos adaptados al contenido de cada columna
            anchos = {
                "k": 40,
                "a": 85,
                "b": 85,
                "xr": 100,
                "fa": 100,
                "fb": 100,
                "fr": 110,
                "eb": 95,
                "er": 115
            }

            tabla.column(
                columna,
                width=anchos[columna],
                minwidth=50 if columna != "k" else 35,
                anchor="center",
                stretch=True
            )

        if not datos["tabla"]:
            tabla.insert(
                "",
                "end",
                values=(
                    "—", "—", "—",
                    self.formato(datos["raiz"]),
                    "—", "—",
                    self.formato(datos["valor_funcion"]),
                    self.formato(datos["error"]),
                    "—"
                )
            )

        for paso in datos["tabla"]:
            tabla.insert(
                "",
                "end",
                values=(
                    paso["k"],
                    self.formato(paso["a"]),
                    self.formato(paso["b"]),
                    self.formato(paso["xr"]),
                    self.formato(paso["fa"]),
                    self.formato(paso["fb"]),
                    self.formato(paso["fr"]),
                    self.formato(paso["eb"]),
                    self.formato(paso["error_relativo"])
                )
            )

        scroll_y = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=tabla.yview
        )

        scroll_x = ttk.Scrollbar(
            contenedor,
            orient="horizontal",
            command=tabla.xview
        )

        tabla.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        tabla.grid(
            row=0, column=0, sticky="nsew"
        )
        scroll_y.grid(
            row=0, column=1, sticky="ns"
        )
        scroll_x.grid(
            row=1, column=0, sticky="ew"
        )

        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        ttk.Label(
            self.panel_resultado,
            text=(
                "La tabla utiliza los extremos antes de "
                "actualizar cada intervalo. "
                "Eb = (b-a)/2. El error relativo es "
                "— cuando no está definido."
            ),
            style="CardSubtitle.TLabel",
            wraplength=500,
            justify="left"
        ).pack(anchor="w", pady=(8, 0))

    def limpiar(self):
        """Vacía los campos de Bisección y borra el resultado guardado."""

        # Vaciar los campos del formulario
        self.funcion.set("")
        self.limite_a.set("")
        self.limite_b.set("")
        self.tolerancia.set("")
        self.iteraciones.set("")

        # Eliminar el resultado almacenado
        self.ultimo_resultado = None

        # Restablecer el panel de resultados
        self.mostrar_inicio()


    def graficar_funcion(self):
        """Grafica la función ingresada usando sus límites actuales.
        Informa si la función o el intervalo no son válidos.
        """

        try:
            figura, datos = crear_grafica(
                self.funcion.get(),
                self.limite_a.get(),
                self.limite_b.get()
            )

            self.mostrar_grafica(
                figura,
                datos,
                "Gráfica de la función"
            )

        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror(
                "Error al graficar",
                str(error),
                parent=self.app.root
            )

    def graficar_raiz(self):
        """Dibuja la última raíz obtenida mediante Bisección.
        Utiliza la función y el intervalo del cálculo guardado.
        """

        if self.ultimo_resultado is None:
            messagebox.showwarning(
                "Sin resultado",
                "Primero debe calcular una raíz con Bisección.",
                parent=self.app.root
            )
            return

        resultado = self.ultimo_resultado

        if resultado["raiz"] is None:
            messagebox.showwarning(
                "Sin raíz",
                "No existe una raíz calculada para graficar.",
                parent=self.app.root
            )
            return

        try:
            a, b = resultado["intervalo_inicial"]

            figura, datos = crear_grafica(
                resultado["funcion"],
                a,
                b,
                raiz=resultado["raiz"],
                intervalo_raiz=(a, b)
            )

            self.mostrar_grafica(
                figura,
                datos,
                "Raíz aproximada por Bisección"
            )

        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror(
                "Error al graficar",
                str(error),
                parent=self.app.root
            )

    def mostrar_grafica(self, figura, datos, titulo):
        """Inserta una figura de Matplotlib en el panel de resultados.
        Muestra también la función y los puntos válidos.
        """

        self.limpiar_panel()

        ttk.Label(
            self.panel_resultado,
            text=titulo,
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(5, 10))

        ttk.Label(
            self.panel_resultado,
            text=(
                f"Función: {datos['funcion']}  |  "
                f"Intervalo: [{datos['x_min']}, {datos['x_max']}]"
            ),
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        contenedor = ttk.Frame(
            self.panel_resultado,
            style="Card.TFrame"
        )
        contenedor.pack(fill="both", expand=True)

        canvas = FigureCanvasTkAgg(
            figura,
            master=contenedor
        )

        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # Conservamos la referencia al lienzo.
        self.canvas_grafica = canvas

        ttk.Label(
            self.panel_resultado,
            text=(
                f"Puntos válidos: {datos['puntos_validos']} "
                f"de {datos['puntos_totales']}"
            ),
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(8, 0))

        ttk.Button(
            self.panel_resultado,
            text="Volver a resultados de Bisección",
            style="Op.TButton",
            command=self.volver_resultados
        ).pack(fill="x", pady=(12, 0))

    def volver_resultados(self):
        """Recupera el último resultado de Bisección, si existe.
        En caso contrario, muestra las instrucciones iniciales.
        """

        if self.ultimo_resultado is not None:
            self.mostrar_resultado(self.ultimo_resultado)
        else:
            self.mostrar_inicio()

    def cambiar_modulo(self, nombre):
        """Muestra la pantalla del módulo seleccionado.
        Resalta su botón y deja los demás con estilo normal.
        """

        vistas = {
            "biseccion": self.vista_biseccion,
            "graficador": self.vista_graficador,
            "posicional": self.vista_posicional,
            "errores": self.vista_errores
        }

        # Mostrar la pantalla seleccionada
        vistas[nombre].tkraise()

        # Resaltar únicamente el botón activo
        for clave, boton in self.botones_modulos.items():
            if clave == nombre:
                boton.configure(style="Accent.TButton")
            else:
                boton.configure(style="Op.TButton")

    def construir_vista_posicional(self):
        """Crea el formulario y los resultados de Notación Posicional.
        Permite seleccionar base 10 o base 2.
        """

        self.vista_posicional.columnconfigure(0, weight=1)
        self.vista_posicional.columnconfigure(1, weight=2)
        self.vista_posicional.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.vista_posicional,
            "Notación Posicional",
            "Conversión de números enteros entre base 10 y base 2."
        )

        izquierda.grid(
            row=0, column=0,
            sticky="nsew", padx=(0, 8)
        )

        derecha = Tarjeta(
            self.vista_posicional,
            "Resultado y procedimiento",
            "Descomposición por potencias y equivalencia entre bases."
        )

        derecha.grid(
            row=0, column=1,
            sticky="nsew", padx=(8, 0)
        )

        # Selección de la base de origen
        ttk.Label(
            izquierda,
            text="Seleccione la base de origen",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(20, 10))

        opciones = ttk.Frame(
            izquierda, style="Card.TFrame"
        )
        opciones.pack(fill="x")

        ttk.Radiobutton(
            opciones,
            text="Base 10 (Decimal)",
            variable=self.base_posicional,
            value="10"
        ).pack(anchor="w", pady=5)

        ttk.Radiobutton(
            opciones,
            text="Base 2 (Binario)",
            variable=self.base_posicional,
            value="2"
        ).pack(anchor="w", pady=5)

        # Entrada del número
        ttk.Label(
            izquierda,
            text="Número entero",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(22, 5))

        self.entrada_posicional = ttk.Entry(
            izquierda,
            textvariable=self.numero_posicional,
            font=("Segoe UI", 12)
        )

        self.entrada_posicional.pack(fill="x")

        ttk.Label(
            izquierda,
            text="Ejemplos: 84506 en base 10 o 11110011 en base 2.",
            style="CardSubtitle.TLabel",
            wraplength=320
        ).pack(anchor="w", pady=(8, 18))

        # Botón Convertir
        ttk.Button(
            izquierda,
            text="Convertir número",
            style="Accent.TButton",
            command=self.convertir_posicional
        ).pack(fill="x", pady=(8, 6))

        # Botón Limpiar
        ttk.Button(
            izquierda,
            text="Limpiar",
            style="Coral.TButton",
            command=self.limpiar_posicional
        ).pack(fill="x")

        # Panel de resultados
        self.panel_posicional = ttk.Frame(
            derecha,
            style="Card.TFrame"
        )

        self.panel_posicional.pack(
            fill="both", expand=True, pady=(12, 0)
        )

        self.mostrar_inicio_posicional()

    def limpiar_panel_posicional(self):
        """Elimina el contenido anterior de Notación Posicional."""

        for widget in self.panel_posicional.winfo_children():
            widget.destroy()

    def mostrar_inicio_posicional(self):
        """Muestra las indicaciones para convertir entre bases."""

        self.limpiar_panel_posicional()

        ttk.Label(
            self.panel_posicional,
            text="Conversión entre bases",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(10, 12))

        texto = (
            "La notación posicional representa un número "
            "mediante dígitos multiplicados por potencias "
            "de una base.\n\n"
            "1. Seleccione base 10 o base 2.\n"
            "2. Ingrese un número entero.\n"
            "3. Presione Convertir número.\n\n"
            "Se mostrará la descomposición por potencias, "
            "las operaciones y el número equivalente "
            "en la otra base."
        )

        ttk.Label(
            self.panel_posicional,
            text=texto,
            style="AnalysisBody.TLabel",
            wraplength=540,
            justify="left"
        ).pack(anchor="w")

    def convertir_posicional(self):
        """Valida el número y calcula su conversión de base.
        Muestra el procedimiento o un mensaje de error.
        """

        numero = self.numero_posicional.get().strip()
        base = int(self.base_posicional.get())

        try:
            datos = descomponer_numero(
                numero, base
            )

            procedimiento = mostrar_procedimiento(datos)


        except ValueError as error:

            # Eliminar el resultado anterior si la entrada es inválida

            self.mostrar_inicio_posicional()

            messagebox.showerror(
                "Número inválido",
                str(error),
                parent=self.app.root

            )

            self.entrada_posicional.focus_set()
            return

        self.mostrar_resultado_posicional(
            datos, procedimiento
        )

    def mostrar_resultado_posicional(self, datos, procedimiento):
        """Muestra la equivalencia decimal-binaria y el procedimiento.
        Presenta los pasos en un área de texto desplazable.
        """

        self.limpiar_panel_posicional()

        ttk.Label(
            self.panel_posicional,
            text="Conversión realizada correctamente",
            style="Status.TLabel",
            padding=10,
            wraplength=520
        ).pack(fill="x", pady=(0, 12))

        # Resumen de la conversión
        resumen = ttk.Frame(
            self.panel_posicional,
            style="Card.TFrame"
        )
        resumen.pack(fill="x", pady=(0, 12))

        informacion = [
            ("Base de origen", str(datos["base_origen"])),
            ("Base de destino", str(datos["base_destino"])),
            ("Número decimal", datos["numero_decimal"]),
            ("Número binario", datos["numero_binario"])
        ]

        for etiqueta, valor in informacion:
            fila = ttk.Frame(
                resumen,
                style="Card.TFrame"
            )
            fila.pack(fill="x", pady=4)

            ttk.Label(
                fila,
                text=etiqueta,
                style="CardSubtitle.TLabel"
            ).pack(side="left")

            ttk.Label(
                fila,
                text=valor,
                style="MetricValue.TLabel"
            ).pack(side="right")

        ttk.Label(
            self.panel_posicional,
            text="Procedimiento paso a paso",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(10, 8))

        # Área desplazable para números largos
        contenedor = ttk.Frame(
            self.panel_posicional,
            style="Card.TFrame"
        )
        contenedor.pack(fill="both", expand=True)

        barra_y = ttk.Scrollbar(
            contenedor,
            orient="vertical"
        )

        barra_x = ttk.Scrollbar(
            contenedor,
            orient="horizontal"
        )

        texto = tk.Text(
            contenedor,
            font=("Consolas", 11),
            bg=self.app.SURFACE_ALT,
            fg=self.app.DARK,
            relief="flat",
            wrap="none",
            padx=12,
            pady=12,
            height=12,
            yscrollcommand=barra_y.set,
            xscrollcommand=barra_x.set
        )

        barra_y.configure(command=texto.yview)
        barra_x.configure(command=texto.xview)

        texto.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")

        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        texto.insert("1.0", procedimiento)
        texto.configure(state="disabled")

    def limpiar_posicional(self):
        """Borra el número, restablece la base y limpia resultados."""

        self.numero_posicional.set("")
        self.base_posicional.set("10")
        self.mostrar_inicio_posicional()
        self.entrada_posicional.focus_set()




    def construir_vista_graficador(self):
        """Crea los campos, botones y panel del Graficador.
        Mantiene esta pantalla separada del Método de Bisección.
        """

        self.vista_graficador.columnconfigure(0, weight=1)
        self.vista_graficador.columnconfigure(1, weight=2)
        self.vista_graficador.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.vista_graficador,
            "Graficador de Funciones",
            "Ingrese una función y el intervalo que desea visualizar."
        )
        izquierda.grid(
            row=0, column=0, sticky="nsew", padx=(0, 8)
        )

        derecha = Tarjeta(
            self.vista_graficador,
            "Representación gráfica",
            "Visualización de funciones y restricciones de dominio."
        )
        derecha.grid(
            row=0, column=1, sticky="nsew", padx=(8, 0)
        )

        self.agregar_campo(
            izquierda, "Función f(x)", self.funcion_grafica
        )

        ttk.Label(
            izquierda,
            text="Ejemplo: sin(x), sqrt(x), log(x), 1/x",
            style="CardSubtitle.TLabel",
            wraplength=320
        ).pack(anchor="w", pady=(5, 12))

        self.agregar_campo(
            izquierda, "Límite inferior (x_min)",
            self.x_min_grafica
        )

        self.agregar_campo(
            izquierda, "Límite superior (x_max)",
            self.x_max_grafica
        )

        ttk.Button(
            izquierda,
            text="Graficar función",
            style="Accent.TButton",
            command=self.graficar_independiente
        ).pack(fill="x", pady=(22, 6))

        ttk.Button(
            izquierda,
            text="Limpiar",
            style="Coral.TButton",
            command=self.limpiar_graficador
        ).pack(fill="x")

        self.panel_graficador = ttk.Frame(
            derecha, style="Card.TFrame"
        )
        self.panel_graficador.pack(
            fill="both", expand=True, pady=(12, 0)
        )

        self.limpiar_graficador()

    def graficar_independiente(self):
        """Obtiene los datos de la función y genera su gráfica.
        La incrusta en la pantalla independiente del Graficador.
        """

        try:
            figura, datos = crear_grafica(
                self.funcion_grafica.get(),
                self.x_min_grafica.get(),
                self.x_max_grafica.get()
            )

        except (ValueError, TypeError, OverflowError) as error:
            messagebox.showerror(
                "Error al graficar",
                str(error),
                parent=self.app.root
            )
            return

        for widget in self.panel_graficador.winfo_children():
            widget.destroy()

        ttk.Label(
            self.panel_graficador,
            text=f"Función: {datos['funcion']}",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(5, 8))

        contenedor = ttk.Frame(
            self.panel_graficador, style="Card.TFrame"
        )
        contenedor.pack(fill="both", expand=True)

        canvas = FigureCanvasTkAgg(
            figura, master=contenedor
        )
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        self.canvas_graficador = canvas

        ttk.Label(
            self.panel_graficador,
            text=(
                f"Intervalo: [{datos['x_min']}, {datos['x_max']}]"
                f"  |  Puntos válidos: "
                f"{datos['puntos_validos']} de "
                f"{datos['puntos_totales']}"
            ),
            style="CardSubtitle.TLabel",
            wraplength=500
        ).pack(anchor="w", pady=(8, 0))

    def limpiar_graficador(self):
        """Vacía los campos del Graficador y elimina la figura anterior."""

        self.funcion_grafica.set("")
        self.x_min_grafica.set("")
        self.x_max_grafica.set("")

        if not hasattr(self, "panel_graficador"):
            return

        for widget in self.panel_graficador.winfo_children():
            widget.destroy()

        ttk.Label(
            self.panel_graficador,
            text="Aquí aparecerá la gráfica de la función.",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(20, 8))

        ttk.Label(
            self.panel_graficador,
            text=(
                "Ingrese una función y establezca sus límites. "
                "Puede graficar funciones polinomiales, "
                "racionales, trigonométricas, radicales "
                "y logarítmicas."
            ),
            style="AnalysisBody.TLabel",
            wraplength=480,
            justify="left"
        ).pack(anchor="w")


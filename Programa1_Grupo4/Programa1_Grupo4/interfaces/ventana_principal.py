"""Interfaz principal de Linear Algebra Studio.

La interfaz usa exclusivamente Tkinter/ttk, por lo que no requiere
librerías externas y conserva la restricción de Python estándar.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)
from interfaces.componentes.tarjeta import Tarjeta
from interfaces.ventana_proceso import VentanaProceso
from modelos.sistema_ecuaciones import SistemaEcuaciones
from utilidades.formato import formatear_numero, formatear_matriz_lineas
from utilidades.fracciones import leer_fraccion


class CalculadoraAlgebraLineal:
    """Controlador de la aplicación y sus vistas."""

    TEAL = "#2E7778"
    TEAL_DARK = "#1F5558"
    CORAL = "#E87B70"
    BACKGROUND = "#EEF3F1"
    WHITE = "#FFFFFF"
    DARK = "#22363B"
    MUTED = "#6C7B7E"
    GREEN = "#2D8A67"
    RED = "#B4514B"
    LIGHT_GREEN = "#E7F4ED"
    LIGHT_RED = "#F9E9E7"

    def __init__(self, root):
        self.root = root
        self.root.title("Estudio de Álgebra Lineal")
        self.root.geometry("1260x780")
        self.root.minsize(1050, 680)
        self.root.configure(bg=self.BACKGROUND)

        self.numero_ecuaciones = tk.IntVar(value=3)
        self.numero_variables = tk.IntVar(value=3)
        self.matriz_entries = []
        self.ultimo_resultado = None
        self.vista_actual = "entrada"

        self.configurar_estilos()
        self.construir_interfaz()
        self.generar_matriz()

    def configurar_estilos(self):
        estilo = ttk.Style(self.root)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("TFrame", background=self.BACKGROUND)
        estilo.configure("Card.TFrame", background=self.WHITE)
        estilo.configure("Matrix.TFrame", background="#F7F9FA")
        estilo.configure("Sidebar.TFrame", background="#24383C")
        estilo.configure("Sidebar.TLabel", background="#24383C", foreground="#DDE8E6")
        estilo.configure("SidebarTitle.TLabel", background="#24383C", foreground="#FFFFFF", font=("Segoe UI", 15, "bold"))
        estilo.configure("Top.TFrame", background="#F7F9F7")
        estilo.configure("PageTitle.TLabel", background=self.BACKGROUND, foreground=self.DARK, font=("Georgia", 25, "bold"))
        estilo.configure("PageSubtitle.TLabel", background=self.BACKGROUND, foreground=self.MUTED, font=("Segoe UI", 10))
        estilo.configure("CardTitle.TLabel", background=self.WHITE, foreground=self.DARK, font=("Segoe UI", 14, "bold"))
        estilo.configure("CardSubtitle.TLabel", background=self.WHITE, foreground=self.MUTED, font=("Segoe UI", 9))
        estilo.configure("SectionTitle.TLabel", background=self.WHITE, foreground=self.DARK, font=("Segoe UI", 12, "bold"))
        estilo.configure("Operation.TLabel", background=self.WHITE, foreground=self.TEAL_DARK, font=("Consolas", 11, "bold"))
        estilo.configure("MetricValue.TLabel", background=self.WHITE, foreground=self.DARK, font=("Segoe UI", 12, "bold"))
        estilo.configure("Status.TLabel", background=self.LIGHT_GREEN, foreground=self.GREEN, font=("Segoe UI", 11, "bold"))
        estilo.configure("StatusBad.TLabel", background=self.LIGHT_RED, foreground=self.RED, font=("Segoe UI", 11, "bold"))
        estilo.configure("Footer.TLabel", background=self.BACKGROUND, foreground=self.MUTED, font=("Segoe UI", 9))
        estilo.configure("Accent.TButton", background=self.TEAL, foreground="white", font=("Segoe UI", 10, "bold"), padding=(15, 9))
        estilo.map("Accent.TButton", background=[("active", self.TEAL_DARK)])
        estilo.configure("Coral.TButton", background=self.CORAL, foreground="white", font=("Segoe UI", 10, "bold"), padding=(15, 9))
        estilo.map("Coral.TButton", background=[("active", "#CF675E")])
        estilo.configure("Sidebar.TButton", background="#24383C", foreground="#DDE8E6", font=("Segoe UI", 10), padding=(14, 11), anchor="w", borderwidth=0)
        estilo.map("Sidebar.TButton", background=[("active", "#305055")], foreground=[("active", "#FFFFFF")])
        estilo.configure("Header.TLabel", background="#F7F9F7", foreground=self.DARK, font=("Georgia", 23, "bold"))
        estilo.configure("HeaderSub.TLabel", background="#F7F9F7", foreground=self.MUTED, font=("Segoe UI", 10))
        estilo.configure("TSpinbox", padding=5)
        estilo.configure("TEntry", padding=7)

    def construir_interfaz(self):
        self.contenedor = ttk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

        self.construir_sidebar()

        self.area = ttk.Frame(self.contenedor)
        self.area.pack(side="left", fill="both", expand=True)

        self.construir_header()

        self.contenido = ttk.Frame(self.area, padding=(24, 10, 24, 10))
        self.contenido.pack(fill="both", expand=True)

        self.construir_vista_entrada()
        self.construir_vista_proceso()
        self.construir_vista_resultados()
        self.mostrar_vista("entrada")

        ttk.Label(
            self.area,
            text="Programa 1 • Álgebra Lineal (MTM0120) • Grupo 4",
            style="Footer.TLabel",
        ).pack(fill="x", padx=24, pady=(0, 8))

    def construir_sidebar(self):
        self.sidebar = ttk.Frame(self.contenedor, width=235, style="Sidebar.TFrame", padding=(16, 20))
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ttk.Label(self.sidebar, text="ESTUDIO", style="Sidebar.TLabel", font=("Segoe UI", 9, "bold" )).pack(anchor="w", pady=(0, 2))
        ttk.Label(self.sidebar, text="Álgebra Lineal", style="SidebarTitle.TLabel").pack(anchor="w", pady=(0, 30))

        self.boton_entrada = ttk.Button(self.sidebar, text="▦   Entrada de Matriz", style="Sidebar.TButton", command=lambda: self.mostrar_vista("entrada"))
        self.boton_entrada.pack(fill="x", pady=3)

        self.boton_proceso = ttk.Button(self.sidebar, text="∑   Proceso Gaussiano", style="Sidebar.TButton", command=self.abrir_proceso)
        self.boton_proceso.pack(fill="x", pady=3)

        self.boton_resultados = ttk.Button(self.sidebar, text="✓   Análisis de Resultados", style="Sidebar.TButton", command=lambda: self.mostrar_vista("resultados"))
        self.boton_resultados.pack(fill="x", pady=3)

        ttk.Separator(self.sidebar).pack(fill="x", pady=22)

        ttk.Label(self.sidebar, text="PROGRAMA 1", style="Sidebar.TLabel", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Label(self.sidebar, text="Eliminación por Filas", style="Sidebar.TLabel").pack(anchor="w", pady=(4, 14))

        ttk.Button(self.sidebar, text="?   Información del grupo", style="Sidebar.TButton", command=self.mostrar_info).pack(fill="x", pady=3)

        ttk.Label(self.sidebar, text="\nUniversidad Americana\nFacultad de Ingeniería y Arquitectura", style="Sidebar.TLabel", justify="left").pack(side="bottom", anchor="w")

    def construir_header(self):
        header = ttk.Frame(self.area, padding=(24, 18), style="Top.TFrame")
        header.pack(fill="x")

        ttk.Label(header, text="Estudio de Álgebra Lineal", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Eliminación por Filas  •  Programa 1  •  Grupo 4", style="HeaderSub.TLabel").pack(anchor="w", pady=(2, 0))

    def nueva_vista(self):
        marco = ttk.Frame(self.contenido)
        marco.place(relx=0, rely=0, relwidth=1, relheight=1)
        return marco

    def construir_vista_entrada(self):
        self.vista_entrada = self.nueva_vista()
        self.vista_entrada.columnconfigure(0, weight=1)
        self.vista_entrada.columnconfigure(1, weight=1)
        self.vista_entrada.rowconfigure(1, weight=1)

        izquierda = ttk.Frame(self.vista_entrada)
        izquierda.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        izquierda.rowconfigure(1, weight=1)

        derecha = ttk.Frame(self.vista_entrada)
        derecha.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))
        derecha.rowconfigure(1, weight=1)

        tarjeta_config = Tarjeta(izquierda, "Entrada del Sistema [ A | b ]", "Configure las dimensiones y escriba los coeficientes.")
        tarjeta_config.pack(fill="x", pady=(0, 10))

        config = ttk.Frame(tarjeta_config, style="Card.TFrame")
        config.pack(fill="x", pady=(16, 0))

        ttk.Label(config, text="Ecuaciones (m)", style="CardSubtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(config, text="Variables (n)", style="CardSubtitle.TLabel").grid(row=0, column=2, sticky="w", padx=(25, 0))
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.numero_ecuaciones, width=7).grid(row=1, column=0, sticky="w", pady=(5, 0))
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.numero_variables, width=7).grid(row=1, column=2, sticky="w", padx=(25, 0), pady=(5, 0))
        ttk.Button(config, text="Generar matriz", style="Accent.TButton", command=self.generar_matriz).grid(row=1, column=4, padx=(25, 0), pady=(0, 0))

        self.tarjeta_matriz = Tarjeta(izquierda, "Matriz aumentada", "Los términos independientes se separan visualmente con |.")
        self.tarjeta_matriz.pack(fill="both", expand=True)
        self.marco_entries = ttk.Frame(self.tarjeta_matriz, style="Card.TFrame")
        self.marco_entries.pack(fill="both", expand=True, pady=(15, 0))

        ttk.Label(
            self.tarjeta_matriz,
            text="Enter reemplaza el 0 inicial y avanza al siguiente dato. "
                 "Acepta enteros, decimales o fracciones (ej.: 3/4, -5/2).",
            style="CardSubtitle.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        botones = ttk.Frame(self.tarjeta_matriz, style="Card.TFrame")
        botones.pack(fill="x", pady=(14, 0))

        self.boton_resolver = ttk.Button(
            botones,
            text="Resolver Sistema",
            style="Accent.TButton",
            command=self.resolver,
        )
        self.boton_resolver.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6),
        )

        ttk.Button(
            botones,
            text="Limpiar",
            style="Coral.TButton",
            command=self.limpiar,
        ).pack(
            side="right",
            fill="x",
            expand=True,
            padx=(6, 0),
        )

        self.tarjeta_resumen = Tarjeta(derecha, "Análisis y Proceso", "El resultado se organiza para que sea fácil de interpretar.")
        self.tarjeta_resumen.pack(fill="both", expand=True)

        self.resumen_contenido = ttk.Frame(self.tarjeta_resumen, style="Card.TFrame")
        self.resumen_contenido.pack(fill="both", expand=True, pady=(16, 0))

        self.construir_resumen_placeholder()

    def construir_resumen_placeholder(self):
        for widget in self.resumen_contenido.winfo_children():
            widget.destroy()
        ttk.Label(self.resumen_contenido, text="Todavía no hay un resultado", style="SectionTitle.TLabel").pack(anchor="w", pady=(30, 5))
        ttk.Label(self.resumen_contenido, text="Ingrese una matriz y presione «Resolver Sistema».", style="CardSubtitle.TLabel").pack(anchor="w")

    def construir_vista_proceso(self):
        self.vista_proceso = self.nueva_vista()
        tarjeta = Tarjeta(self.vista_proceso, "Proceso Gaussiano", "Vista general del proceso y acceso al recorrido paso a paso.")
        tarjeta.pack(fill="both", expand=True)

        marco = ttk.Frame(tarjeta, style="Card.TFrame")
        marco.pack(fill="both", expand=True, pady=(18, 0))
        marco.columnconfigure(0, weight=1)
        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(1, weight=1)

        self.proceso_titulo = ttk.Label(marco, text="Primero resuelva un sistema", style="SectionTitle.TLabel")
        self.proceso_titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.proceso_operacion = ttk.Label(marco, text="Aquí se mostrará la operación elemental aplicada.", style="Operation.TLabel", wraplength=900)
        self.proceso_operacion.grid(row=0, column=1, sticky="e", pady=(0, 12))

        matriz_box = ttk.Frame(marco, style="Matrix.TFrame", padding=20)
        matriz_box.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.proceso_texto = tk.Text(matriz_box, font=("Consolas", 12), bg="#F7F9FA", fg=self.DARK, relief="flat", state="disabled")
        self.proceso_texto.pack(fill="both", expand=True)

        ttk.Button(marco, text="Ver proceso paso a paso", style="Accent.TButton", command=self.abrir_proceso).grid(row=2, column=0, columnspan=2, pady=(14, 0))

    def construir_vista_resultados(self):
        self.vista_resultados = self.nueva_vista()
        self.vista_resultados.columnconfigure(0, weight=1)
        self.vista_resultados.columnconfigure(1, weight=1)
        self.vista_resultados.rowconfigure(1, weight=1)

        izquierda = Tarjeta(self.vista_resultados, "Resumen de la Solución", "Clasificación y variables obtenidas.")
        izquierda.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        derecha = Tarjeta(self.vista_resultados, "Verificación y Validación", "Comprobación automática de la solución en el sistema original.")
        derecha.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))

        self.resultado_resumen = ttk.Frame(izquierda, style="Card.TFrame")
        self.resultado_resumen.pack(fill="both", expand=True, pady=(18, 0))

        self.verificacion_resumen = ttk.Frame(derecha, style="Card.TFrame")
        self.verificacion_resumen.pack(fill="both", expand=True, pady=(18, 0))

        detalle = Tarjeta(self.vista_resultados, "Matriz Escalonada", "Resultado final del proceso de eliminación.")
        detalle.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0))
        self.matriz_final_texto = tk.Text(detalle, font=("Consolas", 11), bg="#F7F9FA", fg=self.DARK, relief="flat", state="disabled", height=8)
        self.matriz_final_texto.pack(fill="both", expand=True, pady=(16, 0))

        self.mostrar_resultado_placeholder()

    def mostrar_resultado_placeholder(self):
        for widget in self.resultado_resumen.winfo_children():
            widget.destroy()
        ttk.Label(self.resultado_resumen, text="Sin datos", style="SectionTitle.TLabel").pack(anchor="w", pady=30)

        for widget in self.verificacion_resumen.winfo_children():
            widget.destroy()
        ttk.Label(self.verificacion_resumen, text="Resuelva un sistema para verificarlo.", style="CardSubtitle.TLabel").pack(anchor="w", pady=30)

        self.actualizar_texto(self.matriz_final_texto, "No hay matriz escalonada disponible.")

    def mostrar_vista(self, nombre):
        vistas = {
            "entrada": self.vista_entrada,
            "proceso": self.vista_proceso,
            "resultados": self.vista_resultados,
        }
        for vista in vistas.values():
            vista.lower()
        vistas[nombre].lift()
        self.vista_actual = nombre

    def generar_matriz(self):
        try:
            ecuaciones = int(self.numero_ecuaciones.get())
            variables = int(self.numero_variables.get())
            if not 1 <= ecuaciones <= 8 or not 1 <= variables <= 8:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Seleccione entre 1 y 8 ecuaciones y entre 1 y 8 variables.")
            return

        for widget in self.marco_entries.winfo_children():
            widget.destroy()

        self.matriz_entries = []

        ttk.Label(self.marco_entries, text="", style="CardSubtitle.TLabel").grid(row=0, column=0, padx=5, pady=5)
        for j in range(variables):
            ttk.Label(self.marco_entries, text=f"x{j + 1}", style="SectionTitle.TLabel").grid(row=0, column=j + 1, padx=5, pady=5)
        ttk.Label(self.marco_entries, text="|", style="SectionTitle.TLabel").grid(row=0, column=variables + 1, padx=10)
        ttk.Label(self.marco_entries, text="b", style="SectionTitle.TLabel").grid(row=0, column=variables + 2, padx=5)

        for i in range(ecuaciones):
            ttk.Label(self.marco_entries, text=f"E{i + 1}", style="CardSubtitle.TLabel").grid(row=i + 1, column=0, padx=5, pady=7)
            fila_entries = []

            for j in range(variables):
                entrada = ttk.Entry(
                    self.marco_entries,
                    width=8,
                    justify="center",
                )
                entrada.insert(0, "0")
                entrada.grid(
                    row=i + 1,
                    column=j + 1,
                    padx=3,
                    pady=5,
                )

                # Si la casilla todavía contiene el 0 inicial, al recibir
                # el foco se selecciona para que el siguiente dato lo reemplace.
                entrada.bind("<FocusIn>", self.seleccionar_cero_inicial)

                # Enter avanza automáticamente a la siguiente casilla.
                entrada.bind(
                    "<Return>",
                    lambda event, campo=entrada: self.avanzar_campo(
                        campo
                    ),
                )

                fila_entries.append(entrada)

            ttk.Label(
                self.marco_entries,
                text="|",
                style="SectionTitle.TLabel",
            ).grid(
                row=i + 1,
                column=variables + 1,
                padx=10,
            )

            entrada_b = ttk.Entry(
                self.marco_entries,
                width=8,
                justify="center",
            )
            entrada_b.insert(0, "0")
            entrada_b.grid(
                row=i + 1,
                column=variables + 2,
                padx=3,
                pady=5,
            )

            entrada_b.bind("<FocusIn>", self.seleccionar_cero_inicial)
            entrada_b.bind(
                "<Return>",
                lambda event, campo=entrada_b: self.avanzar_campo(
                    campo
                ),
            )

            fila_entries.append(entrada_b)
            self.matriz_entries.append(fila_entries)

        self.construir_resumen_placeholder()
        self.mostrar_resultado_placeholder()
        self.proceso_titulo.config(text="Primero resuelva un sistema")
        self.proceso_operacion.config(text="Aquí se mostrará la operación elemental aplicada.")
        self.actualizar_texto(self.proceso_texto, "No hay proceso disponible.")

        self.mostrar_vista("entrada")

    def seleccionar_cero_inicial(self, event):
        """
        Selecciona automáticamente el 0 inicial de una casilla.

        Así el usuario puede escribir directamente un número o una
        fracción sin tener que borrar primero el valor 0.
        """
        entrada = event.widget

        if entrada.get() == "0":
            entrada.select_range(0, tk.END)

    def avanzar_campo(self, campo_actual):
        """
        Mueve el foco al siguiente dato de la matriz al presionar Enter.

        Cuando se llega al último dato, el foco pasa al botón Resolver
        para que el usuario pueda continuar inmediatamente.
        """
        entradas = [
            entrada
            for fila in self.matriz_entries
            for entrada in fila
        ]

        try:
            indice = entradas.index(campo_actual)
        except ValueError:
            return "break"

        if indice + 1 < len(entradas):
            siguiente = entradas[indice + 1]
            siguiente.focus_set()

            if siguiente.get() == "0":
                siguiente.select_range(0, tk.END)
        else:
            self.boton_resolver.focus_set()

        return "break"

    def leer_matriz(self):
        try:
            matriz = []
            for fila_entries in self.matriz_entries:
                fila = []
                for entrada in fila_entries:
                    fila.append(leer_fraccion(entrada.get()))
                matriz.append(fila)
            return matriz
        except ValueError as error:
            messagebox.showerror(
                "Entrada inválida",
                f"{error}\n\nEjemplos válidos: 2, -3, 1/2, -5/8 o 0.25.",
            )
            return None

    def resolver(self):
        matriz_original = self.leer_matriz()
        if matriz_original is None:
            return

        numero_variables = int(self.numero_variables.get())
        sistema = SistemaEcuaciones(matriz_original, numero_variables)

        escalonada, pivotes, inconsistente, pasos = eliminacion_gaussiana(
            sistema.matriz_aumentada, sistema.numero_variables
        )
        clasificacion, libres = obtener_clasificacion(
            escalonada, numero_variables, pivotes, inconsistente
        )

        solucion = None
        verificacion = None
        if clasificacion == "unica":
            solucion = resolver_solucion_unica(escalonada, numero_variables, pivotes)
            verificacion = verificar_solucion(matriz_original, solucion)

        self.ultimo_resultado = {
            "matriz_original": matriz_original,
            "escalonada": escalonada,
            "pivotes": pivotes,
            "inconsistente": inconsistente,
            "clasificacion": clasificacion,
            "variables_libres": libres,
            "solucion": solucion,
            "verificacion": verificacion,
            "pasos": pasos,
        }

        self.actualizar_resumen()
        self.mostrar_vista("entrada")

    def actualizar_resumen(self):
        resultado = self.ultimo_resultado
        if not resultado:
            return

        for widget in self.resumen_contenido.winfo_children():
            widget.destroy()

        clasificacion = resultado["clasificacion"]
        if clasificacion == "unica":
            ttk.Label(self.resumen_contenido, text="✓", foreground=self.GREEN, background=self.LIGHT_GREEN, font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(10, 4))
            ttk.Label(self.resumen_contenido, text="Consistente Determinado", style="Status.TLabel", padding=8).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="Solución Única", style="SectionTitle.TLabel").pack(anchor="w", pady=(10, 14))
            for i, valor in enumerate(resultado["solucion"]):
                ttk.Label(self.resumen_contenido, text=f"x{i + 1} = {formatear_numero(valor)}", style="MetricValue.TLabel").pack(anchor="w", pady=3)
            ttk.Button(self.resumen_contenido, text="Ver proceso paso a paso", style="Accent.TButton", command=self.abrir_proceso).pack(anchor="w", pady=(20, 0))
        elif clasificacion == "infinita":
            ttk.Label(self.resumen_contenido, text="∞", foreground=self.TEAL, font=("Segoe UI", 28, "bold"), background=self.WHITE).pack(anchor="w", pady=(10, 4))
            ttk.Label(self.resumen_contenido, text="Consistente Indeterminado", style="Status.TLabel", padding=8).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="Infinitas Soluciones", style="SectionTitle.TLabel").pack(anchor="w", pady=(10, 14))
            libres_texto = ", ".join(f"x{i + 1}" for i in resultado["variables_libres"])
            ttk.Label(self.resumen_contenido, text=f"Variables libres: {libres_texto}", style="MetricValue.TLabel", wraplength=380).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="En este avance se identifican las variables libres; la parametrización completa queda como mejora futura.", style="CardSubtitle.TLabel", wraplength=390).pack(anchor="w", pady=(18, 0))
            ttk.Button(self.resumen_contenido, text="Ver proceso paso a paso", style="Accent.TButton", command=self.abrir_proceso).pack(anchor="w", pady=(20, 0))
        else:
            ttk.Label(self.resumen_contenido, text="!", foreground=self.RED, font=("Segoe UI", 28, "bold"), background=self.LIGHT_RED).pack(anchor="w", pady=(10, 4))
            ttk.Label(self.resumen_contenido, text="Sistema Inconsistente", style="StatusBad.TLabel", padding=8).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="Sin Solución", style="SectionTitle.TLabel").pack(anchor="w", pady=(10, 14))
            ttk.Label(self.resumen_contenido, text="Se detectó una fila equivalente a 0 ... 0 | c, con c ≠ 0.", style="CardSubtitle.TLabel", wraplength=390).pack(anchor="w")
            ttk.Button(self.resumen_contenido, text="Ver proceso paso a paso", style="Accent.TButton", command=self.abrir_proceso).pack(anchor="w", pady=(20, 0))

        for widget in self.verificacion_resumen.winfo_children():
            widget.destroy()

        if clasificacion == "unica":
            if resultado["verificacion"]:
                ttk.Label(self.verificacion_resumen, text="✓ Verificación automática correcta", style="Status.TLabel", padding=10).pack(anchor="w", pady=(10, 10))
                ttk.Label(self.verificacion_resumen, text="La solución satisface el sistema original.", style="CardSubtitle.TLabel", wraplength=400).pack(anchor="w")
            else:
                ttk.Label(self.verificacion_resumen, text="✗ Verificación incorrecta", style="StatusBad.TLabel", padding=10).pack(anchor="w", pady=(10, 10))
        elif clasificacion == "infinita":
            ttk.Label(self.verificacion_resumen, text="Información", style="Status.TLabel", padding=10).pack(anchor="w", pady=(10, 10))
            ttk.Label(self.verificacion_resumen, text="La verificación numérica automática se aplica en este avance cuando existe solución única.", style="CardSubtitle.TLabel", wraplength=400).pack(anchor="w")
        else:
            ttk.Label(self.verificacion_resumen, text="No aplica", style="StatusBad.TLabel", padding=10).pack(anchor="w", pady=(10, 10))
            ttk.Label(self.verificacion_resumen, text="Al ser inconsistente, no existe una solución numérica que sustituir.", style="CardSubtitle.TLabel", wraplength=400).pack(anchor="w")

        self.actualizar_texto(self.matriz_final_texto, "\n".join(formatear_matriz_lineas(resultado["escalonada"], int(self.numero_variables.get()))))
        self.proceso_titulo.config(text=f"{len(resultado['pasos'])} estados registrados")
        self.proceso_operacion.config(text=resultado["pasos"][-1]["operacion"])
        self.actualizar_texto(self.proceso_texto, "\n".join(formatear_matriz_lineas(resultado["pasos"][-1]["matriz"], int(self.numero_variables.get()))))

        self.mostrar_vista("resultados")

    def abrir_proceso(self):
        if not self.ultimo_resultado:
            messagebox.showinfo("Proceso Gaussiano", "Primero resuelva un sistema para poder mostrar el proceso paso a paso.")
            return
        VentanaProceso(self.root, self.ultimo_resultado["pasos"], int(self.numero_variables.get()))

    def actualizar_texto(self, widget, texto):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", texto)
        widget.config(state="disabled")

    def limpiar(self):
        for fila in self.matriz_entries:
            for entrada in fila:
                entrada.delete(0, "end")
                entrada.insert(0, "0")
        self.ultimo_resultado = None
        self.construir_resumen_placeholder()
        self.mostrar_resultado_placeholder()
        self.proceso_titulo.config(text="Primero resuelva un sistema")
        self.proceso_operacion.config(text="Aquí se mostrará la operación elemental aplicada.")
        self.actualizar_texto(self.proceso_texto, "No hay proceso disponible.")
        self.mostrar_vista("entrada")

    def mostrar_info(self):
        messagebox.showinfo(
            "Grupo 4",
            "Programa 1 - Calculadora de Álgebra Lineal\n\n"
            "Rafael Antonio Arauz Navarro\n"
            "Patricia del Carmen Oquist Talavera\n"
            "Cristopher Rafael Santana Ríos\n"
            "Blanca Alejandra Zeledón Abea\n\n"
            "Universidad Americana (UAM)\n"
            "Álgebra Lineal (MTM0120)",
        )


def iniciar_aplicacion():
    """Inicializa la aplicación."""
    root = tk.Tk()
    CalculadoraAlgebraLineal(root)
    root.mainloop()

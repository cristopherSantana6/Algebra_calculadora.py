"""Interfaz principal de Linear Algebra Studio.

La interfaz usa exclusivamente Tkinter/ttk, por lo que no requiere
librerías externas y conserva la restricción de Python estándar.
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
from pathlib import Path

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    gauss_jordan,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)
from algoritmos.matrices import (
    multiplicar_matrices,
    multiplicar_matriz_escalar,
    multiplicar_matriz_vector,
    restar_matrices,
    sumar_matrices,
)
from algoritmos.vectores import (
    analizar_dependencia_lineal,
    es_combinacion_lineal,
    multiplicar_escalar,
    restar_vectores,
    sumar_vectores,
)
from interfaces.componentes.tarjeta import Tarjeta
from interfaces.ventana_proceso import VentanaProceso
from modelos.sistema_ecuaciones import SistemaEcuaciones
from utilidades.formato import formatear_numero, formatear_matriz_lineas
from utilidades.fracciones import leer_fraccion


class CalculadoraAlgebraLineal:
    """Controlador de la aplicación y sus vistas."""

    # Paletas completas: cada tema conserva la misma estructura visual,
    # pero permite personalizar colores de fondo, tarjetas, botones y textos.
    TEMAS = {
        "Océano": {
            "primary": "#2E7778", "primary_dark": "#1F5558", "accent": "#E87B70",
            "background": "#EEF3F1", "surface": "#FFFFFF", "surface_alt": "#F7F9FA",
            "sidebar": "#24383C", "sidebar_active": "#2E7778", "sidebar_text": "#DDE8E6",
            "text": "#22363B", "muted": "#6C7B7E", "success": "#2D8A67",
            "danger": "#B4514B", "success_bg": "#E7F4ED", "danger_bg": "#F9E9E7",
            "header": "#F7F9F7"
        },
        "Esmeralda": {
            "primary": "#147D64", "primary_dark": "#0D5C4A", "accent": "#F08A5D",
            "background": "#EFF7F3", "surface": "#FFFFFF", "surface_alt": "#F4FAF7",
            "sidebar": "#183C36", "sidebar_active": "#147D64", "sidebar_text": "#DDEEE9",
            "text": "#203A35", "muted": "#68817A", "success": "#16805B",
            "danger": "#B94A48", "success_bg": "#E5F5ED", "danger_bg": "#FBEAEA",
            "header": "#F5FAF8"
        },
        "Atardecer": {
            "primary": "#B85C38", "primary_dark": "#8F4227", "accent": "#D9A441",
            "background": "#FBF4EC", "surface": "#FFFFFF", "surface_alt": "#FCF8F3",
            "sidebar": "#49352D", "sidebar_active": "#B85C38", "sidebar_text": "#F4E8DE",
            "text": "#3D302B", "muted": "#88756B", "success": "#4D8B61",
            "danger": "#B84B4B", "success_bg": "#EAF4EC", "danger_bg": "#FBEAEA",
            "header": "#FCF8F2"
        },
        "Violeta": {
            "primary": "#7057B5", "primary_dark": "#51408C", "accent": "#D978A7",
            "background": "#F5F1FA", "surface": "#FFFFFF", "surface_alt": "#F8F6FC",
            "sidebar": "#302842", "sidebar_active": "#7057B5", "sidebar_text": "#EAE3F4",
            "text": "#332C42", "muted": "#776E86", "success": "#4D916F",
            "danger": "#B64F69", "success_bg": "#E9F5EF", "danger_bg": "#FBEAF0",
            "header": "#F9F7FC"
        },
        "Azul profesional": {
            "primary": "#246BCE", "primary_dark": "#174C99", "accent": "#F28C28",
            "background": "#F1F5FB", "surface": "#FFFFFF", "surface_alt": "#F6F8FC",
            "sidebar": "#1D2E49", "sidebar_active": "#246BCE", "sidebar_text": "#DCE7F5",
            "text": "#26364A", "muted": "#6D7C90", "success": "#258A65",
            "danger": "#B54E4E", "success_bg": "#E7F5EE", "danger_bg": "#FBEAEA",
            "header": "#F6F8FC"
        },
        "Rosa moderno": {
            "primary": "#B44C7A", "primary_dark": "#853657", "accent": "#5D7BD5",
            "background": "#FAF1F6", "surface": "#FFFFFF", "surface_alt": "#FCF6F9",
            "sidebar": "#402A38", "sidebar_active": "#B44C7A", "sidebar_text": "#F2E2EB",
            "text": "#3B2D35", "muted": "#81727A", "success": "#3E8A68",
            "danger": "#B14B55", "success_bg": "#E8F5EE", "danger_bg": "#FBEAEC",
            "header": "#FCF7FA"
        },
    }

    # Valores iniciales; se reemplazan por la paleta guardada en disco.
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
        self.dimension_vector = tk.IntVar(value=3)
        self.cantidad_vectores = tk.IntVar(value=2)
        self.filas_a = tk.IntVar(value=2)
        self.columnas_a = tk.IntVar(value=2)
        self.filas_b = tk.IntVar(value=2)
        self.columnas_b = tk.IntVar(value=2)
        self.operacion_matriz = tk.StringVar(value="Suma (A + B)")
        self.propiedad_seleccionada = tk.StringVar(value="1. Conmutatividad: A + B = B + A")
        self.filas_propiedad = tk.IntVar(value=2)
        self.columnas_propiedad = tk.IntVar(value=2)
        self.escalar = tk.StringVar(value="2")
        self.escalar_r = tk.StringVar(value="2")
        self.escalar_s = tk.StringVar(value="3")
        self.escalar_c = tk.StringVar(value="2")
        self.vector_entries = []
        self.vector_b_entries = []
        self.generador_entries = []
        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.matriz_entries = []
        self.matriz_mv_entries = []
        self.vector_u_mv_entries = []
        self.vector_v_mv_entries = []
        self.prop_a_entries = []
        self.prop_b_entries = []
        self.prop_c_entries = []
        self.prop_u_entries = []
        self.prop_v_entries = []
        self.ultimo_resultado = None
        self.filas_mv = tk.IntVar(value=3)
        self.columnas_mv = tk.IntVar(value=3)
        self.vista_actual = "entrada"
        self.tema_actual = "Océano"
        self.botones_sidebar = {}
        self.entradas_navegables = []
        self.text_widgets = []
        self.cargar_tema_guardado()

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
        estilo.configure("Matrix.TFrame", background=self.SURFACE_ALT)
        estilo.configure("Sidebar.TFrame", background=self.SIDEBAR)
        estilo.configure("Sidebar.TLabel", background=self.SIDEBAR, foreground=self.SIDEBAR_TEXT)
        estilo.configure("SidebarTitle.TLabel", background=self.SIDEBAR, foreground=self.WHITE, font=("Segoe UI", 15, "bold"))
        estilo.configure("Top.TFrame", background=self.HEADER)
        estilo.configure("PageTitle.TLabel", background=self.BACKGROUND, foreground=self.DARK, font=("Georgia", 25, "bold"))
        estilo.configure("PageSubtitle.TLabel", background=self.BACKGROUND, foreground=self.MUTED, font=("Segoe UI", 10))
        estilo.configure("CardTitle.TLabel", background=self.WHITE, foreground=self.DARK, font=("Segoe UI", 14, "bold"))
        estilo.configure("CardSubtitle.TLabel", background=self.WHITE, foreground=self.MUTED, font=("Segoe UI", 9))
        # Subtítulos de ventanas que NO deben aparecer sobre una franja blanca.
        estilo.configure("ProcessSubtitle.TLabel", background=self.BACKGROUND, foreground=self.MUTED, font=("Segoe UI", 10))
        estilo.configure("SectionTitle.TLabel", background=self.WHITE, foreground=self.DARK, font=("Segoe UI", 12, "bold"))
        estilo.configure("Operation.TLabel", background=self.WHITE, foreground=self.TEAL_DARK, font=("Consolas", 11, "bold"))
        estilo.configure("MetricValue.TLabel", background=self.WHITE, foreground=self.DARK, font=("Segoe UI", 12, "bold"))
        estilo.configure("Status.TLabel", background=self.LIGHT_GREEN, foreground=self.GREEN, font=("Segoe UI", 11, "bold"))
        estilo.configure("StatusBad.TLabel", background=self.LIGHT_RED, foreground=self.RED, font=("Segoe UI", 11, "bold"))
        estilo.configure("SuccessIcon.TLabel", background=self.LIGHT_GREEN, foreground=self.GREEN, font=("Segoe UI", 28, "bold"))
        estilo.configure("InfoIcon.TLabel", background=self.WHITE, foreground=self.TEAL, font=("Segoe UI", 28, "bold"))
        estilo.configure("DangerIcon.TLabel", background=self.LIGHT_RED, foreground=self.RED, font=("Segoe UI", 28, "bold"))
        estilo.configure("Footer.TLabel", background=self.BACKGROUND, foreground=self.MUTED, font=("Segoe UI", 9))
        estilo.configure("Accent.TButton", background=self.TEAL, foreground="white", font=("Segoe UI", 10, "bold"), padding=(15, 9))
        estilo.map("Accent.TButton", background=[("active", self.TEAL_DARK), ("pressed", self.TEAL_DARK)])
        estilo.configure("Coral.TButton", background=self.CORAL, foreground="white", font=("Segoe UI", 10, "bold"), padding=(15, 9))
        estilo.map("Coral.TButton", background=[("active", self.CORAL_DARK), ("pressed", self.CORAL_DARK)])
        estilo.configure("Sidebar.TButton", background=self.SIDEBAR, foreground=self.SIDEBAR_TEXT, font=("Segoe UI", 10), padding=(14, 11), anchor="w", borderwidth=0)
        estilo.map("Sidebar.TButton", background=[("active", self.SIDEBAR_ACTIVE), ("pressed", self.SIDEBAR_ACTIVE)], foreground=[("active", self.WHITE), ("pressed", self.WHITE)])
        estilo.configure("SidebarActive.TButton", background=self.SIDEBAR_ACTIVE, foreground=self.WHITE, font=("Segoe UI", 10, "bold"), padding=(14, 11), anchor="w", borderwidth=0)
        estilo.map("SidebarActive.TButton", background=[("active", self.TEAL_DARK), ("pressed", self.TEAL_DARK)], foreground=[("active", self.WHITE)])
        estilo.configure("Header.TLabel", background=self.HEADER, foreground=self.DARK, font=("Georgia", 23, "bold"))
        estilo.configure("HeaderSub.TLabel", background=self.HEADER, foreground=self.MUTED, font=("Segoe UI", 10))
        estilo.configure("TSpinbox", padding=5)
        estilo.configure("TEntry", padding=7, fieldbackground=self.WHITE, foreground=self.DARK)
        self.root.configure(bg=self.BACKGROUND)

    def cargar_tema_guardado(self):
        """Carga el tema guardado; si no existe, usa Océano."""
        archivo = Path(__file__).resolve().parent.parent / "tema_interfaz.json"
        try:
            datos = json.loads(archivo.read_text(encoding="utf-8"))
            nombre = datos.get("tema", "Océano")
            if nombre in self.TEMAS:
                self.tema_actual = nombre
            elif isinstance(datos.get("colores"), dict):
                self.TEMAS["Personalizado"] = datos["colores"]
                self.tema_actual = "Personalizado"
        except (OSError, json.JSONDecodeError, TypeError):
            self.tema_actual = "Océano"
        self.aplicar_paleta(self.TEMAS[self.tema_actual])

    def aplicar_paleta(self, paleta):
        """Actualiza los colores centrales de toda la aplicación sin cambiar su estructura."""
        self.TEAL = paleta["primary"]
        self.TEAL_DARK = paleta["primary_dark"]
        self.CORAL = paleta["accent"]
        self.BACKGROUND = paleta["background"]
        self.WHITE = paleta["surface"]
        self.SURFACE_ALT = paleta["surface_alt"]
        self.SIDEBAR = paleta["sidebar"]
        self.SIDEBAR_ACTIVE = paleta["sidebar_active"]
        self.SIDEBAR_TEXT = paleta["sidebar_text"]
        self.DARK = paleta["text"]
        self.MUTED = paleta["muted"]
        self.GREEN = paleta["success"]
        self.RED = paleta["danger"]
        self.LIGHT_GREEN = paleta["success_bg"]
        self.LIGHT_RED = paleta["danger_bg"]
        self.HEADER = paleta["header"]
        self.CORAL_DARK = paleta.get("accent_dark", self.TEAL_DARK)

    def guardar_tema(self, nombre, paleta=None):
        """Guarda la preferencia para que se conserve al volver a abrir PyCharm."""
        archivo = Path(__file__).resolve().parent.parent / "tema_interfaz.json"
        datos = {"tema": nombre}
        if paleta is not None:
            datos["colores"] = paleta
        try:
            archivo.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    def aplicar_tema(self, nombre, paleta=None):
        """Aplica un tema, actualiza estilos y refresca colores de widgets existentes."""
        if paleta is None:
            paleta = self.TEMAS[nombre]
        self.aplicar_paleta(paleta)
        self.tema_actual = nombre
        self.configurar_estilos()
        self.root.configure(bg=self.BACKGROUND)
        for widget in self.text_widgets:
            try:
                widget.configure(bg=self.SURFACE_ALT, fg=self.DARK, insertbackground=self.DARK)
            except tk.TclError:
                pass
        self.marcar_sidebar_activa(self.vista_actual)
        self.guardar_tema(nombre, None if nombre in self.TEMAS and nombre != "Personalizado" else paleta)

    def abrir_personalizacion_colores(self):
        """Muestra paletas listas y permite crear una combinación personalizada."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Tema y colores")
        ventana.geometry("510x510")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.configure(bg=self.BACKGROUND)

        ttk.Label(ventana, text="Personaliza tu estudio", style="PageTitle.TLabel", font=("Georgia", 20, "bold")).pack(anchor="w", padx=24, pady=(22, 2))
        ttk.Label(ventana, text="Elige una combinación o crea tus propios colores.", style="PageSubtitle.TLabel").pack(anchor="w", padx=24, pady=(0, 15))

        marco = ttk.Frame(ventana, style="Card.TFrame", padding=16)
        marco.pack(fill="x", padx=24)
        ttk.Label(marco, text="Combinaciones prediseñadas", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 8))
        botones = ttk.Frame(marco, style="Card.TFrame")
        botones.pack(fill="x")
        for i, nombre in enumerate(self.TEMAS):
            if nombre == "Personalizado":
                continue
            ttk.Button(botones, text=nombre, style="Accent.TButton", command=lambda n=nombre: [self.aplicar_tema(n), ventana.destroy()]).grid(row=i//2, column=i%2, padx=4, pady=4, sticky="ew")
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)

        personalizado = ttk.Frame(ventana, style="Card.TFrame", padding=16)
        personalizado.pack(fill="x", padx=24, pady=14)
        ttk.Label(personalizado, text="Combinación personalizada", style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(personalizado, text="Puedes cambiar fondo, barra lateral, color principal y acento.", style="CardSubtitle.TLabel").pack(anchor="w", pady=(3, 10))

        base = self.TEMAS.get(self.tema_actual, self.TEMAS["Océano"]).copy()
        if self.tema_actual == "Personalizado" and hasattr(self, "paleta_personalizada"):
            base = self.paleta_personalizada.copy()
        elecciones = [("Fondo", "background"), ("Barra lateral", "sidebar"), ("Color principal", "primary"), ("Color de acento", "accent")]
        botones_color = ttk.Frame(personalizado, style="Card.TFrame")
        botones_color.pack(fill="x")
        for i, (texto, clave) in enumerate(elecciones):
            def elegir(c=clave):
                color = colorchooser.askcolor(title=f"Elegir {c}", initialcolor=base[c], parent=ventana)[1]
                if color:
                    base[c] = color
                    muestras[c].configure(bg=color)
            ttk.Button(botones_color, text=texto, command=elegir).grid(row=i, column=0, sticky="w", pady=3)
            muestras = locals().get("muestras", {})
            muestra = tk.Label(botones_color, width=5, bg=base[clave], relief="solid", bd=1)
            muestra.grid(row=i, column=1, padx=10)
            muestras[clave] = muestra
            # Guardamos la referencia en el closure mediante el diccionario del marco.
            botones_color.muestras = muestras
        # Reasignar el diccionario para que los closures lo encuentren.
        muestras = getattr(botones_color, "muestras", {})

        def guardar_personalizado():
            # Derivados para mantener contraste y coherencia visual.
            personalizado = base.copy()
            personalizado["primary_dark"] = base["sidebar"]
            personalizado["sidebar_active"] = base["primary"]
            personalizado["sidebar_text"] = "#F3F7F7"
            personalizado["text"] = "#243238"
            personalizado["muted"] = "#68777A"
            personalizado["success"] = "#2D8A67"
            personalizado["danger"] = "#B4514B"
            personalizado["success_bg"] = "#E7F4ED"
            personalizado["danger_bg"] = "#F9E9E7"
            personalizado["surface"] = "#FFFFFF"
            personalizado["surface_alt"] = "#F6F8F8"
            personalizado["header"] = "#F8FAF9"
            self.paleta_personalizada = personalizado.copy()
            self.TEMAS["Personalizado"] = personalizado
            self.aplicar_tema("Personalizado", personalizado)
            ventana.destroy()

        ttk.Button(personalizado, text="Guardar combinación personalizada", style="Accent.TButton", command=guardar_personalizado).pack(anchor="w", pady=(12, 0))

    def configurar_entrada(self, entrada, mover_derecha=None, mover_izquierda=None, mover_arriba=None, mover_abajo=None):
        """Hace que un Entry se comporte como una casilla de calculadora.

        Al entrar se limpia el cero de ayuda y, al salir, una casilla vacía
        vuelve a mostrar 0. Las flechas llevan directamente a la casilla
        vecina, evitando depender de una lista global de entradas.
        """
        entrada._valor_inicial = "0"
        entrada.bind("<FocusIn>", lambda e, w=entrada: self._limpiar_cero(w), add="+")
        entrada.bind("<FocusOut>", lambda e, w=entrada: self._restaurar_cero(w), add="+")
        entrada.bind("<Right>", lambda e, w=mover_derecha: self._mover_foco_especifico(w))
        entrada.bind("<Left>", lambda e, w=mover_izquierda: self._mover_foco_especifico(w))
        entrada.bind("<Up>", lambda e, w=mover_arriba: self._mover_foco_especifico(w))
        entrada.bind("<Down>", lambda e, w=mover_abajo: self._mover_foco_especifico(w))
        entrada.bind("<Return>", lambda e, w=mover_derecha: self._mover_foco_especifico(w))

    def _limpiar_cero(self, entrada):
        if entrada.get().strip() == "0":
            entrada.delete(0, "end")

    def _restaurar_cero(self, entrada):
        if not entrada.get().strip():
            entrada.insert(0, "0")

    def _mover_foco_especifico(self, destino):
        if destino is not None:
            destino.focus_set()
            destino.icursor("end")
        return "break"

    def preparar_navegacion(self, entradas):
        """Registra una cuadrícula de Entry con navegación por teclado.

        Las flechas izquierda/derecha recorren la fila; arriba/abajo
        conservan la columna cuando existe en la fila vecina. Esto funciona
        de forma independiente para cada matriz o grupo de vectores.
        """
        if not entradas:
            self.entradas_navegables = []
            return

        # Normalizamos una lista simple a una sola fila.
        if not isinstance(entradas[0], list):
            entradas = [list(entradas)]

        self.entradas_navegables = [e for fila in entradas for e in fila]
        for i, fila in enumerate(entradas):
            for j, entrada in enumerate(fila):
                izquierda = fila[j - 1] if j > 0 else None
                derecha = fila[j + 1] if j + 1 < len(fila) else None
                arriba = entradas[i - 1][j] if i > 0 and j < len(entradas[i - 1]) else None
                abajo = entradas[i + 1][j] if i + 1 < len(entradas) and j < len(entradas[i + 1]) else None
                self.configurar_entrada(entrada, derecha, izquierda, arriba, abajo)

    def marcar_sidebar_activa(self, nombre):
        """Resalta claramente la sección activa en la barra lateral."""
        if not self.botones_sidebar:
            return
        for clave, boton in self.botones_sidebar.items():
            boton.configure(style="SidebarActive.TButton" if clave == nombre else "Sidebar.TButton")

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
        self.construir_vista_vectores()
        self.construir_vista_matrices()
        self.construir_vista_matriz_vector()
        self.construir_vista_propiedades()
        self.mostrar_vista("entrada")

        ttk.Label(
            self.area,
            text="Programa 3 • Álgebra Lineal (MTM0120) • Grupo 4",
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
        self.botones_sidebar["entrada"] = self.boton_entrada

        self.boton_proceso = ttk.Button(self.sidebar, text="∑   Proceso Gaussiano", style="Sidebar.TButton", command=self.abrir_proceso)
        self.boton_proceso.pack(fill="x", pady=3)
        self.botones_sidebar["proceso"] = self.boton_proceso

        self.boton_jordan = ttk.Button(self.sidebar, text="≡   Proceso Gauss-Jordan", style="Sidebar.TButton", command=self.abrir_proceso_jordan)
        self.boton_jordan.pack(fill="x", pady=3)
        self.botones_sidebar["jordan"] = self.boton_jordan

        self.boton_vectores = ttk.Button(
            self.sidebar, text="→   Operaciones de Vectores", style="Sidebar.TButton",
            command=lambda: self.mostrar_vista("vectores")
        )
        self.boton_vectores.pack(fill="x", pady=3)
        self.botones_sidebar["vectores"] = self.boton_vectores

        self.boton_matrices = ttk.Button(
            self.sidebar, text="▦   Operaciones Matriciales", style="Sidebar.TButton",
            command=lambda: self.mostrar_vista("matrices")
        )
        self.boton_matrices.pack(fill="x", pady=3)
        self.botones_sidebar["matrices"] = self.boton_matrices

        self.boton_matriz_vector = ttk.Button(
            self.sidebar, text="A·v   Matriz por Vector", style="Sidebar.TButton",
            command=lambda: self.mostrar_vista("matriz_vector")
        )
        self.boton_matriz_vector.pack(fill="x", pady=3)
        self.botones_sidebar["matriz_vector"] = self.boton_matriz_vector

        self.boton_propiedades = ttk.Button(
            self.sidebar, text="∷   Propiedades y Dependencias", style="Sidebar.TButton",
            command=lambda: self.mostrar_vista("propiedades")
        )
        self.boton_propiedades.pack(fill="x", pady=3)
        self.botones_sidebar["propiedades"] = self.boton_propiedades

        self.boton_resultados = ttk.Button(self.sidebar, text="✓   Análisis de Resultados", style="Sidebar.TButton", command=lambda: self.mostrar_vista("resultados"))
        self.boton_resultados.pack(fill="x", pady=3)
        self.botones_sidebar["resultados"] = self.boton_resultados

        ttk.Separator(self.sidebar).pack(fill="x", pady=22)

        ttk.Label(self.sidebar, text="PROGRAMA 3", style="Sidebar.TLabel", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Label(self.sidebar, text="Álgebra Vectorial y Matricial", style="Sidebar.TLabel").pack(anchor="w", pady=(4, 14))

        ttk.Button(self.sidebar, text="?   Información del grupo", style="Sidebar.TButton", command=self.mostrar_info).pack(fill="x", pady=3)
        ttk.Button(self.sidebar, text="●   Tema y colores", style="Sidebar.TButton", command=self.abrir_personalizacion_colores).pack(fill="x", pady=3)

        ttk.Label(self.sidebar, text="\nUniversidad Americana\nFacultad de Ingeniería y Arquitectura", style="Sidebar.TLabel", justify="left").pack(side="bottom", anchor="w")

    def construir_header(self):
        header = ttk.Frame(self.area, padding=(24, 18), style="Top.TFrame")
        header.pack(fill="x")

        ttk.Label(header, text="Estudio de Álgebra Lineal", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Operaciones Vectoriales y Matriciales  •  Programa 3  •  Grupo 4", style="HeaderSub.TLabel").pack(anchor="w", pady=(2, 0))

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
            text="Puede ingresar enteros, decimales o fracciones (ej.: 3/4, -5/2).",
            style="CardSubtitle.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        botones = ttk.Frame(self.tarjeta_matriz, style="Card.TFrame")
        botones.pack(fill="x", pady=(14, 0))
        ttk.Button(botones, text="Resolver con Gauss", style="Accent.TButton", command=self.resolver).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ttk.Button(botones, text="Gauss-Jordan", style="Accent.TButton", command=self.resolver_jordan).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(botones, text="Ver Ax = b", style="Accent.TButton", command=self.mostrar_forma_matricial).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(botones, text="Limpiar", style="Coral.TButton", command=self.limpiar).pack(side="right", fill="x", expand=True, padx=(4, 0))

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
        self.proceso_texto = tk.Text(matriz_box, font=("Consolas", 12), bg=self.SURFACE_ALT, fg=self.DARK, relief="flat", state="disabled", insertbackground=self.DARK)
        self.proceso_texto.pack(fill="both", expand=True)
        self.text_widgets.append(self.proceso_texto)

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
        self.matriz_final_texto = tk.Text(detalle, font=("Consolas", 11), bg=self.SURFACE_ALT, fg=self.DARK, relief="flat", state="disabled", height=8, insertbackground=self.DARK)
        self.matriz_final_texto.pack(fill="both", expand=True, pady=(16, 0))
        self.text_widgets.append(self.matriz_final_texto)

        self.mostrar_resultado_placeholder()

    def mostrar_resultado_placeholder(self):
        for widget in self.resultado_resumen.winfo_children():
            widget.destroy()
        ttk.Label(self.resultado_resumen, text="Sin datos", style="SectionTitle.TLabel").pack(anchor="w", pady=30)

        for widget in self.verificacion_resumen.winfo_children():
            widget.destroy()
        ttk.Label(self.verificacion_resumen, text="Resuelva un sistema para verificarlo.", style="CardSubtitle.TLabel").pack(anchor="w", pady=30)

        self.actualizar_texto(self.matriz_final_texto, "No hay matriz escalonada disponible.")

    def construir_vista_vectores(self):
        """Construye la vista de operaciones en R^n reutilizando el estilo visual existente."""
        self.vista_vectores = self.nueva_vista()
        self.vista_vectores.columnconfigure(0, weight=1)
        self.vista_vectores.columnconfigure(1, weight=1)
        self.vista_vectores.rowconfigure(1, weight=1)

        izquierda = Tarjeta(
            self.vista_vectores,
            "Operaciones con Vectores en Rⁿ",
            "Suma, resta, producto por escalar y combinación lineal."
        )
        izquierda.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        derecha = Tarjeta(
            self.vista_vectores,
            "Resultado Vectorial",
            "Los cálculos se muestran con fracciones exactas."
        )
        derecha.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))

        config = ttk.Frame(izquierda, style="Card.TFrame")
        config.pack(fill="x", pady=(16, 5))
        ttk.Label(config, text="Dimensión n", style="CardSubtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(config, text="Vectores generadores", style="CardSubtitle.TLabel").grid(row=0, column=2, sticky="w", padx=(20, 0))
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.dimension_vector, width=7).grid(row=1, column=0, pady=5, sticky="w")
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.cantidad_vectores, width=7).grid(row=1, column=2, padx=(20, 0), pady=5, sticky="w")
        ttk.Button(config, text="Generar", style="Accent.TButton", command=self.generar_vectores).grid(row=1, column=4, padx=(20, 0))

        self.marco_vectores = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_vectores.pack(fill="both", expand=True, pady=(10, 0))

        botones = ttk.Frame(izquierda, style="Card.TFrame")
        botones.pack(fill="x", pady=(14, 0))
        ttk.Button(botones, text="Suma A + B", style="Accent.TButton", command=lambda: self.operar_vector("suma")).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ttk.Button(botones, text="Resta A - B", style="Accent.TButton", command=lambda: self.operar_vector("resta")).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(botones, text="Escalar A", style="Accent.TButton", command=lambda: self.operar_vector("escalar")).pack(side="left", fill="x", expand=True, padx=(4, 0))

        self.marco_resultado_vector = ttk.Frame(derecha, style="Card.TFrame")
        self.marco_resultado_vector.pack(fill="both", expand=True, pady=(16, 0))
        ttk.Button(
            derecha, text="Evaluar combinación lineal", style="Accent.TButton",
            command=self.evaluar_combinacion
        ).pack(anchor="w", pady=(14, 0))
        ttk.Button(
            derecha, text="Analizar dependencia lineal", style="Coral.TButton",
            command=self.evaluar_dependencia_lineal
        ).pack(anchor="w", pady=(8, 0))
        self.generar_vectores()

    def generar_vectores(self):
        """Genera las casillas para vectores según n; equivale a definir los elementos de R^n."""
        try:
            n = int(self.dimension_vector.get())
            k = int(self.cantidad_vectores.get())
            if not 1 <= n <= 8 or not 1 <= k <= 8:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Use dimensiones entre 1 y 8.")
            return

        for widget in self.marco_vectores.winfo_children():
            widget.destroy()
        self.generador_entries = []
        self.vector_entries = []
        self.vector_b_entries = []

        ttk.Label(self.marco_vectores, text="Vectores generadores", style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=n+1, sticky="w", pady=(0, 8))
        for j in range(n):
            ttk.Label(self.marco_vectores, text=self.subindice("v", j+1) if j < k else "", style="CardSubtitle.TLabel").grid(row=1, column=j+1, padx=4)

        # Cada columna representa un vector v_j y cada fila una componente.
        for j in range(k):
            ttk.Label(self.marco_vectores, text=self.subindice("v", j+1), style="CardSubtitle.TLabel").grid(row=j+2, column=0, sticky="w")
            fila = []
            for i in range(n):
                e = ttk.Entry(self.marco_vectores, width=7, justify="center")
                e.insert(0, "0")
                e.grid(row=j+2, column=i+1, padx=3, pady=3)
                fila.append(e)
            self.generador_entries.append(fila)

        ttk.Label(self.marco_vectores, text="Vector A", style="SectionTitle.TLabel").grid(row=k+3, column=0, sticky="w", pady=(14, 5))
        for i in range(n):
            e = ttk.Entry(self.marco_vectores, width=7, justify="center")
            e.insert(0, "0")
            e.grid(row=k+3, column=i+1, padx=3, pady=(14, 5))
            self.vector_entries.append(e)

        ttk.Label(self.marco_vectores, text="Vector B (para A+B/A-B)", style="SectionTitle.TLabel").grid(row=k+4, column=0, sticky="w")
        for i in range(n):
            e = ttk.Entry(self.marco_vectores, width=7, justify="center")
            e.insert(0, "0")
            e.grid(row=k+4, column=i+1, padx=3, pady=3)
            self.vector_b_entries.append(e)

        ttk.Label(self.marco_vectores, text="Escalar", style="CardSubtitle.TLabel").grid(row=k+5, column=0, sticky="w", pady=(8, 0))
        self.entrada_escalar = ttk.Entry(self.marco_vectores, textvariable=self.escalar, width=7, justify="center")
        self.entrada_escalar.grid(row=k+5, column=1, pady=(8, 0), sticky="w")
        self.preparar_navegacion(self.generador_entries + [self.vector_entries, self.vector_b_entries])

        self.mostrar_resultado_vector("Ingrese datos y seleccione una operación.")

    def leer_vector_entries(self, entries):
        """Lee las componentes de un vector; cada entrada representa una coordenada real."""
        try:
            return [leer_fraccion(e.get()) for e in entries]
        except ValueError as error:
            messagebox.showerror("Entrada inválida", str(error))
            return None

    def mostrar_resultado_vector(self, texto):
        """Actualiza el panel de resultado sin modificar la apariencia de la interfaz."""
        for widget in self.marco_resultado_vector.winfo_children():
            widget.destroy()
        ttk.Label(self.marco_resultado_vector, text=texto, style="SectionTitle.TLabel", wraplength=420).pack(anchor="w", pady=20)

    def formatear_vector(self, vector):
        """Convierte un vector a una representación legible de sus componentes."""
        return "( " + ",  ".join(formatear_numero(x) for x in vector) + " )"

    @staticmethod
    def subindice(letra, numero):
        """Devuelve etiquetas matemáticas como v₁, v₂, v₃ en lugar de v1, v2, v3."""
        mapa = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return f"{letra}{str(numero).translate(mapa)}"

    def formatear_vector_columna(self, vector):
        """Presenta un vector como columna para acercarlo a la notación matemática."""
        return "[\n" + "\n".join(f"  {formatear_numero(x):>6}" for x in vector) + "\n]"

    def evaluar_dependencia_lineal(self):
        """Analiza si los vectores generadores son linealmente independientes."""
        try:
            vectores = []
            for entradas in self.generador_entries:
                vector = self.leer_vector_entries(entradas)
                if vector is None:
                    return
                vectores.append(vector)
            resultado = analizar_dependencia_lineal(vectores)
        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))
            return

        cantidad = resultado["cantidad"]
        dimension = resultado["dimension"]
        if resultado["independiente"]:
            texto = (
                "✓ Los vectores son linealmente independientes.\n\n"
                f"Cantidad de vectores: {cantidad}\n"
                f"Dimensión de Rⁿ: {dimension}\n"
                f"Rango: {resultado['rango']}\n\n"
                "La única combinación que produce el vector cero es la combinación trivial "
                "(todos los coeficientes son 0)."
            )
        else:
            relacion = resultado.get("relacion")
            if relacion is not None:
                partes = []
                for i, coef in enumerate(relacion):
                    if coef != 0:
                        partes.append(f"({formatear_numero(coef)}){self.subindice('v', i+1)}")
                relacion_texto = " + ".join(partes) + " = 0"
            else:
                relacion_texto = "Existe una relación no trivial entre los vectores."
            texto = (
                "⚠ Los vectores son linealmente dependientes.\n\n"
                f"Cantidad de vectores: {cantidad}\n"
                f"Dimensión de Rⁿ: {dimension}\n"
                f"Rango: {resultado['rango']}\n\n"
                f"Relación no trivial encontrada: {relacion_texto}\n\n"
                "Dependencia dimensional: si hay más vectores que la dimensión del espacio, "
                "el conjunto necesariamente es dependiente."
            )
        self.mostrar_resultado_vector(texto)

    def operar_vector(self, operacion):
        """Ejecuta la operación vectorial seleccionada aplicando la definición componente a componente."""
        a = self.leer_vector_entries(self.vector_entries)
        b = self.leer_vector_entries(self.vector_b_entries)
        if a is None or b is None:
            return
        try:
            if operacion == "suma":
                resultado = sumar_vectores(a, b)
                titulo = "A + B"
            elif operacion == "resta":
                resultado = restar_vectores(a, b)
                titulo = "A - B"
            else:
                resultado = multiplicar_escalar(a, leer_fraccion(self.escalar.get()))
                titulo = f"{formatear_numero(leer_fraccion(self.escalar.get()))}A"
        except ValueError as error:
            messagebox.showerror("Operación inválida", str(error))
            return
        self.mostrar_resultado_vector(f"{titulo}\n\n= {self.formatear_vector(resultado)}")

    def evaluar_combinacion(self):
        """Evalúa b=c1v1+...+ckvk mediante el sistema matricial equivalente Vc=b."""
        try:
            vectores = []
            for fila in self.generador_entries:
                vector = self.leer_vector_entries(fila)
                if vector is None:
                    return
                vectores.append(vector)
            b = self.leer_vector_entries(self.vector_entries)
            if b is None:
                return
            resultado = es_combinacion_lineal(vectores, b)
        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))
            return

        if resultado["es_combinacion"]:
            if resultado["coeficientes"] is not None:
                coef = ", ".join(
                    f"c{i+1} = {formatear_numero(v)}"
                    for i, v in enumerate(resultado["coeficientes"])
                )
                texto = "✓ Sí, es combinación lineal.\n\n" + coef
            else:
                libres = ", ".join(f"c{i+1}" for i in resultado["variables_libres"])
                texto = "✓ Sí, es combinación lineal.\n\nExisten infinitas combinaciones.\nVariables libres: " + libres
        else:
            texto = "✗ No es combinación lineal.\n\nEl sistema equivalente Vc = A es inconsistente."
        self.mostrar_resultado_vector(texto)

    def construir_vista_matrices(self):
        """Construye el módulo de operaciones matriciales manteniendo tarjetas y estilos existentes."""
        self.vista_matrices = self.nueva_vista()
        self.vista_matrices.columnconfigure(0, weight=1)
        self.vista_matrices.columnconfigure(1, weight=1)
        self.vista_matrices.rowconfigure(1, weight=1)

        izquierda = Tarjeta(
            self.vista_matrices, "Operaciones Matriciales Básicas",
            "Suma, resta, producto por escalar y multiplicación A·B."
        )
        izquierda.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        derecha = Tarjeta(
            self.vista_matrices, "Resultado Matricial",
            "Se validan automáticamente las dimensiones."
        )
        derecha.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))

        config = ttk.Frame(izquierda, style="Card.TFrame")
        config.pack(fill="x", pady=(16, 6))
        for col, texto, var in [
            (0, "Filas A", self.filas_a), (2, "Columnas A", self.columnas_a),
            (4, "Filas B", self.filas_b), (6, "Columnas B", self.columnas_b)
        ]:
            ttk.Label(config, text=texto, style="CardSubtitle.TLabel").grid(row=0, column=col, padx=3)
            ttk.Spinbox(config, from_=1, to=8, textvariable=var, width=5).grid(row=1, column=col, padx=3, pady=4)

        ttk.Label(config, text="Operación", style="CardSubtitle.TLabel").grid(row=2, column=0, pady=(8, 0), sticky="w")
        opciones = ["Suma (A + B)", "Resta (A - B)", "Escalar (cA)", "Multiplicación (A · B)"]
        ttk.Combobox(config, textvariable=self.operacion_matriz, values=opciones, state="readonly", width=23).grid(row=3, column=0, columnspan=5, sticky="w", pady=4)
        ttk.Button(config, text="Generar matrices", style="Accent.TButton", command=self.generar_matrices).grid(row=3, column=6, padx=5)

        self.marco_matrices = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_matrices.pack(fill="both", expand=True, pady=(10, 0))
        self.marco_resultado_matriz = ttk.Frame(derecha, style="Card.TFrame")
        self.marco_resultado_matriz.pack(fill="both", expand=True, pady=(16, 0))
        ttk.Button(derecha, text="Calcular operación", style="Accent.TButton", command=self.operar_matriz).pack(anchor="w", pady=(14, 0))
        self.generar_matrices()

    def crear_entradas_matriz(self, contenedor, filas, columnas, titulo):
        """Crea una cuadrícula m×n; cada casilla corresponde a una entrada a_ij."""
        marco = ttk.Frame(contenedor, style="Card.TFrame")
        marco.pack(fill="x", pady=(5, 10))
        ttk.Label(marco, text=titulo, style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=columnas, sticky="w", pady=(0, 5))
        entradas = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                e = ttk.Entry(marco, width=7, justify="center")
                e.insert(0, "0")
                e.grid(row=i+1, column=j, padx=3, pady=3)
                fila.append(e)
            entradas.append(fila)
        return entradas

    def generar_matrices(self):
        """Regenera las matrices A y B de acuerdo con sus dimensiones seleccionadas."""
        try:
            fa, ca = int(self.filas_a.get()), int(self.columnas_a.get())
            fb, cb = int(self.filas_b.get()), int(self.columnas_b.get())
            if not all(1 <= x <= 8 for x in (fa, ca, fb, cb)):
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Use dimensiones entre 1 y 8.")
            return
        for widget in self.marco_matrices.winfo_children():
            widget.destroy()
        self.matriz_a_entries = self.crear_entradas_matriz(self.marco_matrices, fa, ca, "Matriz A")
        self.matriz_b_entries = self.crear_entradas_matriz(self.marco_matrices, fb, cb, "Matriz B")
        self.preparar_navegacion(self.matriz_a_entries + self.matriz_b_entries)
        ttk.Label(self.marco_matrices, text="Para cA, el escalar se toma del campo de operación.", style="CardSubtitle.TLabel").pack(anchor="w", pady=5)
        self.mostrar_resultado_matriz("Genere las matrices, complete sus entradas y calcule.")

    def leer_matriz_entries(self, entries):
        """Convierte las casillas de una matriz en una lista de filas de números racionales."""
        try:
            return [[leer_fraccion(e.get()) for e in fila] for fila in entries]
        except ValueError as error:
            messagebox.showerror("Entrada inválida", str(error))
            return None

    def mostrar_resultado_matriz(self, texto):
        """Presenta una matriz o mensaje en el panel de resultados."""
        for widget in self.marco_resultado_matriz.winfo_children():
            widget.destroy()
        texto_widget = tk.Text(self.marco_resultado_matriz, font=("Consolas", 11), bg=self.SURFACE_ALT, fg=self.DARK, relief="flat", state="normal", height=12, insertbackground=self.DARK)
        texto_widget.insert("1.0", texto)
        texto_widget.config(state="disabled")
        texto_widget.pack(fill="both", expand=True)
        self.text_widgets.append(texto_widget)

    def operar_matriz(self):
        """Ejecuta la operación matricial seleccionada respetando las condiciones de dimensiones."""
        a = self.leer_matriz_entries(self.matriz_a_entries)
        b = self.leer_matriz_entries(self.matriz_b_entries)
        if a is None or b is None:
            return
        op = self.operacion_matriz.get()
        try:
            if op == "Suma (A + B)":
                resultado = sumar_matrices(a, b)
            elif op == "Resta (A - B)":
                resultado = restar_matrices(a, b)
            elif op == "Escalar (cA)":
                c = leer_fraccion(self.escalar.get())
                resultado = multiplicar_matriz_escalar(a, c)
            else:
                resultado = multiplicar_matrices(a, b)
        except ValueError as error:
            messagebox.showerror("Dimensiones incompatibles", str(error))
            return

        lineas = [f"{op}", ""]
        lineas.extend(formatear_matriz_lineas(resultado, len(resultado[0])))
        self.mostrar_resultado_matriz("\n".join(lineas))

    def construir_vista_matriz_vector(self):
        """Módulo directo para productos A·v y la distributividad A(u+v)=Au+Av.

        Este módulo cubre directamente los ejercicios del examen que requieren
        producto matriz-vector y la interpretación del resultado como
        combinación lineal de las columnas de A.
        """
        self.vista_matriz_vector = self.nueva_vista()
        self.vista_matriz_vector.columnconfigure(0, weight=1)
        self.vista_matriz_vector.columnconfigure(1, weight=1)
        self.vista_matriz_vector.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.vista_matriz_vector,
            "Producto matriz · vector",
            "Ingrese A y dos vectores. El vector v se usa para A·v; u y v permiten verificar la distributividad."
        )
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        derecha = Tarjeta(
            self.vista_matriz_vector,
            "Resultado del examen",
            "Muestra el cálculo, la igualdad distributiva y la combinación lineal de las columnas."
        )
        derecha.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        config = ttk.Frame(izquierda, style="Card.TFrame")
        config.pack(fill="x", pady=(16, 8))
        ttk.Label(config, text="Filas de A (m)", style="CardSubtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(config, text="Columnas de A (n)", style="CardSubtitle.TLabel").grid(row=0, column=2, sticky="w", padx=(20, 0))
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.filas_mv, width=6).grid(row=1, column=0, pady=5, sticky="w")
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.columnas_mv, width=6).grid(row=1, column=2, padx=(20, 0), pady=5, sticky="w")
        ttk.Button(config, text="Generar", style="Accent.TButton", command=self.generar_matriz_vector).grid(row=1, column=4, padx=(20, 0))

        self.marco_matriz_vector = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_matriz_vector.pack(fill="both", expand=True, pady=(8, 0))

        botones = ttk.Frame(izquierda, style="Card.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        ttk.Button(
            botones, text="Calcular A·v", style="Accent.TButton",
            command=self.calcular_matriz_vector
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ttk.Button(
            botones, text="Verificar A(u+v)", style="Accent.TButton",
            command=self.verificar_distributividad_mv
        ).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(
            botones, text="Limpiar", style="Coral.TButton",
            command=self.generar_matriz_vector
        ).pack(side="right", fill="x", expand=True, padx=(4, 0))

        self.marco_resultado_matriz_vector = ttk.Frame(derecha, style="Card.TFrame")
        self.marco_resultado_matriz_vector.pack(fill="both", expand=True, pady=(16, 0))
        self.generar_matriz_vector()

    def crear_entradas_vector_mv(self, contenedor, titulo, n):
        marco = ttk.Frame(contenedor, style="Card.TFrame")
        marco.pack(fill="x", pady=(5, 7))
        ttk.Label(marco, text=titulo, style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w")
        entradas = []
        for j in range(n):
            e = ttk.Entry(marco, width=7, justify="center")
            e.insert(0, "0")
            e.grid(row=1, column=j, padx=3, pady=5)
            entradas.append(e)
        return entradas

    def generar_matriz_vector(self):
        """Genera A, u y v respetando que A sea m×n y cada vector tenga n componentes."""
        try:
            m = int(self.filas_mv.get())
            n = int(self.columnas_mv.get())
            if not 1 <= m <= 8 or not 1 <= n <= 8:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Use dimensiones entre 1 y 8.")
            return

        for widget in self.marco_matriz_vector.winfo_children():
            widget.destroy()

        ttk.Label(
            self.marco_matriz_vector,
            text=f"Matriz A ({m}×{n})",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(0, 4))

        marco_a = ttk.Frame(self.marco_matriz_vector, style="Card.TFrame")
        marco_a.pack(fill="x", pady=(0, 7))
        self.matriz_mv_entries = []
        for i in range(m):
            fila = []
            for j in range(n):
                e = ttk.Entry(marco_a, width=7, justify="center")
                e.insert(0, "0")
                e.grid(row=i, column=j, padx=3, pady=3)
                fila.append(e)
            self.matriz_mv_entries.append(fila)

        self.vector_u_mv_entries = self.crear_entradas_vector_mv(
            self.marco_matriz_vector, "Vector u", n
        )
        self.vector_v_mv_entries = self.crear_entradas_vector_mv(
            self.marco_matriz_vector, "Vector v", n
        )

        self.preparar_navegacion(
            self.matriz_mv_entries + [self.vector_u_mv_entries, self.vector_v_mv_entries]
        )
        self.mostrar_resultado_matriz_vector(
            "Complete A, u y v.\n\n"
            "• «Calcular A·v» resuelve el producto y muestra la combinación lineal.\n"
            "• «Verificar A(u+v)» comprueba A(u+v)=Au+Av."
        )

    def leer_matriz_vector_entries(self):
        try:
            matriz = [
                [leer_fraccion(e.get()) for e in fila]
                for fila in self.matriz_mv_entries
            ]
            u = [leer_fraccion(e.get()) for e in self.vector_u_mv_entries]
            v = [leer_fraccion(e.get()) for e in self.vector_v_mv_entries]
            return matriz, u, v
        except ValueError as error:
            messagebox.showerror("Entrada inválida", str(error))
            return None

    def mostrar_resultado_matriz_vector(self, texto):
        for widget in self.marco_resultado_matriz_vector.winfo_children():
            widget.destroy()
        caja = tk.Text(
            self.marco_resultado_matriz_vector,
            font=("Consolas", 10),
            bg=self.SURFACE_ALT,
            fg=self.DARK,
            relief="flat",
            state="normal",
            wrap="word"
        )
        caja.insert("1.0", texto)
        caja.config(state="disabled")
        caja.pack(fill="both", expand=True)
        self.text_widgets.append(caja)

    def _formatear_vector_columna_bonito(self, vector):
        return "[ " + "\n  ".join(formatear_numero(x) for x in vector) + " ]"

    def _formatear_matriz_normal_mv(self, matriz):
        return "\n".join(formatear_matriz_lineas(matriz, len(matriz[0])))

    def calcular_matriz_vector(self):
        datos = self.leer_matriz_vector_entries()
        if datos is None:
            return
        matriz, u, v = datos
        try:
            resultado = multiplicar_matriz_vector(matriz, v)
        except ValueError as error:
            messagebox.showerror("Dimensiones incompatibles", str(error))
            return

        partes = []
        for j, coef in enumerate(v):
            columna = [fila[j] for fila in matriz]
            partes.append(
                f"({formatear_numero(coef)})·C{j + 1} = "
                f"({formatear_numero(coef)}){self._formatear_vector_columna_bonito(columna)}"
            )

        combinacion = " + ".join(
            f"({formatear_numero(coef)})C{j + 1}"
            for j, coef in enumerate(v)
        )

        texto = (
            "PRODUCTO MATRIZ · VECTOR\n\n"
            f"A =\n{self._formatear_matriz_normal_mv(matriz)}\n\n"
            f"v = {self._formatear_vector_columna_bonito(v)}\n\n"
            f"A·v = {self._formatear_vector_columna_bonito(resultado)}\n\n"
            "COMBINACIÓN LINEAL DE LAS COLUMNAS\n"
            f"A·v = {combinacion}\n\n"
            + "\n".join(partes)
            + "\n\n"
            f"Por tanto, A·v = {combinacion} = {self._formatear_vector_columna_bonito(resultado)}."
        )
        self.mostrar_resultado_matriz_vector(texto)

    def verificar_distributividad_mv(self):
        datos = self.leer_matriz_vector_entries()
        if datos is None:
            return
        matriz, u, v = datos
        try:
            suma = sumar_vectores(u, v)
            izquierda = multiplicar_matriz_vector(matriz, suma)
            au = multiplicar_matriz_vector(matriz, u)
            av = multiplicar_matriz_vector(matriz, v)
            derecha = sumar_vectores(au, av)
        except ValueError as error:
            messagebox.showerror("Dimensiones incompatibles", str(error))
            return

        cumple = izquierda == derecha
        texto = (
            "VERIFICACIÓN DE LA PROPIEDAD DISTRIBUTIVA\n\n"
            "A(u + v) = Au + Av\n\n"
            f"1) u + v = {self._formatear_vector_columna_bonito(suma)}\n\n"
            f"2) A(u + v) = {self._formatear_vector_columna_bonito(izquierda)}\n\n"
            f"3) Au = {self._formatear_vector_columna_bonito(au)}\n"
            f"   Av = {self._formatear_vector_columna_bonito(av)}\n\n"
            f"4) Au + Av = {self._formatear_vector_columna_bonito(derecha)}\n\n"
            + ("✓ Se cumple: A(u + v) = Au + Av."
               if cumple else "✗ No coincide. Revise los datos.")
        )
        self.mostrar_resultado_matriz_vector(texto)

    def construir_vista_propiedades(self):
        """Construye el módulo para verificar las 8 propiedades solicitadas."""
        self.vista_propiedades = self.nueva_vista()
        self.vista_propiedades.columnconfigure(0, weight=3)
        self.vista_propiedades.columnconfigure(1, weight=2)
        self.vista_propiedades.rowconfigure(1, weight=1)

        izquierda = Tarjeta(
            self.vista_propiedades,
            "Propiedades de matrices y producto matriz–vector",
            "Las mismas matrices y vectores permanecen cargados al cambiar de propiedad."
        )
        izquierda.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        derecha = Tarjeta(
            self.vista_propiedades,
            "Resultado y dependencias",
            "Se comprueba la igualdad y se explican las condiciones de dimensiones y componentes."
        )
        derecha.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))

        config = ttk.Frame(izquierda, style="Card.TFrame")
        config.pack(fill="x", pady=(16, 8))
        ttk.Label(config, text="Filas m", style="CardSubtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(config, text="Columnas n", style="CardSubtitle.TLabel").grid(row=0, column=2, sticky="w", padx=(15, 0))
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.filas_propiedad, width=5).grid(row=1, column=0, sticky="w")
        ttk.Spinbox(config, from_=1, to=8, textvariable=self.columnas_propiedad, width=5).grid(row=1, column=2, sticky="w", padx=(15, 0))
        ttk.Button(config, text="Generar datos", style="Accent.TButton", command=self.generar_propiedades).grid(row=1, column=4, padx=(18, 0))

        ttk.Label(config, text="Propiedad a verificar", style="CardSubtitle.TLabel").grid(row=2, column=0, sticky="w", pady=(10, 0))
        propiedades = [
            "1. Conmutatividad: A + B = B + A",
            "2. Asociatividad: (A + B) + C = A + (B + C)",
            "3. Identidad aditiva: A + 0 = A",
            "4. Distributiva: r(A + B) = rA + rB",
            "5. Distributiva de escalares: (r + s)A = rA + sA",
            "6. Asociatividad escalar: r(sA) = (rs)A",
            "7. Producto matriz–vector: A(u + v) = Au + Av",
            "8. Homogeneidad matriz–vector: A(cu) = c(Au)",
        ]
        combo = ttk.Combobox(config, textvariable=self.propiedad_seleccionada, values=propiedades, state="readonly", width=58)
        combo.grid(row=3, column=0, columnspan=5, sticky="ew", pady=4)
        ttk.Button(config, text="Resolver propiedad", style="Accent.TButton", command=self.operar_propiedad).grid(row=3, column=5, padx=(8, 0))

        self.marco_propiedades = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_propiedades.pack(fill="both", expand=True, pady=(8, 0))
        self.marco_resultado_propiedad = ttk.Frame(derecha, style="Card.TFrame")
        self.marco_resultado_propiedad.pack(fill="both", expand=True, pady=(16, 0))
        self.generar_propiedades()

    def crear_entradas_propiedad_matriz(self, contenedor, filas, columnas, titulo):
        marco = ttk.Frame(contenedor, style="Card.TFrame")
        marco.pack(side="left", padx=(0, 10), pady=5, anchor="n")
        ttk.Label(marco, text=titulo, style="SectionTitle.TLabel").grid(row=0, column=0, columnspan=columnas, sticky="w", pady=(0, 5))
        entradas = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                e = ttk.Entry(marco, width=6, justify="center")
                e.insert(0, "0")
                e.grid(row=i+1, column=j, padx=2, pady=2)
                fila.append(e)
            entradas.append(fila)
        return entradas

    def crear_entradas_propiedad_vector(self, contenedor, dimension, titulo):
        marco = ttk.Frame(contenedor, style="Card.TFrame")
        marco.pack(side="left", padx=(0, 10), pady=5, anchor="n")
        ttk.Label(marco, text=titulo, style="SectionTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 5))
        entradas = []
        for i in range(dimension):
            e = ttk.Entry(marco, width=6, justify="center")
            e.insert(0, "0")
            e.grid(row=i+1, column=0, padx=2, pady=2)
            entradas.append(e)
        return entradas

    def generar_propiedades(self):
        try:
            m, n = int(self.filas_propiedad.get()), int(self.columnas_propiedad.get())
            if not (1 <= m <= 8 and 1 <= n <= 8):
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Las dimensiones deben estar entre 1 y 8.")
            return
        for widget in self.marco_propiedades.winfo_children():
            widget.destroy()

        fila_superior = ttk.Frame(self.marco_propiedades, style="Card.TFrame")
        fila_superior.pack(fill="x", pady=(4, 8))
        self.prop_a_entries = self.crear_entradas_propiedad_matriz(fila_superior, m, n, "Matriz A")
        self.prop_b_entries = self.crear_entradas_propiedad_matriz(fila_superior, m, n, "Matriz B")
        self.prop_c_entries = self.crear_entradas_propiedad_matriz(fila_superior, m, n, "Matriz C")

        fila_inferior = ttk.Frame(self.marco_propiedades, style="Card.TFrame")
        fila_inferior.pack(fill="x", pady=(5, 8))
        self.prop_u_entries = self.crear_entradas_propiedad_vector(fila_inferior, n, "Vector u")
        self.prop_v_entries = self.crear_entradas_propiedad_vector(fila_inferior, n, "Vector v")

        escalares = ttk.Frame(fila_inferior, style="Card.TFrame")
        escalares.pack(side="left", padx=(8, 0), pady=5, anchor="n")
        for fila, texto, variable in [(0, "r", self.escalar_r), (1, "s", self.escalar_s), (2, "c", self.escalar_c)]:
            ttk.Label(escalares, text=texto, style="CardSubtitle.TLabel").grid(row=fila, column=0, padx=(0, 5), pady=2)
            ttk.Entry(escalares, textvariable=variable, width=7, justify="center").grid(row=fila, column=1, pady=2)

        ttk.Label(
            self.marco_propiedades,
            text=f"Condición base: A, B y C son {m}×{n}; u y v pertenecen a Rⁿ ({n} componentes). Para A·u, las {n} columnas de A deben coincidir con la dimensión del vector.",
            style="CardSubtitle.TLabel", wraplength=720
        ).pack(anchor="w", pady=(6, 0))
        self.preparar_navegacion(self.prop_a_entries + self.prop_b_entries + self.prop_c_entries + [self.prop_u_entries, self.prop_v_entries])
        self.mostrar_resultado_propiedad("Seleccione una propiedad y presione «Resolver propiedad».")

    def leer_prop_matriz(self, entries):
        try:
            return [[leer_fraccion(e.get()) for e in fila] for fila in entries]
        except ValueError as error:
            messagebox.showerror("Entrada inválida", str(error))
            return None

    def leer_prop_vector(self, entries):
        try:
            return [leer_fraccion(e.get()) for e in entries]
        except ValueError as error:
            messagebox.showerror("Entrada inválida", str(error))
            return None

    def mostrar_resultado_propiedad(self, texto):
        for widget in self.marco_resultado_propiedad.winfo_children():
            widget.destroy()
        caja = tk.Text(self.marco_resultado_propiedad, font=("Consolas", 10), bg=self.SURFACE_ALT, fg=self.DARK, relief="flat", state="normal", wrap="word")
        caja.insert("1.0", texto)
        caja.config(state="disabled")
        caja.pack(fill="both", expand=True, pady=(8, 0))
        self.text_widgets.append(caja)

    def formatear_lado_propiedad(self, valor, es_vector=False):
        if es_vector:
            return self.formatear_vector_columna(valor)
        return "\n".join(formatear_matriz_lineas(valor, len(valor[0])))

    def operar_propiedad(self):
        A = self.leer_prop_matriz(self.prop_a_entries)
        B = self.leer_prop_matriz(self.prop_b_entries)
        C = self.leer_prop_matriz(self.prop_c_entries)
        u = self.leer_prop_vector(self.prop_u_entries)
        v = self.leer_prop_vector(self.prop_v_entries)
        if any(x is None for x in (A, B, C, u, v)):
            return
        try:
            nombre = self.propiedad_seleccionada.get()
            r = leer_fraccion(self.escalar_r.get())
            s = leer_fraccion(self.escalar_s.get())
            c = leer_fraccion(self.escalar_c.get())

            if nombre.startswith("1."):
                izquierda = sumar_matrices(A, B)
                derecha = sumar_matrices(B, A)
                titulo = "Propiedad 1 — Conmutatividad de la suma"
                detalle = "A + B = B + A"
                dep = "A y B deben tener exactamente las mismas dimensiones. Cada componente aᵢⱼ se suma con bᵢⱼ."
            elif nombre.startswith("2."):
                izquierda = sumar_matrices(sumar_matrices(A, B), C)
                derecha = sumar_matrices(A, sumar_matrices(B, C))
                titulo = "Propiedad 2 — Asociatividad de la suma"
                detalle = "(A + B) + C = A + (B + C)"
                dep = "A, B y C deben tener las mismas filas y columnas. La agrupación cambia, pero cada componente final conserva la misma suma."
            elif nombre.startswith("3."):
                cero = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
                izquierda = sumar_matrices(A, cero)
                derecha = A
                titulo = "Propiedad 3 — Identidad aditiva"
                detalle = "A + 0 = A"
                dep = "La matriz cero debe tener exactamente las mismas dimensiones que A; todos sus componentes son 0."
            elif nombre.startswith("4."):
                izquierda = multiplicar_matriz_escalar(sumar_matrices(A, B), r)
                derecha = sumar_matrices(multiplicar_matriz_escalar(A, r), multiplicar_matriz_escalar(B, r))
                titulo = "Propiedad 4 — Distributividad del escalar"
                detalle = "r(A + B) = rA + rB"
                dep = "A y B deben compartir dimensiones. r es un escalar y multiplica cada componente sin cambiar las dimensiones."
            elif nombre.startswith("5."):
                izquierda = multiplicar_matriz_escalar(A, r + s)
                derecha = sumar_matrices(multiplicar_matriz_escalar(A, r), multiplicar_matriz_escalar(A, s))
                titulo = "Propiedad 5 — Distributividad respecto a escalares"
                detalle = "(r + s)A = rA + sA"
                dep = "r y s son escalares. A conserva su dimensión m×n en ambos lados y cada componente se calcula de forma independiente."
            elif nombre.startswith("6."):
                izquierda = multiplicar_matriz_escalar(multiplicar_matriz_escalar(A, s), r)
                derecha = multiplicar_matriz_escalar(A, r * s)
                titulo = "Propiedad 6 — Asociatividad de la multiplicación escalar"
                detalle = "r(sA) = (rs)A"
                dep = "r y s son escalares; el producto escalar no cambia el número de filas ni de columnas de A."
            elif nombre.startswith("7."):
                suma_uv = sumar_vectores(u, v)
                izquierda = multiplicar_matriz_vector(A, suma_uv)
                derecha = sumar_vectores(multiplicar_matriz_vector(A, u), multiplicar_matriz_vector(A, v))
                titulo = "Propiedad 7 — Distributividad del producto matriz–vector"
                detalle = "A(u + v) = Au + Av"
                dep = "u y v deben tener n componentes y A debe ser m×n. u+v pertenece a Rⁿ; Au, Av y A(u+v) pertenecen a Rᵐ."
            else:
                cu = multiplicar_escalar(u, c)
                izquierda = multiplicar_matriz_vector(A, cu)
                derecha = multiplicar_escalar(multiplicar_matriz_vector(A, u), c)
                titulo = "Propiedad 8 — Homogeneidad del producto matriz–vector"
                detalle = "A(cu) = c(Au)"
                dep = "u debe tener n componentes y A debe ser m×n. El escalar c cambia los componentes de u, pero no su dimensión."
        except ValueError as error:
            messagebox.showerror("Dimensiones incompatibles", str(error))
            return

        es_vector = nombre.startswith(("7.", "8."))
        cuerpo = f"{titulo}\n\n{detalle}\n\nLADO IZQUIERDO:\n{self.formatear_lado_propiedad(izquierda, es_vector)}\n\nLADO DERECHO:\n{self.formatear_lado_propiedad(derecha, es_vector)}"
        cuerpo += "\n\n✓ Igualdad verificada." if izquierda == derecha else "\n\n✗ La igualdad no coincide; revise los datos."
        cuerpo += f"\n\nDEPENDENCIAS DE DIMENSIÓN Y COMPONENTES\n{dep}"
        self.mostrar_resultado_propiedad(cuerpo)

    def mostrar_vista(self, nombre):
        vistas = {
            "entrada": self.vista_entrada,
            "proceso": self.vista_proceso,
            "resultados": self.vista_resultados,
            "vectores": self.vista_vectores,
            "matrices": self.vista_matrices,
            "matriz_vector": self.vista_matriz_vector,
            "propiedades": self.vista_propiedades,
        }
        for vista in vistas.values():
            vista.lower()
        vistas[nombre].lift()
        self.vista_actual = nombre
        self.marcar_sidebar_activa(nombre)

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
                entrada = ttk.Entry(self.marco_entries, width=8, justify="center")
                entrada.insert(0, "0")
                entrada.grid(row=i + 1, column=j + 1, padx=3, pady=5)
                fila_entries.append(entrada)

            ttk.Label(self.marco_entries, text="|", style="SectionTitle.TLabel").grid(row=i + 1, column=variables + 1, padx=10)
            entrada_b = ttk.Entry(self.marco_entries, width=8, justify="center")
            entrada_b.insert(0, "0")
            entrada_b.grid(row=i + 1, column=variables + 2, padx=3, pady=5)
            fila_entries.append(entrada_b)
            self.matriz_entries.append(fila_entries)

        self.preparar_navegacion(self.matriz_entries)
        self.construir_resumen_placeholder()
        self.mostrar_resultado_placeholder()
        self.proceso_titulo.config(text="Primero resuelva un sistema")
        self.proceso_operacion.config(text="Aquí se mostrará la operación elemental aplicada.")
        self.actualizar_texto(self.proceso_texto, "No hay proceso disponible.")

        self.mostrar_vista("entrada")

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

    def mostrar_forma_matricial(self):
        """Muestra la matriz A, el vector incógnita x y el vector b del sistema Ax=b."""
        matriz = self.leer_matriz()
        if matriz is None:
            return

        n = int(self.numero_variables.get())
        if not matriz or any(len(fila) != n + 1 for fila in matriz):
            messagebox.showerror("Datos inválidos", "Primero genere una matriz aumentada válida.")
            return

        a = [fila[:n] for fila in matriz]
        b = [fila[n] for fila in matriz]
        x = [f"x{i + 1}" for i in range(n)]

        a_texto = "\n".join(formatear_matriz_lineas(a, n))
        b_texto = "\n".join(f"[ {formatear_numero(valor)} ]" for valor in b)
        x_texto = "\n".join(f"[ {nombre} ]" for nombre in x)

        texto = (
            "FORMA MATRICIAL DEL SISTEMA\n\n"
            f"A =\n{a_texto}\n\n"
            f"x =\n{x_texto}\n\n"
            f"b =\n{b_texto}\n\n"
            "Por lo tanto:\n\n"
            "A · x = b"
        )
        messagebox.showinfo("Forma matricial Ax = b", texto)

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
            "metodo": "Gauss",
        }

        self.actualizar_resumen()
        self.mostrar_vista("entrada")

    def resolver_jordan(self):
        matriz_original = self.leer_matriz()
        if matriz_original is None:
            return

        numero_variables = int(self.numero_variables.get())
        sistema = SistemaEcuaciones(matriz_original, numero_variables)
        reducida, pivotes, inconsistente, pasos = gauss_jordan(
            sistema.matriz_aumentada, sistema.numero_variables
        )
        clasificacion, libres = obtener_clasificacion(
            reducida, numero_variables, pivotes, inconsistente
        )

        solucion = None
        verificacion = None
        if clasificacion == "unica":
            # En Gauss-Jordan la matriz ya está reducida, por lo que la
            # solución se lee directamente de la columna independiente.
            solucion = [reducida[fila][numero_variables] for fila, _ in pivotes]
            verificacion = verificar_solucion(matriz_original, solucion)

        self.ultimo_resultado = {
            "matriz_original": matriz_original,
            "escalonada": reducida,
            "pivotes": pivotes,
            "inconsistente": inconsistente,
            "clasificacion": clasificacion,
            "variables_libres": libres,
            "solucion": solucion,
            "verificacion": verificacion,
            "pasos": pasos,
            "metodo": "Gauss-Jordan",
        }

        self.proceso_titulo.config(text="Proceso Gauss-Jordan")
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
            ttk.Label(self.resumen_contenido, text="✓", style="SuccessIcon.TLabel").pack(anchor="w", pady=(10, 4))
            ttk.Label(self.resumen_contenido, text="Consistente Determinado", style="Status.TLabel", padding=8).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="Solución Única", style="SectionTitle.TLabel").pack(anchor="w", pady=(10, 14))
            for i, valor in enumerate(resultado["solucion"]):
                ttk.Label(self.resumen_contenido, text=f"x{i + 1} = {formatear_numero(valor)}", style="MetricValue.TLabel").pack(anchor="w", pady=3)
            ttk.Button(self.resumen_contenido, text="Ver proceso paso a paso", style="Accent.TButton", command=self.abrir_proceso).pack(anchor="w", pady=(20, 0))
        elif clasificacion == "infinita":
            ttk.Label(self.resumen_contenido, text="∞", style="InfoIcon.TLabel").pack(anchor="w", pady=(10, 4))
            ttk.Label(self.resumen_contenido, text="Consistente Indeterminado", style="Status.TLabel", padding=8).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="Infinitas Soluciones", style="SectionTitle.TLabel").pack(anchor="w", pady=(10, 14))
            libres_texto = ", ".join(f"x{i + 1}" for i in resultado["variables_libres"])
            ttk.Label(self.resumen_contenido, text=f"Variables libres: {libres_texto}", style="MetricValue.TLabel", wraplength=380).pack(anchor="w")
            ttk.Label(self.resumen_contenido, text="En este avance se identifican las variables libres; la parametrización completa queda como mejora futura.", style="CardSubtitle.TLabel", wraplength=390).pack(anchor="w", pady=(18, 0))
            ttk.Button(self.resumen_contenido, text="Ver proceso paso a paso", style="Accent.TButton", command=self.abrir_proceso).pack(anchor="w", pady=(20, 0))
        else:
            ttk.Label(self.resumen_contenido, text="!", style="DangerIcon.TLabel").pack(anchor="w", pady=(10, 4))
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

    def abrir_proceso_jordan(self):
        if not self.ultimo_resultado:
            messagebox.showinfo("Proceso Gauss-Jordan", "Primero resuelva el sistema con el botón «Gauss-Jordan» para mostrar el proceso paso a paso.")
            return
        if self.ultimo_resultado.get("metodo") != "Gauss-Jordan":
            messagebox.showinfo("Proceso Gauss-Jordan", "El resultado actual fue obtenido con Gauss. Presione «Gauss-Jordan» para generar el proceso correspondiente.")
            return
        self.vista_actual = "jordan"
        self.marcar_sidebar_activa("jordan")
        VentanaProceso(self.root, self.ultimo_resultado["pasos"], int(self.numero_variables.get()), titulo="Proceso Gauss-Jordan • Paso a paso")


    def abrir_proceso(self):
        if not self.ultimo_resultado:
            messagebox.showinfo("Proceso Gaussiano", "Primero resuelva un sistema para poder mostrar el proceso paso a paso.")
            return
        self.vista_actual = "proceso"
        self.marcar_sidebar_activa("proceso")
        VentanaProceso(self.root, self.ultimo_resultado["pasos"], int(self.numero_variables.get()), titulo="Proceso Gaussiano • Paso a paso")

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
            "Programa 3 - Calculadora de Álgebra Lineal\n\n"
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

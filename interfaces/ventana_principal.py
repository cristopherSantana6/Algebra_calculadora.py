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
    es_homogeneo,
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
    trasponer_matriz,
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
from interfaces.ventana_matriz import crear_matriz_visual, crear_vector_visual
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
        self.ultimo_analisis = None
        # Modo calculadora en Matrices: último resultado y qué representa cada matriz.
        self.ultimo_resultado_matriz = None
        self.ultima_expresion = None
        self.expresion_a = "A"
        self.expresion_b = "B"
        self.filas_mv = tk.IntVar(value=3)
        self.columnas_mv = tk.IntVar(value=3)
        self.vista_actual = "entrada"
        self.tema_actual = "Océano"
        self.botones_sidebar = {}
        self.sidebar_expandida = False
        self.ancho_sidebar_colapsada = 235
        self.ancho_sidebar_expandida = 365
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
        estilo.configure("MatrixCell.TLabel", background=self.WHITE, foreground=self.DARK,
                         font=("Cambria Math", 11, "bold"), relief="solid", borderwidth=1)
        estilo.configure("MatrixSeparator.TLabel", background=self.SURFACE_ALT, foreground=self.DARK)
        estilo.configure("AnalysisStep.TFrame", background=self.WHITE, relief="solid", borderwidth=1)
        estilo.configure("AnalysisStepTitle.TLabel", background=self.WHITE, foreground=self.TEAL_DARK,
                         font=("Segoe UI", 11, "bold"))
        estilo.configure("AnalysisBody.TLabel", background=self.WHITE, foreground=self.DARK,
                         font=("Segoe UI", 10))
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
        """Ventana completa de personalización con botones coloreados y desplazamiento."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Tema y colores")
        ventana.geometry("780x720")
        ventana.minsize(700, 620)
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.configure(bg=self.BACKGROUND)

        encabezado = ttk.Frame(ventana, padding=(28, 22, 28, 12), style="Top.TFrame")
        encabezado.pack(fill="x")
        ttk.Label(
            encabezado, text="Personaliza tu estudio",
            style="Header.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            encabezado,
            text="Selecciona una combinación prediseñada o modifica los colores principales de la aplicación.",
            style="HeaderSub.TLabel", wraplength=680
        ).pack(anchor="w", pady=(4, 0))

        # Área desplazable para que ningún control quede fuera de la pantalla.
        contenedor = ttk.Frame(ventana)
        contenedor.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        canvas = tk.Canvas(
            contenedor, bg=self.BACKGROUND, highlightthickness=0, bd=0
        )
        barra = ttk.Scrollbar(
            contenedor, orient="vertical", command=canvas.yview
        )
        interior = ttk.Frame(canvas, style="TFrame")
        interior.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        ventana_canvas = canvas.create_window(
            (0, 0), window=interior, anchor="nw"
        )
        canvas.configure(yscrollcommand=barra.set)
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(ventana_canvas, width=e.width)
        )
        canvas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        def rueda(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", rueda)

        pred = ttk.Frame(interior, style="Card.TFrame", padding=18)
        pred.pack(fill="x", pady=(0, 12))
        ttk.Label(
            pred, text="Combinaciones prediseñadas",
            style="SectionTitle.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            pred,
            text="Cada botón utiliza el color principal real de la combinación.",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(3, 12))

        botones = ttk.Frame(pred, style="Card.TFrame")
        botones.pack(fill="x")
        for i, (nombre, paleta) in enumerate(self.TEMAS.items()):
            if nombre == "Personalizado":
                continue
            color = paleta["primary"]
            boton = tk.Button(
                botones,
                text=nombre,
                bg=color,
                fg="white",
                activebackground=paleta["primary_dark"],
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 10, "bold"),
                padx=14, pady=10,
                cursor="hand2",
                command=lambda n=nombre: self.aplicar_tema(n) or cerrar()
            )
            boton.grid(
                row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew"
            )
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)

        personalizado = ttk.Frame(interior, style="Card.TFrame", padding=18)
        personalizado.pack(fill="x", pady=(0, 12))
        ttk.Label(
            personalizado, text="Combinación personalizada",
            style="SectionTitle.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            personalizado,
            text="Pulsa cada botón para elegir un color. La muestra cambia inmediatamente.",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(3, 12))

        base = self.TEMAS.get(
            self.tema_actual, self.TEMAS["Océano"]
        ).copy()
        if self.tema_actual == "Personalizado" and hasattr(
            self, "paleta_personalizada"
        ):
            base = self.paleta_personalizada.copy()

        elecciones = [
            ("Fondo", "background"),
            ("Barra lateral", "sidebar"),
            ("Color principal", "primary"),
            ("Color de acento", "accent"),
        ]
        muestras = {}

        for fila, (texto, clave) in enumerate(elecciones):
            fila_frame = ttk.Frame(personalizado, style="Card.TFrame")
            fila_frame.pack(fill="x", pady=5)

            tk.Button(
                fila_frame,
                text=texto,
                bg=base[clave],
                fg="white" if clave != "background" else "#222222",
                activebackground=base[clave],
                relief="flat",
                bd=0,
                highlightthickness=0,
                font=("Segoe UI", 10, "bold"),
                width=22,
                padx=8, pady=7,
                command=lambda c=clave: elegir_color(c)
            ).pack(side="left")

            muestra = tk.Label(
                fila_frame,
                text=base[clave].upper(),
                bg=base[clave],
                fg="white" if clave != "background" else "#222222",
                relief="flat", bd=0, highlightthickness=0,
                width=16, padx=8, pady=7,
                font=("Consolas", 9, "bold")
            )
            muestra.pack(side="left", padx=12)
            muestras[clave] = (muestra, fila_frame.winfo_children()[0])

        def elegir_color(clave):
            color = colorchooser.askcolor(
                title=f"Elegir {clave}",
                initialcolor=base[clave],
                parent=ventana
            )[1]
            if color:
                base[clave] = color
                muestra, boton = muestras[clave]
                oscuro = clave != "background"
                muestra.configure(
                    bg=color,
                    fg="white" if oscuro else "#222222",
                    text=color.upper()
                )
                boton.configure(
                    bg=color,
                    activebackground=color,
                    fg="white" if oscuro else "#222222"
                )

        def cerrar():
            try:
                canvas.unbind_all("<MouseWheel>")
            except tk.TclError:
                pass
            ventana.destroy()

        def guardar_personalizado():
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
            personalizado["header"] = base["background"]
            self.paleta_personalizada = personalizado.copy()
            self.TEMAS["Personalizado"] = personalizado
            self.aplicar_tema("Personalizado", personalizado)
            cerrar()

        botones_finales = ttk.Frame(interior, style="TFrame")
        botones_finales.pack(fill="x", pady=(0, 20))
        ttk.Button(
            botones_finales,
            text="Guardar combinación personalizada",
            style="Accent.TButton",
            command=guardar_personalizado
        ).pack(side="left")
        ttk.Button(
            botones_finales, text="Cerrar", command=cerrar
        ).pack(side="right")

        # Permite desplazar con la rueda solo mientras la ventana está abierta.
        canvas.focus_set()

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
            text="Programa 4 • Álgebra Lineal (MTM0120) • Grupo 4",
            style="Footer.TLabel",
        ).pack(fill="x", padx=24, pady=(0, 8))

    def ampliar_sidebar(self):
        """Amplía una sola vez la barra lateral para mostrar completos los nombres."""
        if self.sidebar_expandida:
            return
        self.sidebar_expandida = True
        self.sidebar.configure(width=self.ancho_sidebar_expandida)
        self.sidebar.pack_propagate(False)
        # La opción de expansión desaparece después de utilizarse; no se crea
        # un segundo control de contracción para mantener la interfaz sencilla.
        if hasattr(self, "boton_ampliar_sidebar"):
            self.boton_ampliar_sidebar.destroy()

    def construir_sidebar(self):
        self.sidebar = ttk.Frame(self.contenedor, width=self.ancho_sidebar_colapsada, style="Sidebar.TFrame", padding=(16, 20))
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ttk.Label(self.sidebar, text="ESTUDIO", style="Sidebar.TLabel", font=("Segoe UI", 9, "bold" )).pack(anchor="w", pady=(0, 2))
        ttk.Label(self.sidebar, text="Álgebra Lineal", style="SidebarTitle.TLabel").pack(anchor="w", pady=(0, 12))

        self.boton_ampliar_sidebar = ttk.Button(
            self.sidebar, text="»  Ampliar menú", style="Sidebar.TButton",
            command=self.ampliar_sidebar
        )
        self.boton_ampliar_sidebar.pack(fill="x", pady=(0, 16))

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

        ttk.Label(self.sidebar, text="PROGRAMA 4", style="Sidebar.TLabel", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Label(self.sidebar, text="Álgebra Vectorial y Matricial", style="Sidebar.TLabel").pack(anchor="w", pady=(4, 14))

        ttk.Button(self.sidebar, text="?   Información del grupo", style="Sidebar.TButton", command=self.mostrar_info).pack(fill="x", pady=3)
        ttk.Button(self.sidebar, text="●   Tema y colores", style="Sidebar.TButton", command=self.abrir_personalizacion_colores).pack(fill="x", pady=3)

        ttk.Label(self.sidebar, text="\nUniversidad Americana\nFacultad de Ingeniería y Arquitectura", style="Sidebar.TLabel", justify="left").pack(side="bottom", anchor="w")

    def construir_header(self):
        header = ttk.Frame(self.area, padding=(24, 18), style="Top.TFrame")
        header.pack(fill="x")

        ttk.Label(header, text="Estudio de Álgebra Lineal", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Operaciones Vectoriales y Matriciales  •  Programa 4  •  Grupo 4", style="HeaderSub.TLabel").pack(anchor="w", pady=(2, 0))

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
        """Vista global de análisis, procedimiento y resultado final."""
        self.vista_resultados = self.nueva_vista()
        self.vista_resultados.columnconfigure(0, weight=1)
        self.vista_resultados.columnconfigure(1, weight=2)
        self.vista_resultados.rowconfigure(0, weight=1)

        izquierda = Tarjeta(
            self.vista_resultados,
            "Análisis de Resultados",
            "Aquí se explica qué se resolvió, qué tipo de ejercicio es y por qué se obtiene ese resultado."
        )
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        derecha = Tarjeta(
            self.vista_resultados,
            "Procedimiento",
            "Cada operación se muestra paso a paso con matrices y vectores visuales."
        )
        derecha.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.resultado_resumen = ttk.Frame(
            izquierda, style="Card.TFrame"
        )
        self.resultado_resumen.pack(fill="both", expand=True, pady=(14, 0))

        self.analisis_resumen = ttk.Frame(
            derecha, style="Card.TFrame"
        )
        self.analisis_resumen.pack(fill="both", expand=True, pady=(14, 0))

        self.mostrar_resultado_placeholder()

    def mostrar_resultado_placeholder(self):
        for widget in self.resultado_resumen.winfo_children():
            widget.destroy()
        ttk.Label(
            self.resultado_resumen,
            text="Sin datos",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(30, 5))
        ttk.Label(
            self.resultado_resumen,
            text="Realice un ejercicio desde cualquiera de los módulos para ver aquí su análisis completo.",
            style="CardSubtitle.TLabel",
            wraplength=330,
        ).pack(anchor="w")

        for widget in self.analisis_resumen.winfo_children():
            widget.destroy()
        ttk.Label(
            self.analisis_resumen,
            text="Todavía no hay procedimiento.",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=30)

    def _crear_area_desplazable(self, parent):
        """Crea un área vertical desplazable para procedimientos largos."""
        contenedor = ttk.Frame(parent, style="Card.TFrame")
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            contenedor, bg=self.WHITE, highlightthickness=0, bd=0
        )
        barra = ttk.Scrollbar(
            contenedor, orient="vertical", command=canvas.yview
        )
        interior = ttk.Frame(canvas, style="Card.TFrame")
        interior.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        ventana = canvas.create_window((0, 0), window=interior, anchor="nw")
        canvas.configure(yscrollcommand=barra.set)
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(ventana, width=e.width)
        )
        canvas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        def rueda(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # El desplazamiento queda ligado al área que contiene el cursor,
        # evitando mover otras ventanas de la aplicación.
        def entrar(_event):
            canvas.bind_all("<MouseWheel>", rueda)

        def salir(_event):
            try:
                canvas.unbind_all("<MouseWheel>")
            except tk.TclError:
                pass

        canvas.bind("<Enter>", entrar)
        canvas.bind("<Leave>", salir)
        return interior

    def _agregar_seccion_analisis(self, parent, titulo, descripcion=None):
        tarjeta = ttk.Frame(
            parent, style="AnalysisStep.TFrame", padding=14
        )
        tarjeta.pack(fill="x", padx=4, pady=6)
        ttk.Label(
            tarjeta, text=titulo, style="AnalysisStepTitle.TLabel"
        ).pack(anchor="w")
        if descripcion:
            ttk.Label(
                tarjeta, text=descripcion, style="AnalysisBody.TLabel",
                wraplength=650
            ).pack(anchor="w", pady=(4, 8))
        return tarjeta

    def mostrar_analisis_completo(self, datos, ir_a_resultados=True):
        """Renderiza un procedimiento estructurado sin depender de texto monoespaciado."""
        self.ultimo_analisis = datos

        for widget in self.resultado_resumen.winfo_children():
            widget.destroy()
        for widget in self.analisis_resumen.winfo_children():
            widget.destroy()

        resumen = self.resultado_resumen
        ttk.Label(
            resumen, text=datos.get("tipo", "Ejercicio"),
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(8, 5))
        ttk.Label(
            resumen, text=datos.get("veredicto", ""),
            style="Status.TLabel" if datos.get("positivo", True) else "StatusBad.TLabel",
            padding=10, wraplength=330
        ).pack(anchor="w", pady=(4, 12))

        for etiqueta, valor in datos.get("metricas", []):
            fila = ttk.Frame(resumen, style="Card.TFrame")
            fila.pack(fill="x", pady=3)
            ttk.Label(
                fila, text=etiqueta, style="CardSubtitle.TLabel"
            ).pack(side="left")
            ttk.Label(
                fila, text=str(valor), style="MetricValue.TLabel"
            ).pack(side="right")

        if datos.get("explicacion"):
            marco = self._agregar_seccion_analisis(
                resumen, "¿Por qué?", datos["explicacion"]
            )
            marco.pack(fill="x", padx=0, pady=(18, 0))

        interior = self._crear_area_desplazable(self.analisis_resumen)
        for paso in datos.get("pasos_visuales", []):
            tarjeta = self._agregar_seccion_analisis(
                interior,
                paso.get("titulo", "Paso"),
                paso.get("descripcion")
            )

            if paso.get("matriz") is not None:
                matriz = crear_matriz_visual(
                    tarjeta,
                    paso["matriz"],
                    paso.get("numero_variables")
                )
                matriz.pack(anchor="center", pady=(6, 8))

            if paso.get("vector") is not None:
                vec = crear_vector_visual(
                    tarjeta, paso["vector"], paso.get("vector_titulo")
                )
                vec.pack(anchor="center", pady=(6, 8))

            if paso.get("ecuacion"):
                ttk.Label(
                    tarjeta,
                    text=paso["ecuacion"],
                    style="Operation.TLabel",
                    wraplength=650,
                ).pack(anchor="w", pady=(4, 4))

            if paso.get("nota"):
                ttk.Label(
                    tarjeta,
                    text=paso["nota"],
                    style="AnalysisBody.TLabel",
                    wraplength=650,
                ).pack(anchor="w", pady=(4, 2))

        # Los módulos que ya muestran su procedimiento en su propio panel
        # pasan ir_a_resultados=False para que el usuario no pierda la vista.
        if ir_a_resultados:
            self.mostrar_vista("resultados")

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

    def nombrar_variables(self, indices, letra):
        """Convierte índices de columna (0, 2) en nombres como «c₁, c₃»."""
        if not indices:
            return "ninguna"
        return ", ".join(self.subindice(letra, j + 1) for j in indices)

    def formatear_relacion(self, coeficientes, letra="v"):
        """Escribe c₁v₁ + ... + cₖvₖ = 0 como en papel, por ejemplo v₁ − 2v₂ + v₃ = 0."""
        texto = ""
        for i, coef in enumerate(coeficientes):
            if coef == 0:
                continue
            magnitud = abs(coef)
            if magnitud == 1:
                factor = ""
            elif magnitud.denominator == 1:
                factor = formatear_numero(magnitud)
            else:
                factor = f"({formatear_numero(magnitud)})"
            termino = f"{factor}{self.subindice(letra, i + 1)}"
            if not texto:
                texto = f"−{termino}" if coef < 0 else termino
            else:
                texto += f" − {termino}" if coef < 0 else f" + {termino}"
        return f"{texto} = 0"

    def formatear_vector_columna(self, vector):
        """Presenta un vector como columna para acercarlo a la notación matemática."""
        return "[\n" + "\n".join(f"  {formatear_numero(x):>6}" for x in vector) + "\n]"

    def evaluar_dependencia_lineal(self):
        """Resuelve el sistema homogéneo Vc=0 y determina L.I. o L.D."""
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
        rango = resultado["rango"]
        libres = resultado["variables_libres"]
        basicas = resultado["columnas_pivote"]
        matriz_homogenea = resultado["matriz"]
        matriz_columnas = resultado["matriz_columnas"]
        reducida = resultado["reducida"]
        tipo_sistema = "homogéneo" if resultado["homogeneo"] else "heterogéneo"
        texto_basicas = self.nombrar_variables(basicas, "c")
        texto_libres = self.nombrar_variables(libres, "c")

        if resultado["independiente"]:
            veredicto = (
                "✓ L.I. — Los vectores son linealmente independientes.\n"
                f"Sistema {tipo_sistema} V·c = 0: solo tiene la solución trivial c = 0."
            )
            positivo = True
            explicacion = (
                f"El sistema es {tipo_sistema} porque todos sus términos "
                "independientes son 0; por eso siempre es consistente "
                "(c = 0 siempre es solución). "
                f"La forma reducida tiene {rango} pivote(s) para "
                f"{cantidad} vector(es). Como rango = cantidad de vectores, "
                "cada variable tiene pivote, no hay variables libres y "
                "V·c = 0 solo admite la solución trivial."
            )
        else:
            veredicto = (
                "⚠ L.D. — Los vectores son linealmente dependientes.\n"
                f"Sistema {tipo_sistema} V·c = 0: tiene infinitas soluciones (no triviales)."
            )
            positivo = False
            explicacion = (
                f"El sistema es {tipo_sistema} porque todos sus términos "
                "independientes son 0; por eso siempre es consistente. "
                f"La forma reducida tiene {rango} pivote(s) para "
                f"{cantidad} vector(es). Como rango < cantidad de vectores, "
                f"existen {len(libres)} variable(s) libre(s) ({texto_libres}). "
                "Eso permite construir una solución no trivial de V·c = 0."
            )

        pasos = [{
            "titulo": "Paso 1 — Matriz de columnas",
            "descripcion": "Cada vector se coloca como una columna de V.",
            "matriz": matriz_columnas,
            "numero_variables": cantidad,
        }, {
            "titulo": "Paso 2 — Sistema homogéneo",
            "descripcion": "Se estudia V·c = 0 agregando la columna de ceros.",
            "matriz": matriz_homogenea,
            "numero_variables": cantidad,
        }]

        # El primer paso de Gauss-Jordan es la matriz inicial, que ya se
        # mostró como «Sistema homogéneo»; se omite para no repetirla.
        for i, paso in enumerate(resultado["pasos"][1:], start=3):
            pasos.append({
                "titulo": f"Paso {i} — {paso['titulo']}",
                "descripcion": paso["operacion"],
                "matriz": paso["matriz"],
                "numero_variables": cantidad,
            })

        pasos.append({
            "titulo": "Paso final — Matriz escalonada reducida",
            "descripcion": (
                f"Pivotes: {rango} (variables básicas: {texto_basicas}). "
                f"Variables libres: {len(libres)} ({texto_libres})."
            ),
            "matriz": reducida,
            "numero_variables": cantidad,
        })

        if not resultado["independiente"] and resultado.get("relacion") is not None:
            pasos.append({
                "titulo": "Relación no trivial",
                "ecuacion": self.formatear_relacion(resultado["relacion"]),
                "nota": "Como al menos un coeficiente es distinto de cero, esta relación demuestra la dependencia lineal.",
            })

        datos_analisis = {
            "tipo": "Dependencia e independencia lineal",
            "veredicto": veredicto,
            "positivo": positivo,
            "metricas": [
                ("Veredicto", "L.I." if resultado["independiente"] else "L.D."),
                ("Tipo de sistema", tipo_sistema.capitalize()),
                ("Vectores", cantidad),
                ("Dimensión", f"R^{dimension}"),
                ("Pivotes", rango),
                ("Variables básicas", texto_basicas),
                ("Variables libres", f"{len(libres)} ({texto_libres})"),
                ("Criterio", "rango = vectores" if resultado["independiente"] else "rango < vectores"),
            ],
            "explicacion": explicacion,
            "pasos_visuales": pasos,
        }
        self.mostrar_analisis_completo(datos_analisis)

        # El panel local de vectores también muestra el procedimiento visual.
        for widget in self.marco_resultado_vector.winfo_children():
            widget.destroy()
        interior = self._crear_area_desplazable(self.marco_resultado_vector)
        for paso in pasos:
            tarjeta = self._agregar_seccion_analisis(
                interior, paso["titulo"], paso.get("descripcion")
            )
            if "matriz" in paso:
                crear_matriz_visual(
                    tarjeta, paso["matriz"], paso["numero_variables"]
                ).pack(anchor="center", pady=7)
            if paso.get("ecuacion"):
                ttk.Label(
                    tarjeta, text=paso["ecuacion"],
                    style="Operation.TLabel", wraplength=500
                ).pack(anchor="center", pady=5)
            if paso.get("nota"):
                ttk.Label(
                    tarjeta, text=paso["nota"],
                    style="AnalysisBody.TLabel", wraplength=500
                ).pack(anchor="w")

    def operar_vector(self, operacion):
        """Ejecuta una operación vectorial y muestra su procedimiento."""
        a = self.leer_vector_entries(self.vector_entries)
        b = self.leer_vector_entries(self.vector_b_entries)
        if a is None or b is None:
            return

        try:
            if operacion == "suma":
                resultado = sumar_vectores(a, b)
                titulo = "Suma de vectores"
                ecuacion = "A + B"
                componentes = [
                    f"Componente {i+1}: {formatear_numero(a[i])} + "
                    f"{formatear_numero(b[i])} = {formatear_numero(resultado[i])}"
                    for i in range(len(a))
                ]
                explicacion = "Se suman las componentes correspondientes porque ambos vectores pertenecen al mismo Rⁿ."
            elif operacion == "resta":
                resultado = restar_vectores(a, b)
                titulo = "Resta de vectores"
                ecuacion = "A − B"
                componentes = [
                    f"Componente {i+1}: {formatear_numero(a[i])} − "
                    f"{formatear_numero(b[i])} = {formatear_numero(resultado[i])}"
                    for i in range(len(a))
                ]
                explicacion = "Se restan las componentes correspondientes porque ambos vectores tienen la misma dimensión."
            else:
                escalar = leer_fraccion(self.escalar.get())
                resultado = multiplicar_escalar(a, escalar)
                titulo = "Multiplicación de un vector por un escalar"
                ecuacion = f"({formatear_numero(escalar)})A"
                componentes = [
                    f"Componente {i+1}: ({formatear_numero(escalar)})"
                    f"({formatear_numero(a[i])}) = {formatear_numero(resultado[i])}"
                    for i in range(len(a))
                ]
                explicacion = "El escalar multiplica cada componente del vector y la dimensión permanece igual."
        except ValueError as error:
            messagebox.showerror("Operación inválida", str(error))
            return

        for widget in self.marco_resultado_vector.winfo_children():
            widget.destroy()
        interior = self._crear_area_desplazable(self.marco_resultado_vector)

        datos = self._agregar_seccion_analisis(
            interior, titulo, "Procedimiento componente a componente."
        )
        fila = ttk.Frame(datos, style="Card.TFrame")
        fila.pack(fill="x", pady=6)
        crear_vector_visual(fila, a, "A").pack(side="left", padx=(0, 18))
        if operacion != "escalar":
            crear_vector_visual(fila, b, "B").pack(side="left")

        paso = self._agregar_seccion_analisis(
            interior, "Paso 1 — Aplicar la operación",
            ecuacion
        )
        for componente in componentes:
            ttk.Label(
                paso, text=componente, style="AnalysisBody.TLabel"
            ).pack(anchor="w", pady=2)

        final = self._agregar_seccion_analisis(
            interior, "Paso 2 — Resultado",
            "Resultado obtenido:"
        )
        crear_vector_visual(final, resultado, ecuacion).pack(anchor="center")

        self.mostrar_analisis_completo({
            "tipo": titulo,
            "veredicto": f"Resultado: {self.formatear_vector(resultado)}",
            "positivo": True,
            "metricas": [
                ("Dimensión", f"R^{len(resultado)}"),
                ("Componentes", len(resultado)),
            ],
            "explicacion": explicacion,
            "pasos_visuales": [
                {"titulo": "Datos de entrada", "vector": a, "vector_titulo": "A"},
                {"titulo": "Resultado", "vector": resultado, "vector_titulo": ecuacion},
            ],
        }, ir_a_resultados=False)

    def evaluar_combinacion(self):
        """Determina si el vector objetivo pertenece al espacio generado."""
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

        k = len(vectores)
        n = len(b)
        pasos = [
            {
                "titulo": "Paso 1 — Construir la matriz de columnas",
                "descripcion": "Los vectores generadores se colocan como columnas de V y el vector objetivo forma la columna independiente.",
                "matriz": resultado["matriz"],
                "numero_variables": k,
            }
        ]
        for i, paso in enumerate(resultado["pasos"], start=2):
            pasos.append({
                "titulo": f"Paso {i} — {paso['titulo']}",
                "descripcion": paso["operacion"],
                "matriz": paso["matriz"],
                "numero_variables": k,
            })

        if resultado["es_combinacion"]:
            if resultado["clasificacion"] == "unica":
                coef = resultado["coeficientes"]
                coef_texto = ", ".join(
                    f"c{i+1} = {formatear_numero(v)}"
                    for i, v in enumerate(coef)
                )
                veredicto = "✓ Sí es combinación lineal y la representación es única."
                explicacion = (
                    "El sistema Vc = b es consistente y tiene un pivote para cada "
                    "variable de coeficiente, por lo que existe una única combinación."
                )
                pasos.append({
                    "titulo": "Paso final — Coeficientes",
                    "ecuacion": coef_texto,
                    "nota": "Estos coeficientes satisfacen c₁v₁ + ... + cₖvₖ = b."
                })
            else:
                libres = resultado["variables_libres"]
                libres_texto = ", ".join(
                    f"c{i+1}" for i in libres
                )
                veredicto = "✓ Sí es combinación lineal, con infinitas representaciones."
                explicacion = (
                    "El sistema es consistente, pero tiene variables libres. "
                    f"Por ello existen infinitas elecciones de coeficientes ({libres_texto})."
                )
                pasos.append({
                    "titulo": "Paso final — Variables libres",
                    "ecuacion": f"Variables libres: {libres_texto}",
                    "nota": "Las variables libres generan diferentes combinaciones que producen el mismo vector objetivo."
                })
        else:
            veredicto = "✗ No es combinación lineal."
            explicacion = (
                "El sistema Vc = b es inconsistente. Por lo tanto, no existe "
                "ninguna combinación de los vectores generadores que produzca b."
            )
            pasos.append({
                "titulo": "Paso final — Inconsistencia",
                "nota": "Se detectó una fila de la forma 0 ... 0 | c, con c ≠ 0."
            })

        for widget in self.marco_resultado_vector.winfo_children():
            widget.destroy()
        interior = self._crear_area_desplazable(self.marco_resultado_vector)
        for paso in pasos:
            tarjeta = self._agregar_seccion_analisis(
                interior, paso["titulo"], paso.get("descripcion")
            )
            if "matriz" in paso:
                crear_matriz_visual(
                    tarjeta, paso["matriz"], paso["numero_variables"]
                ).pack(anchor="center", pady=7)
            if paso.get("ecuacion"):
                ttk.Label(
                    tarjeta, text=paso["ecuacion"],
                    style="Operation.TLabel", wraplength=500
                ).pack(anchor="center", pady=5)
            if paso.get("nota"):
                ttk.Label(
                    tarjeta, text=paso["nota"],
                    style="AnalysisBody.TLabel", wraplength=500
                ).pack(anchor="w")

        if resultado["homogeneo"]:
            tipo_sistema = "Homogéneo"
            veredicto += "\nSistema homogéneo V·c = 0 (b es el vector cero)."
        else:
            tipo_sistema = "Heterogéneo"
            veredicto += "\nSistema heterogéneo V·c = b (b ≠ 0)."

        self.mostrar_analisis_completo({
            "tipo": "Combinación lineal",
            "veredicto": veredicto,
            "positivo": resultado["es_combinacion"],
            "metricas": [
                ("Tipo de sistema", tipo_sistema),
                ("Vectores generadores", k),
                ("Dimensión", f"R^{n}"),
                ("Clasificación", resultado["clasificacion"]),
                ("Variables libres", len(resultado["variables_libres"])),
            ],
            "explicacion": explicacion,
            "pasos_visuales": pasos,
        }, ir_a_resultados=False)

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
        opciones = [
            "Suma (A + B)", "Resta (A - B)", "Escalar (cA)", "Multiplicación (A · B)",
            "Traspuesta (Aᵀ)", "Traspuesta del producto (A · B)ᵀ",
        ]
        ttk.Combobox(config, textvariable=self.operacion_matriz, values=opciones, state="readonly", width=32).grid(row=3, column=0, columnspan=5, sticky="w", pady=4)
        ttk.Button(config, text="Generar matrices", style="Accent.TButton", command=self.generar_matrices).grid(row=3, column=6, padx=5)

        self.marco_matrices = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_matrices.pack(fill="both", expand=True, pady=(10, 0))
        self.marco_resultado_matriz = ttk.Frame(derecha, style="Card.TFrame")
        self.marco_resultado_matriz.pack(fill="both", expand=True, pady=(16, 0))
        ttk.Button(derecha, text="Calcular operación", style="Accent.TButton", command=self.operar_matriz).pack(anchor="w", pady=(14, 0))

        # Botones para encadenar operaciones como en una calculadora.
        acumular = ttk.Frame(derecha, style="Card.TFrame")
        acumular.pack(fill="x", pady=(8, 0))
        ttk.Button(acumular, text="Usar resultado como A", style="Accent.TButton", command=lambda: self.usar_resultado_como("A")).pack(side="left", padx=(0, 4))
        ttk.Button(acumular, text="Usar resultado como B", style="Accent.TButton", command=lambda: self.usar_resultado_como("B")).pack(side="left", padx=4)
        ttk.Button(acumular, text="Reiniciar expresión", style="Coral.TButton", command=self.reiniciar_expresion_matrices).pack(side="left", padx=(4, 0))
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

    def generar_matrices(self, conservar_expresion=False):
        """Regenera las matrices A y B de acuerdo con sus dimensiones seleccionadas.

        Al generar datos nuevos, A y B vuelven a llamarse «A» y «B». Cuando se
        carga un resultado (modo calculadora) se conserva lo que representa cada una.
        """
        try:
            fa, ca = int(self.filas_a.get()), int(self.columnas_a.get())
            fb, cb = int(self.filas_b.get()), int(self.columnas_b.get())
            if not all(1 <= x <= 8 for x in (fa, ca, fb, cb)):
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Use dimensiones entre 1 y 8.")
            return
        if not conservar_expresion:
            self.expresion_a = "A"
            self.expresion_b = "B"
        for widget in self.marco_matrices.winfo_children():
            widget.destroy()
        titulo_a = "Matriz A" if self.expresion_a == "A" else f"Matriz A = {self.expresion_a}"
        titulo_b = "Matriz B" if self.expresion_b == "B" else f"Matriz B = {self.expresion_b}"
        self.matriz_a_entries = self.crear_entradas_matriz(self.marco_matrices, fa, ca, titulo_a)
        self.matriz_b_entries = self.crear_entradas_matriz(self.marco_matrices, fb, cb, titulo_b)
        self.preparar_navegacion(self.matriz_a_entries + self.matriz_b_entries)
        ttk.Label(self.marco_matrices, text="Para cA, el escalar se toma del campo de operación.", style="CardSubtitle.TLabel").pack(anchor="w", pady=5)
        ttk.Label(self.marco_matrices, text="Para Aᵀ solo se usa la matriz A; B se ignora.", style="CardSubtitle.TLabel").pack(anchor="w")
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
        """Ejecuta una operación matricial y muestra el procedimiento visual."""
        a = self.leer_matriz_entries(self.matriz_a_entries)
        b = self.leer_matriz_entries(self.matriz_b_entries)
        if a is None or b is None:
            return

        op = self.operacion_matriz.get()
        producto = None
        comprobacion = None
        try:
            if op == "Traspuesta (Aᵀ)":
                resultado = trasponer_matriz(a)
                titulo = "Traspuesta de una matriz"
                formula = "Aᵀ"
                explicacion = (
                    "La traspuesta convierte cada fila de A en una columna: la entrada "
                    "(i, j) pasa a la posición (j, i). Si A es m×n, Aᵀ es n×m."
                )
            elif op == "Traspuesta del producto (A · B)ᵀ":
                producto = multiplicar_matrices(a, b)
                resultado = trasponer_matriz(producto)
                # Se comprueba la propiedad (AB)ᵀ = BᵀAᵀ calculando el lado derecho aparte.
                comprobacion = multiplicar_matrices(trasponer_matriz(b), trasponer_matriz(a))
                titulo = "Traspuesta del producto"
                formula = "(A · B)ᵀ"
                explicacion = (
                    "Primero se calcula A·B (las columnas de A deben coincidir con las "
                    "filas de B) y luego se traspone el resultado. Se cumple la propiedad "
                    "(A·B)ᵀ = BᵀAᵀ: el orden de los factores se invierte."
                )
            elif op == "Suma (A + B)":
                resultado = sumar_matrices(a, b)
                titulo = "Suma de matrices"
                formula = "A + B"
                explicacion = "Las matrices deben tener las mismas dimensiones y se suman sus componentes correspondientes."
            elif op == "Resta (A - B)":
                resultado = restar_matrices(a, b)
                titulo = "Resta de matrices"
                formula = "A − B"
                explicacion = "Las matrices deben tener las mismas dimensiones y se restan sus componentes correspondientes."
            elif op == "Escalar (cA)":
                c = leer_fraccion(self.escalar.get())
                resultado = multiplicar_matriz_escalar(a, c)
                titulo = "Multiplicación por escalar"
                formula = f"({formatear_numero(c)})A"
                explicacion = "El escalar multiplica cada entrada de A sin modificar sus dimensiones."
            else:
                resultado = multiplicar_matrices(a, b)
                formula = "A · B"
                titulo = "Multiplicación de matrices"
                explicacion = (
                    "Para A·B, las columnas de A deben coincidir con las filas de B. "
                    "Cada entrada cᵢⱼ se obtiene multiplicando una fila de A por una columna de B."
                )
        except ValueError as error:
            messagebox.showerror("Dimensiones incompatibles", str(error))
            return

        # Expresión acumulada: dice qué representa el resultado en función
        # de los datos originales, por ejemplo «(A·B)ᵀ + B».
        ea = self._envolver(self.expresion_a)
        eb = self._envolver(self.expresion_b)
        if op == "Traspuesta (Aᵀ)":
            expresion = f"{ea}ᵀ"
        elif op == "Traspuesta del producto (A · B)ᵀ":
            expresion = f"({ea}·{eb})ᵀ"
        elif op == "Suma (A + B)":
            expresion = f"{ea} + {eb}"
        elif op == "Resta (A - B)":
            expresion = f"{ea} − {eb}"
        elif op == "Escalar (cA)":
            expresion = f"({formatear_numero(c)}){ea}"
        else:
            expresion = f"{ea}·{eb}"
        self.ultimo_resultado_matriz = resultado
        self.ultima_expresion = expresion

        for widget in self.marco_resultado_matriz.winfo_children():
            widget.destroy()
        interior = self._crear_area_desplazable(self.marco_resultado_matriz)

        datos = self._agregar_seccion_analisis(
            interior, titulo, explicacion
        )
        fila = ttk.Frame(datos, style="Card.TFrame")
        fila.pack(fill="x", pady=6)
        usa_b = op not in ("Escalar (cA)", "Traspuesta (Aᵀ)")
        crear_matriz_visual(
            fila, a, len(a[0])
        ).pack(side="left", padx=(0, 18))
        if usa_b:
            crear_matriz_visual(
                fila, b, len(b[0])
            ).pack(side="left")

        paso = self._agregar_seccion_analisis(
            interior, "Paso 1 — Aplicar la operación",
            "Primero se calcula A · B" if producto is not None else formula
        )

        if op == "Multiplicación (A · B)":
            self._mostrar_pasos_producto(paso, a, b, resultado)
        elif op == "Traspuesta (Aᵀ)":
            self._mostrar_pasos_traspuesta(paso, a, "A", "Aᵀ")
        elif producto is not None:
            self._mostrar_pasos_producto(paso, a, b, producto)
            crear_matriz_visual(
                paso, producto, len(producto[0])
            ).pack(anchor="center", pady=6)

            paso2 = self._agregar_seccion_analisis(
                interior, "Paso 2 — Trasponer el producto",
                "Cada fila de A·B se convierte en una columna de (A·B)ᵀ."
            )
            self._mostrar_pasos_traspuesta(paso2, producto, "A·B", "(A·B)ᵀ")

            coincide = comprobacion == resultado
            comp = self._agregar_seccion_analisis(
                interior, "Comprobación — (A·B)ᵀ = BᵀAᵀ",
                "Se calcula BᵀAᵀ por separado; observe que el orden de A y B se invierte."
            )
            crear_matriz_visual(
                comp, comprobacion, len(comprobacion[0])
            ).pack(anchor="center", pady=6)
            ttk.Label(
                comp,
                text="✓ BᵀAᵀ coincide con (A·B)ᵀ." if coincide else "✗ BᵀAᵀ no coincide con (A·B)ᵀ.",
                style="Status.TLabel" if coincide else "StatusBad.TLabel",
                padding=8,
            ).pack(anchor="w", pady=(4, 0))
        else:
            for i in range(len(resultado)):
                ttk.Label(
                    paso,
                    text="   ".join(
                        f"{formatear_numero(a[i][j])}"
                        for j in range(len(a[i]))
                    ),
                    style="AnalysisBody.TLabel",
                ).pack(anchor="w", pady=2)

        final = self._agregar_seccion_analisis(
            interior, f"Paso final — Resultado = {expresion}",
            "Puede seguir operando con «Usar resultado como A» o «como B»."
        )
        crear_matriz_visual(
            final, resultado, len(resultado[0])
        ).pack(anchor="center", pady=6)

        metricas = [("Expresión", expresion), ("Dimensión A", f"{len(a)}×{len(a[0])}")]
        if usa_b:
            metricas.append(("Dimensión B", f"{len(b)}×{len(b[0])}"))
        if producto is not None:
            metricas.append(("Dimensión A·B", f"{len(producto)}×{len(producto[0])}"))
        metricas.append(("Dimensión resultado", f"{len(resultado)}×{len(resultado[0])}"))
        if comprobacion is not None:
            metricas.append(("(A·B)ᵀ = BᵀAᵀ", "Verificada" if comprobacion == resultado else "No coincide"))

        pasos_visuales = [{"titulo": "Datos de entrada", "matriz": a, "numero_variables": len(a[0])}]
        if producto is not None:
            pasos_visuales.append({"titulo": "Producto A·B", "matriz": producto, "numero_variables": len(producto[0])})
        pasos_visuales.append({"titulo": "Resultado", "matriz": resultado, "numero_variables": len(resultado[0])})

        self.mostrar_analisis_completo({
            "tipo": titulo,
            "veredicto": f"Resultado {expresion} calculado correctamente.",
            "positivo": True,
            "metricas": metricas,
            "explicacion": explicacion,
            "pasos_visuales": pasos_visuales,
        }, ir_a_resultados=False)

    @staticmethod
    def _envolver(expresion):
        """Pone paréntesis a una expresión compuesta para poder seguir operándola."""
        return expresion if expresion in ("A", "B") else f"({expresion})"

    def usar_resultado_como(self, destino):
        """Copia el último resultado en A o B para encadenar otra operación."""
        if self.ultimo_resultado_matriz is None:
            messagebox.showinfo(
                "Sin resultado",
                "Primero calcule una operación; luego podrá usar su resultado como A o B."
            )
            return

        resultado = self.ultimo_resultado_matriz
        # Se guarda lo escrito en ambas matrices para no perder la que no cambia.
        texto_a = [[e.get() for e in fila] for fila in self.matriz_a_entries]
        texto_b = [[e.get() for e in fila] for fila in self.matriz_b_entries]
        texto_resultado = [[formatear_numero(x) for x in fila] for fila in resultado]

        # El resultado puede tener otra dimensión (p. ej. Aᵀ de 2×3 pasa a 3×2).
        if destino == "A":
            self.filas_a.set(len(resultado))
            self.columnas_a.set(len(resultado[0]))
            self.expresion_a = self.ultima_expresion
            texto_a = texto_resultado
        else:
            self.filas_b.set(len(resultado))
            self.columnas_b.set(len(resultado[0]))
            self.expresion_b = self.ultima_expresion
            texto_b = texto_resultado

        self.generar_matrices(conservar_expresion=True)
        self._rellenar_matrices(texto_a, texto_b)

        self.mostrar_resultado_matriz(
            f"Resultado cargado en {destino}:  {destino} = {self.ultima_expresion}\n\n"
            "Elija la siguiente operación y presione «Calcular operación»."
        )

    def _rellenar_matrices(self, texto_a, texto_b):
        """Escribe los valores dados en las casillas de A y B."""
        for entradas, valores in ((self.matriz_a_entries, texto_a), (self.matriz_b_entries, texto_b)):
            for fila_entradas, fila_valores in zip(entradas, valores):
                for entrada, valor in zip(fila_entradas, fila_valores):
                    entrada.delete(0, "end")
                    entrada.insert(0, valor)

    def reiniciar_expresion_matrices(self):
        """Vuelve a llamar «A» y «B» a las matrices sin borrar sus valores."""
        texto_a = [[e.get() for e in fila] for fila in self.matriz_a_entries]
        texto_b = [[e.get() for e in fila] for fila in self.matriz_b_entries]
        self.ultimo_resultado_matriz = None
        self.ultima_expresion = None
        self.generar_matrices()
        self._rellenar_matrices(texto_a, texto_b)

    def _mostrar_pasos_producto(self, parent, a, b, producto):
        """Muestra cada entrada cᵢⱼ de A·B como fila de A por columna de B."""
        for i in range(len(a)):
            for j in range(len(b[0])):
                terminos = " + ".join(
                    f"({formatear_numero(a[i][k])})({formatear_numero(b[k][j])})"
                    for k in range(len(a[0]))
                )
                ttk.Label(
                    parent,
                    text=f"c{i+1},{j+1} = {terminos} = {formatear_numero(producto[i][j])}",
                    style="AnalysisBody.TLabel",
                    wraplength=650,
                ).pack(anchor="w", pady=2)

    def _mostrar_pasos_traspuesta(self, parent, matriz, nombre, nombre_traspuesta):
        """Explica la traspuesta fila por fila: la fila i pasa a ser la columna i."""
        for i, fila in enumerate(matriz):
            valores = ", ".join(formatear_numero(x) for x in fila)
            ttk.Label(
                parent,
                text=f"Fila {i+1} de {nombre}: ({valores})  →  columna {i+1} de {nombre_traspuesta}",
                style="AnalysisBody.TLabel",
                wraplength=650,
            ).pack(anchor="w", pady=2)
        ttk.Label(
            parent,
            text=f"Dimensión: {len(matriz)}×{len(matriz[0])}  →  {len(matriz[0])}×{len(matriz)}",
            style="Operation.TLabel",
        ).pack(anchor="w", pady=(6, 2))

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
            "Procedimiento",
            "Muestra el cálculo paso a paso, la igualdad distributiva y la combinación lineal de las columnas."
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

    def mostrar_resultado_matriz_vector(self, datos):
        """Muestra el procedimiento A·v con componentes visuales."""
        for widget in self.marco_resultado_matriz_vector.winfo_children():
            widget.destroy()

        if isinstance(datos, str):
            ttk.Label(
                self.marco_resultado_matriz_vector,
                text=datos,
                style="CardSubtitle.TLabel",
                wraplength=520,
            ).pack(anchor="w", pady=20)
            return

        interior = self._crear_area_desplazable(self.marco_resultado_matriz_vector)

        titulo = self._agregar_seccion_analisis(
            interior,
            datos["titulo"],
            datos.get("descripcion")
        )

        fila_datos = ttk.Frame(titulo, style="Card.TFrame")
        fila_datos.pack(fill="x", pady=(6, 0))
        crear_matriz_visual(
            fila_datos, datos["matriz"], len(datos["matriz"][0])
        ).pack(side="left", padx=(0, 18))
        crear_vector_visual(
            fila_datos, datos["vector"], "Vector v"
        ).pack(side="left")

        if datos.get("suma"):
            ttk.Label(
                titulo, text="Primero se calcula u + v:",
                style="AnalysisBody.TLabel"
            ).pack(anchor="w", pady=(10, 3))
            crear_vector_visual(
                titulo, datos["suma"], "u + v"
            ).pack(anchor="w")

        for paso in datos.get("pasos", []):
            tarjeta = self._agregar_seccion_analisis(
                interior,
                paso["titulo"],
                paso.get("descripcion")
            )
            if paso.get("ecuacion"):
                ttk.Label(
                    tarjeta,
                    text=paso["ecuacion"],
                    style="Operation.TLabel",
                    wraplength=650,
                ).pack(anchor="w", pady=(3, 7))
            if paso.get("vector") is not None:
                crear_vector_visual(
                    tarjeta, paso["vector"], paso.get("vector_titulo")
                ).pack(anchor="center", pady=5)
            if paso.get("componentes"):
                for componente in paso["componentes"]:
                    ttk.Label(
                        tarjeta,
                        text=componente,
                        style="AnalysisBody.TLabel",
                        wraplength=650,
                    ).pack(anchor="w", pady=2)

        final = self._agregar_seccion_analisis(
            interior, "Resultado final", datos.get("final_texto")
        )
        crear_vector_visual(
            final, datos["resultado"], "Resultado"
        ).pack(anchor="center", pady=6)

    def _paso_producto_fila(self, fila, vector, numero_fila):
        terminos = " + ".join(
            f"({formatear_numero(a)})({formatear_numero(b)})"
            for a, b in zip(fila, vector)
        )
        resultado = sum(
            (a * b for a, b in zip(fila, vector)), 0
        )
        return (
            f"Fila {numero_fila}: {terminos} = "
            f"{formatear_numero(resultado)}"
        )

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

        columnas = [
            [fila[j] for fila in matriz]
            for j in range(len(v))
        ]
        combinacion = " + ".join(
            f"({formatear_numero(coef)})C{j + 1}"
            for j, coef in enumerate(v)
        )
        componentes = [
            self._paso_producto_fila(fila, v, i + 1)
            for i, fila in enumerate(matriz)
        ]

        datos_resultado = {
            "titulo": "Procedimiento: producto matriz · vector",
            "descripcion": "Se calcula cada componente de A·v mediante el producto fila por columna.",
            "matriz": matriz,
            "vector": v,
            "resultado": resultado,
            "pasos": [
                {
                    "titulo": "Paso 1 — Producto fila por columna",
                    "descripcion": "Cada fila de A se multiplica componente a componente por v y luego se suman los productos.",
                    "componentes": componentes,
                },
                {
                    "titulo": "Paso 2 — Interpretación como combinación lineal",
                    "descripcion": "Los componentes de v funcionan como escalares de las columnas de A.",
                    "ecuacion": f"A·v = {combinacion}",
                },
                {
                    "titulo": "Paso 3 — Columnas de A",
                    "descripcion": "Se identifican las columnas y se multiplican por sus respectivos coeficientes.",
                    "componentes": [
                        f"({formatear_numero(coef)})C{j + 1} = "
                        f"{self.formatear_vector_columna(columna)}"
                        for j, (coef, columna) in enumerate(zip(v, columnas))
                    ],
                },
            ],
            "final_texto": f"Por tanto, A·v = {combinacion}.",
        }
        self.mostrar_resultado_matriz_vector(datos_resultado)

        self.mostrar_analisis_completo({
            "tipo": "Producto matriz · vector",
            "veredicto": "Producto calculado correctamente.",
            "positivo": True,
            "metricas": [
                ("Dimensión de A", f"{len(matriz)}×{len(matriz[0])}"),
                ("Dimensión de v", f"{len(v)} componentes"),
            ],
            "explicacion": "Cada componente del resultado se obtiene con el producto de una fila de A por el vector v. Además, A·v puede interpretarse como una combinación lineal de las columnas de A usando las entradas de v como escalares.",
            "pasos_visuales": [
                {
                    "titulo": "Matriz A y vector v",
                    "matriz": matriz,
                    "numero_variables": len(v),
                    "vector": v,
                    "vector_titulo": "v",
                },
                {
                    "titulo": "Resultado A·v",
                    "vector": resultado,
                    "vector_titulo": "A·v",
                    "descripcion": f"A·v = {combinacion}",
                },
            ],
        }, ir_a_resultados=False)

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
        datos_resultado = {
            "titulo": "Procedimiento: propiedad distributiva",
            "descripcion": "Se verifica A(u + v) = Au + Av calculando ambos lados por separado.",
            "matriz": matriz,
            "vector": v,
            "suma": suma,
            "resultado": izquierda,
            "pasos": [
                {
                    "titulo": "Paso 1 — Sumar los vectores",
                    "ecuacion": "u + v",
                    "vector": suma,
                    "vector_titulo": "u + v",
                },
                {
                    "titulo": "Paso 2 — Calcular A(u + v)",
                    "vector": izquierda,
                    "vector_titulo": "A(u + v)",
                },
                {
                    "titulo": "Paso 3 — Calcular Au y Av",
                    "componentes": [
                        f"Au = {self.formatear_vector_columna(au)}",
                        f"Av = {self.formatear_vector_columna(av)}",
                    ],
                },
                {
                    "titulo": "Paso 4 — Sumar Au + Av",
                    "vector": derecha,
                    "vector_titulo": "Au + Av",
                },
            ],
            "final_texto": (
                "✓ Se cumple A(u + v) = Au + Av."
                if cumple else
                "✗ No coincide; revise las dimensiones y los datos."
            ),
        }
        self.mostrar_resultado_matriz_vector(datos_resultado)

        self.mostrar_analisis_completo({
            "tipo": "Verificación de propiedad distributiva",
            "veredicto": "La propiedad se verifica." if cumple else "La igualdad no coincide.",
            "positivo": cumple,
            "metricas": [
                ("A(u + v)", self.formatear_vector(izquierda)),
                ("Au + Av", self.formatear_vector(derecha)),
            ],
            "explicacion": "La propiedad distributiva del producto matriz–vector establece que multiplicar A por la suma de dos vectores produce el mismo resultado que sumar los productos Au y Av.",
            "pasos_visuales": [
                {"titulo": "u + v", "vector": suma, "vector_titulo": "u + v"},
                {"titulo": "Lado izquierdo", "vector": izquierda, "vector_titulo": "A(u + v)"},
                {"titulo": "Lado derecho", "vector": derecha, "vector_titulo": "Au + Av"},
            ],
        }, ir_a_resultados=False)

    def construir_vista_propiedades(self):
        """Construye el módulo para verificar las 8 propiedades solicitadas,
        más un contraejemplo (A·B = B·A) donde la igualdad puede fallar."""
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
            "9. ¿Conmutatividad del producto?: A · B = B · A",
        ]
        combo = ttk.Combobox(config, textvariable=self.propiedad_seleccionada, values=propiedades, state="readonly", width=58)
        combo.grid(row=3, column=0, columnspan=5, sticky="ew", pady=4)
        ttk.Button(config, text="Resolver propiedad", style="Accent.TButton", command=self.operar_propiedad).grid(row=3, column=5, padx=(8, 0))

        # El área de entrada de propiedades también es desplazable, igual que
        # el procedimiento paso a paso. Esto evita que matrices, vectores y
        # controles inferiores queden fuera de la pantalla.
        self.marco_propiedades = self._crear_area_desplazable(izquierda)
        self.marco_propiedades.pack_configure(pady=(8, 0))
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

    def mostrar_resultado_propiedad(self, datos):
        for widget in self.marco_resultado_propiedad.winfo_children():
            widget.destroy()

        if isinstance(datos, str):
            ttk.Label(
                self.marco_resultado_propiedad,
                text=datos, style="CardSubtitle.TLabel",
                wraplength=480
            ).pack(anchor="w", pady=20)
            return

        interior = self._crear_area_desplazable(self.marco_resultado_propiedad)
        titulo = self._agregar_seccion_analisis(
            interior, datos["titulo"], datos["detalle"]
        )

        fila = ttk.Frame(titulo, style="Card.TFrame")
        fila.pack(fill="x", pady=8)

        izq = ttk.Frame(fila, style="Card.TFrame")
        izq.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(
            izq, text="Lado izquierdo", style="SectionTitle.TLabel"
        ).pack(anchor="w")
        self._mostrar_valor_visual(izq, datos["izquierda"])

        der = ttk.Frame(fila, style="Card.TFrame")
        der.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ttk.Label(
            der, text="Lado derecho", style="SectionTitle.TLabel"
        ).pack(anchor="w")
        self._mostrar_valor_visual(der, datos["derecha"])

        estado = "✓ Igualdad verificada." if datos["cumple"] else "✗ La igualdad no coincide."
        ttk.Label(
            interior, text=estado,
            style="Status.TLabel" if datos["cumple"] else "StatusBad.TLabel",
            padding=10
        ).pack(anchor="w", pady=(8, 8))

        self._agregar_seccion_analisis(
            interior, "Dependencias de dimensión y componentes",
            datos["dependencias"]
        )

    def _mostrar_valor_visual(self, parent, valor):
        """Muestra matrices o vectores en el panel de propiedades."""
        if isinstance(valor, list) and valor and isinstance(valor[0], list):
            crear_matriz_visual(
                parent, valor, len(valor[0])
            ).pack(anchor="center", pady=6)
        elif isinstance(valor, list):
            crear_vector_visual(
                parent, valor
            ).pack(anchor="center", pady=6)
        else:
            ttk.Label(
                parent, text=str(valor), style="Operation.TLabel"
            ).pack(anchor="center", pady=6)

    def formatear_lado_propiedad(self, valor, es_vector=False):
        """Compatibilidad con versiones anteriores del módulo."""
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
                dep = "A y B deben tener exactamente las mismas dimensiones."
            elif nombre.startswith("2."):
                izquierda = sumar_matrices(sumar_matrices(A, B), C)
                derecha = sumar_matrices(A, sumar_matrices(B, C))
                titulo = "Propiedad 2 — Asociatividad de la suma"
                detalle = "(A + B) + C = A + (B + C)"
                dep = "A, B y C deben tener las mismas filas y columnas."
            elif nombre.startswith("3."):
                cero = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
                izquierda = sumar_matrices(A, cero)
                derecha = A
                titulo = "Propiedad 3 — Identidad aditiva"
                detalle = "A + 0 = A"
                dep = "La matriz cero debe tener las mismas dimensiones que A."
            elif nombre.startswith("4."):
                izquierda = multiplicar_matriz_escalar(sumar_matrices(A, B), r)
                derecha = sumar_matrices(
                    multiplicar_matriz_escalar(A, r),
                    multiplicar_matriz_escalar(B, r)
                )
                titulo = "Propiedad 4 — Distributividad del escalar"
                detalle = "r(A + B) = rA + rB"
                dep = "A y B deben compartir dimensiones; r es un escalar."
            elif nombre.startswith("5."):
                izquierda = multiplicar_matriz_escalar(A, r + s)
                derecha = sumar_matrices(
                    multiplicar_matriz_escalar(A, r),
                    multiplicar_matriz_escalar(A, s)
                )
                titulo = "Propiedad 5 — Distributividad respecto a escalares"
                detalle = "(r + s)A = rA + sA"
                dep = "r y s son escalares y A conserva sus dimensiones."
            elif nombre.startswith("6."):
                izquierda = multiplicar_matriz_escalar(
                    multiplicar_matriz_escalar(A, s), r
                )
                derecha = multiplicar_matriz_escalar(A, r * s)
                titulo = "Propiedad 6 — Asociatividad de la multiplicación escalar"
                detalle = "r(sA) = (rs)A"
                dep = "r y s son escalares; el producto no cambia las dimensiones de A."
            elif nombre.startswith("7."):
                suma_uv = sumar_vectores(u, v)
                izquierda = multiplicar_matriz_vector(A, suma_uv)
                derecha = sumar_vectores(
                    multiplicar_matriz_vector(A, u),
                    multiplicar_matriz_vector(A, v)
                )
                titulo = "Propiedad 7 — Distributividad del producto matriz–vector"
                detalle = "A(u + v) = Au + Av"
                dep = "u y v deben tener n componentes y A debe ser m×n."
            elif nombre.startswith("8."):
                cu = multiplicar_escalar(u, c)
                izquierda = multiplicar_matriz_vector(A, cu)
                derecha = multiplicar_escalar(
                    multiplicar_matriz_vector(A, u), c
                )
                titulo = "Propiedad 8 — Homogeneidad del producto matriz–vector"
                detalle = "A(cu) = c(Au)"
                dep = "u debe tener n componentes y A debe ser m×n."
            else:
                # A diferencia de las anteriores, esta igualdad NO es una
                # propiedad general: sirve para mostrar un caso donde falla.
                if len(A) != len(A[0]):
                    raise ValueError(
                        "A·B y B·A solo existen a la vez si A y B son cuadradas. "
                        "Genere los datos con filas m = columnas n."
                    )
                izquierda = multiplicar_matrices(A, B)
                derecha = multiplicar_matrices(B, A)
                titulo = "Propiedad 9 — ¿Conmutatividad del producto de matrices?"
                detalle = "A · B = B · A"
                dep = (
                    "A y B deben ser cuadradas (n×n) para que existan A·B y B·A. "
                    "Aun así, en general A·B ≠ B·A: el producto de matrices NO es "
                    "conmutativo, por lo que es normal que esta igualdad no se cumpla."
                )

        except ValueError as error:
            messagebox.showerror("Dimensiones incompatibles", str(error))
            return

        cumple = izquierda == derecha
        datos = {
            "titulo": titulo,
            "detalle": detalle,
            "izquierda": izquierda,
            "derecha": derecha,
            "cumple": cumple,
            "dependencias": dep,
        }
        self.mostrar_resultado_propiedad(datos)

        self.mostrar_analisis_completo({
            "tipo": titulo,
            "veredicto": "La propiedad se cumple." if cumple else "La igualdad no coincide.",
            "positivo": cumple,
            "metricas": [
                ("Igualdad", "Verificada" if cumple else "No coincide"),
                ("Dimensión de A", f"{len(A)}×{len(A[0])}"),
            ],
            "explicacion": f"{detalle}. {dep}",
            "pasos_visuales": [
                {
                    "titulo": "Lado izquierdo",
                    "matriz": izquierda if isinstance(izquierda, list) and izquierda and isinstance(izquierda[0], list) else None,
                    "numero_variables": len(izquierda[0]) if isinstance(izquierda, list) and izquierda and isinstance(izquierda[0], list) else None,
                    "vector": izquierda if isinstance(izquierda, list) and izquierda and not isinstance(izquierda[0], list) else None,
                },
                {
                    "titulo": "Lado derecho",
                    "matriz": derecha if isinstance(derecha, list) and derecha and isinstance(derecha[0], list) else None,
                    "numero_variables": len(derecha[0]) if isinstance(derecha, list) and derecha and isinstance(derecha[0], list) else None,
                    "vector": derecha if isinstance(derecha, list) and derecha and not isinstance(derecha[0], list) else None,
                },
            ],
        }, ir_a_resultados=False)

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
        """Muestra Ax=b de forma visual, sin una caja de texto monoespaciada."""
        matriz = self.leer_matriz()
        if matriz is None:
            return

        n = int(self.numero_variables.get())
        if not matriz or any(len(fila) != n + 1 for fila in matriz):
            messagebox.showerror(
                "Datos inválidos",
                "Primero genere una matriz aumentada válida."
            )
            return

        a = [fila[:n] for fila in matriz]
        b = [fila[n] for fila in matriz]
        x = [f"x{i + 1}" for i in range(n)]

        ventana = tk.Toplevel(self.root)
        ventana.title("Forma matricial — Ax = b")
        ventana.geometry("850x620")
        ventana.minsize(720, 520)
        ventana.transient(self.root)

        contenedor = ttk.Frame(ventana, padding=24)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor, text="Forma matricial del sistema",
            style="PageTitle.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Se separan visualmente A, x y b para mostrar cómo se construye Ax = b.",
            style="ProcessSubtitle.TLabel"
        ).pack(anchor="w", pady=(3, 15))

        cuerpo = ttk.Frame(contenedor, style="Card.TFrame", padding=20)
        cuerpo.pack(fill="both", expand=True)

        fila = ttk.Frame(cuerpo, style="Card.TFrame")
        fila.pack(expand=True)

        marco_a = self._crear_bloque_matriz(fila, "A — Matriz de coeficientes")
        crear_matriz_visual(marco_a, a, n).pack(pady=8)

        ttk.Label(
            fila, text="×", style="PageTitle.TLabel"
        ).pack(side="left", padx=16)

        marco_x = self._crear_bloque_matriz(fila, "x — Vector incógnita")
        cuerpo_x = ttk.Frame(marco_x, style="Matrix.TFrame", padding=8)
        cuerpo_x.pack(pady=8)
        for i, nombre in enumerate(x):
            ttk.Label(
                cuerpo_x, text=nombre, style="MatrixCell.TLabel",
                width=8, anchor="center", padding=(8, 6)
            ).grid(row=i, column=0, padx=2, pady=2)

        ttk.Label(
            fila, text="=", style="PageTitle.TLabel"
        ).pack(side="left", padx=16)

        marco_b = self._crear_bloque_matriz(fila, "b — Términos independientes")
        crear_vector_visual(marco_b, b, vertical=True).pack(pady=8)

        ttk.Label(
            cuerpo,
            text="Por lo tanto, el sistema se representa como  A · x = b.",
            style="Operation.TLabel"
        ).pack(anchor="center", pady=(25, 5))

        ttk.Button(
            contenedor, text="Cerrar",
            command=ventana.destroy
        ).pack(anchor="e", pady=(12, 0))

        self.mostrar_analisis_completo({
            "tipo": "Forma matricial Ax = b",
            "veredicto": "Representación matricial construida correctamente.",
            "positivo": True,
            "metricas": [
                ("Matriz A", f"{len(a)}×{len(a[0])}"),
                ("Vector x", f"{len(x)} incógnitas"),
                ("Vector b", f"{len(b)} términos"),
            ],
            "explicacion": "La matriz A contiene los coeficientes, x contiene las incógnitas y b contiene los términos independientes. Al multiplicar A por x se obtiene el vector b.",
            "pasos_visuales": [
                {"titulo": "Matriz A", "matriz": a, "numero_variables": n},
                {"titulo": "Vector b", "vector": b, "vector_titulo": "b"},
            ],
        }, ir_a_resultados=False)

    def _crear_bloque_matriz(self, parent, titulo):
        marco = ttk.Frame(parent, style="Card.TFrame")
        marco.pack(side="left", padx=6, anchor="center")
        ttk.Label(
            marco, text=titulo, style="SectionTitle.TLabel",
            wraplength=180
        ).pack(anchor="center")
        return marco

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
        self.mostrar_vista("resultados")

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
        self.mostrar_vista("resultados")


    def actualizar_resumen(self):
        """Construye el análisis completo de un sistema Ax=b."""
        resultado = self.ultimo_resultado
        if not resultado:
            return

        numero_variables = int(self.numero_variables.get())
        clasificacion = resultado["clasificacion"]
        homogeneo = es_homogeneo(resultado["matriz_original"], numero_variables)
        tipo_sistema = "homogéneo (b = 0)" if homogeneo else "heterogéneo (b ≠ 0)"

        if clasificacion == "unica":
            veredicto = f"Sistema {tipo_sistema} consistente determinado: tiene una única solución."
            if homogeneo:
                veredicto += " Es la solución trivial x = 0."
            positivo = True
        elif clasificacion == "infinita":
            veredicto = f"Sistema {tipo_sistema} consistente indeterminado: tiene infinitas soluciones."
            positivo = True
        else:
            veredicto = f"Sistema {tipo_sistema} inconsistente: no tiene solución."
            positivo = False

        pasos_visuales = []
        for i, paso in enumerate(resultado["pasos"], start=1):
            pasos_visuales.append({
                "titulo": f"Paso {i}: {paso['titulo']}",
                "descripcion": paso["operacion"],
                "matriz": paso["matriz"],
                "numero_variables": numero_variables,
            })

        pivotes = resultado["pivotes"]
        libres = resultado["variables_libres"]
        explicacion = (
            f"Se aplicó {resultado['metodo']} sobre la matriz aumentada [A|b]. "
            f"Se identificaron {len(pivotes)} pivote(s) y "
            f"{len(libres)} variable(s) libre(s). "
        )
        if clasificacion == "unica":
            explicacion += (
                "Como existe un pivote para cada variable, la solución es única. "
                "La sustitución en el sistema original "
                + ("fue correcta." if resultado["verificacion"] else "no coincidió; revise los datos.")
            )
        elif clasificacion == "infinita":
            explicacion += (
                "Como hay menos pivotes que variables y no aparece una fila "
                "0 ... 0 | c con c ≠ 0, existen variables libres y por ello infinitas soluciones."
            )
        else:
            explicacion += (
                "Se detectó una fila equivalente a 0 ... 0 | c con c ≠ 0, "
                "por lo que el sistema es incompatible."
            )

        metricas = [
            ("Tipo de sistema", "Homogéneo" if homogeneo else "Heterogéneo"),
            ("Método", resultado["metodo"]),
            ("Pivotes", len(pivotes)),
            ("Variables", numero_variables),
            ("Variables libres", len(libres)),
        ]
        if clasificacion == "unica" and resultado["solucion"] is not None:
            metricas.append((
                "Solución",
                ", ".join(
                    f"x{i+1}={formatear_numero(v)}"
                    for i, v in enumerate(resultado["solucion"])
                )
            ))
        if libres:
            metricas.append((
                "Libres",
                ", ".join(f"x{i+1}" for i in libres)
            ))

        datos = {
            "tipo": "Resolución de sistema Ax = b",
            "veredicto": veredicto,
            "positivo": positivo,
            "metricas": metricas,
            "explicacion": explicacion,
            "pasos_visuales": pasos_visuales,
        }
        self.mostrar_analisis_completo(datos)

        # La matriz final también queda disponible en la vista de procedimiento.
        self.proceso_titulo.config(
            text=f"Resultado final • {resultado['metodo']}"
        )
        self.proceso_operacion.config(
            text=resultado["pasos"][-1]["operacion"]
        )
        for widget in self.proceso_texto.winfo_children():
            widget.destroy()
        self.actualizar_texto(
            self.proceso_texto,
            "\n".join(
                formatear_matriz_lineas(
                    resultado["escalonada"], numero_variables
                )
            )
        )

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
        self.ultimo_analisis = None
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

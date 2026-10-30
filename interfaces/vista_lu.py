"""Vista Tkinter de la Factorización LU y la solución de Ax = b (Programa 6).

Pide las dimensiones, A y b con validación y reentrada, llama a modulos/modulo_lu.py y muestra L, U, y, x
y los mensajes de verificación. Incluye el logotipo ASCII y la opción «0. Ver Teoremas Clave del Módulo».
Unidad: Programa 6 de Álgebra Lineal (MTM0120), Universidad Americana.
Elaborado por: Rafael Antonio Arauz Navarro, Patricia del Carmen Oquist Talavera,
Cristopher Rafael Santana Ríos y Blanca Alejandra Zeledón Abea
"""

import tkinter as tk
from tkinter import messagebox, ttk

from interfaces.componentes.tarjeta import Tarjeta
from interfaces.dialogo_verificar_lu import DialogoVerificarLU
from interfaces.ventana_matriz import crear_matriz_visual, crear_vector_visual
from modulos.modulo_lu import factorizar_lu, resolver_con_lu, verificar_factorizacion
from utilidades.fracciones import formatear_fraccion, leer_fraccion

LOGOTIPO_ASCII = (
    "  _      _   _\n"
    " | |    | | | |\n"
    " | |    | | | |\n"
    " | |___ | |_| |\n"
    " |_____| \\___/\n"
    "   A = L · U"
)

TEOREMAS_CLAVE = (
    "A = L · U: si la eliminación no necesita intercambiar filas, A (m×n) es el producto de L (m×m, triangular "
    "inferior con unos) y U (forma escalonada de A).",
    "Cada multiplicador l = (elemento a eliminar) / (pivote) se guarda en la posición (i, j) de L.",
    "Ax = b equivale a dos sistemas triangulares: Ly = b (sustitución hacia adelante) y Ux = y "
    "(sustitución hacia atrás).",
    "Si un pivote es 0 y hay que intercambiar filas, no existe LU sin permutación: se necesita PA = LU.",
    "Sin permutaciones, det(A) = producto de la diagonal de U, porque det(L) = 1.",
    "Ax = b (A cuadrada) tiene solución única si y solo si U tiene n pivotes, es decir, su diagonal no tiene ceros.",
    "Verificaciones del módulo: L · U == A y A · x == b, con aritmética exacta (fracciones).",
)

_SUBINDICES = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _subindice(numero):
    """Escribe un entero con subíndices matemáticos (21 → ₂₁)."""
    return str(numero).translate(_SUBINDICES)


class VistaLU:
    """Vista de «Factorización LU y solución Ax = b» dentro de la calculadora."""

    def __init__(self, app):
        """Construye la vista sobre la aplicación `app`, de la que reutiliza estilos y áreas desplazables."""
        self.app = app
        self.filas = tk.IntVar(value=3)
        self.columnas = tk.IntVar(value=3)
        self.entradas = []
        self.filas_generadas = 0
        self.columnas_generadas = 0
        self.marco = app.nueva_vista()
        self._construir()

    def _construir(self):
        """Crea las dos tarjetas de la vista: entrada a la izquierda y resultados a la derecha."""
        self.marco.columnconfigure(0, weight=1)
        self.marco.columnconfigure(1, weight=1)
        self.marco.rowconfigure(0, weight=1)

        izquierda = Tarjeta(self.marco, "Factorización LU y solución Ax = b",
                            "Ingrese A (m×n) y el vector b con m componentes; acepta enteros, decimales y fracciones.")
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        derecha = Tarjeta(self.marco, "Resultado", "L, U, el vector intermedio y, la solución x y sus verificaciones.")
        derecha.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        configuracion = ttk.Frame(izquierda, style="Card.TFrame")
        configuracion.pack(fill="x", pady=(16, 8))
        ttk.Label(configuracion, text="Filas (m)", style="CardSubtitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(configuracion, text="Columnas (n)", style="CardSubtitle.TLabel").grid(
            row=0, column=2, sticky="w", padx=(20, 0))
        ttk.Spinbox(configuracion, from_=1, to=8, textvariable=self.filas, width=6).grid(
            row=1, column=0, pady=5, sticky="w")
        ttk.Spinbox(configuracion, from_=1, to=8, textvariable=self.columnas, width=6).grid(
            row=1, column=2, padx=(20, 0), pady=5, sticky="w")
        ttk.Button(configuracion, text="Generar", style="Accent.TButton", command=self.generar).grid(
            row=1, column=4, padx=(20, 0))

        self.marco_entradas = ttk.Frame(izquierda, style="Card.TFrame")
        self.marco_entradas.pack(fill="both", expand=True, pady=(8, 0))

        self.ayuda = ttk.Label(izquierda, text="", style="CardSubtitle.TLabel", wraplength=480)
        self.ayuda.pack(anchor="w", pady=(6, 0))

        botones = ttk.Frame(izquierda, style="Card.TFrame")
        botones.pack(fill="x", pady=(10, 0))
        ttk.Button(botones, text="Factorizar A = LU", style="Accent.TButton", command=self.factorizar).pack(
            side="left", fill="x", expand=True, padx=(0, 4))
        self.boton_resolver = ttk.Button(botones, text="Resolver Ax = b", style="Accent.TButton",
                                         command=self.resolver)
        self.boton_resolver.pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(botones, text="Limpiar", style="Coral.TButton", command=self.generar).pack(
            side="right", fill="x", expand=True, padx=(4, 0))
        ttk.Button(
            izquierda,
            text="Ingresar L y U manualmente y comprobar L · U = A",
            style="Op.TButton",
            command=self.abrir_verificacion_manual,
        ).pack(fill="x", pady=(8, 0))
        ttk.Button(izquierda, text="0. Ver Teoremas Clave del Módulo", style="Op.TButton",
                   command=self.mostrar_teoremas).pack(fill="x", pady=(8, 0))

        self.marco_resultado = ttk.Frame(derecha, style="Card.TFrame")
        self.marco_resultado.pack(fill="both", expand=True, pady=(16, 0))
        self.generar()

    def generar(self):
        """Genera las casillas de [A | b] con las dimensiones pedidas y limpia el resultado."""
        try:
            filas, columnas = int(self.filas.get()), int(self.columnas.get())
            if not 1 <= filas <= 8 or not 1 <= columnas <= 8:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Datos inválidos", "Use dimensiones entre 1 y 8.")
            return
        self.filas_generadas, self.columnas_generadas = filas, columnas
        for widget in self.marco_entradas.winfo_children():
            widget.destroy()

        ttk.Label(self.marco_entradas, text=f"Matriz aumentada [ A | b ]   (A es {filas}×{columnas})",
                  style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 6))
        rejilla = ttk.Frame(self.marco_entradas, style="Card.TFrame")
        rejilla.pack(anchor="w")
        self.entradas = []
        for i in range(filas):
            fila = []
            for j in range(columnas + 1):
                columna_visual = j if j < columnas else j + 1
                if j == columnas:
                    ttk.Label(rejilla, text="│", style="SectionTitle.TLabel").grid(row=i, column=columnas, padx=4)
                entrada = ttk.Entry(rejilla, width=7, justify="center")
                entrada.insert(0, "0")
                entrada.grid(row=i, column=columna_visual, padx=3, pady=3)
                fila.append(entrada)
            self.entradas.append(fila)
        self.app.preparar_navegacion(self.entradas)

        es_cuadrada = filas == columnas
        self.boton_resolver.configure(state="normal" if es_cuadrada else "disabled")
        self.ayuda.configure(
            text="" if es_cuadrada else "Resolver Ax = b requiere A cuadrada (m = n); aquí solo puede factorizar A = LU.")
        self._mostrar_inicio()

    def _leer(self):
        """Lee A y b de las casillas. Si hay un dato inválido avisa, enfoca esa casilla y devuelve None."""
        matriz_a, vector_b = [], []
        for fila in self.entradas:
            valores = []
            for entrada in fila:
                try:
                    valores.append(leer_fraccion(entrada.get()))
                except ValueError as error:
                    messagebox.showerror("Entrada inválida", str(error))
                    entrada.focus_set()
                    entrada.selection_range(0, "end")
                    return None
            matriz_a.append(valores[:-1])
            vector_b.append(valores[-1])
        return matriz_a, vector_b

    def abrir_verificacion_manual(self):
        """Abre un formulario para ingresar L y U y comprobar su producto con A."""
        matriz_a = []
        for i, fila in enumerate(self.entradas):
            valores = []
            for j, entrada in enumerate(fila[:self.columnas_generadas]):
                try:
                    valores.append(leer_fraccion(entrada.get()))
                except (ValueError, ZeroDivisionError) as error:
                    messagebox.showerror(
                        "Entrada inválida",
                        f"Matriz A, fila {i + 1}, columna {j + 1}: {error}",
                    )
                    entrada.focus_set()
                    entrada.selection_range(0, "end")
                    return
            matriz_a.append(valores)

        DialogoVerificarLU(self.app, matriz_a)

    def factorizar(self):
        """Factoriza A = LU, verifica L·U == A y muestra el resultado (o el aviso de permutación)."""
        datos = self._leer()
        if datos is None:
            return
        matriz_a, _ = datos
        try:
            factorizacion = factorizar_lu(matriz_a)
        except ValueError as error:
            self._mostrar_error("No se puede factorizar", str(error))
            return
        verificacion = verificar_factorizacion(matriz_a, factorizacion["matriz_L"], factorizacion["matriz_U"])
        self._mostrar_resultado(factorizacion, verificacion, None)

    def resolver(self):
        """Resuelve Ax = b con LU (A cuadrada) y muestra y, x y las dos verificaciones."""
        datos = self._leer()
        if datos is None:
            return
        matriz_a, vector_b = datos
        try:
            resolucion = resolver_con_lu(matriz_a, vector_b)
        except ValueError as error:
            self._mostrar_error("No se puede resolver", str(error))
            return
        self._mostrar_resultado(resolucion, resolucion["verificacion"], resolucion)

    def _limpiar_resultado(self):
        """Vacía el panel de resultados."""
        for widget in self.marco_resultado.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self):
        """Muestra el logotipo ASCII y las instrucciones iniciales."""
        self._limpiar_resultado()
        ttk.Label(self.marco_resultado, text=LOGOTIPO_ASCII, style="Operation.TLabel", justify="left").pack(
            anchor="w", pady=(10, 12))
        ttk.Label(
            self.marco_resultado,
            text="Complete A y b.\n\n• «Factorizar A = LU» obtiene L y U y comprueba L · U == A.\n"
                 "• «Resolver Ax = b» resuelve Ly = b y Ux = y y comprueba A · x == b.\n"
                 "• «0. Ver Teoremas Clave del Módulo» resume la teoría detrás del método.",
            style="CardSubtitle.TLabel", wraplength=520, justify="left").pack(anchor="w")

    def _mostrar_error(self, titulo, mensaje):
        """Muestra en el panel un aviso de error con estilo de estado negativo."""
        self._limpiar_resultado()
        ttk.Label(self.marco_resultado, text=titulo, style="SectionTitle.TLabel").pack(anchor="w", pady=(8, 5))
        ttk.Label(self.marco_resultado, text=mensaje, style="StatusBad.TLabel", padding=10, wraplength=480).pack(
            anchor="w", pady=(4, 12))

    def mostrar_teoremas(self):
        """Opción 0: muestra los teoremas clave del módulo en el panel de resultados."""
        self._limpiar_resultado()
        interior = self.app._crear_area_desplazable(self.marco_resultado)
        seccion = self.app._agregar_seccion_analisis(interior, "Teoremas clave: factorización LU")
        for numero, texto in enumerate(TEOREMAS_CLAVE, start=1):
            ttk.Label(seccion, text=f"{numero}. {texto}", style="AnalysisBody.TLabel", wraplength=560,
                      justify="left").pack(anchor="w", pady=3)

    def _mostrar_matrices_lado_a_lado(self, padre, matriz_L, matriz_U):
        """
        Dibuja L y U en bloques verticales para que ambas matrices
        aprovechen el ancho completo del panel de resultados.

        Si una matriz tiene muchas columnas, incorpora desplazamiento
        horizontal local en lugar de dejar que las últimas columnas
        queden recortadas.
        """
        matrices = (
            (f"Matriz L ({len(matriz_L)}×{len(matriz_L[0])})", matriz_L),
            (f"Matriz U ({len(matriz_U)}×{len(matriz_U[0])})", matriz_U),
        )

        for titulo, matriz in matrices:
            bloque = ttk.Frame(padre, style="Card.TFrame")
            bloque.pack(fill="x", pady=(10, 8))

            ttk.Label(
                bloque,
                text=titulo,
                style="SectionTitle.TLabel",
            ).pack(anchor="w", pady=(0, 5))

            cantidad_columnas = max(
                (len(fila) for fila in matriz),
                default=0,
            )

            # En matrices pequeñas se usa todo el ancho disponible.
            # Las matrices anchas reciben una barra horizontal propia.
            if cantidad_columnas <= 5:
                tabla = crear_matriz_visual(
                    bloque,
                    matriz,
                    cell_width=58,
                    pad=3,
                )
                tabla.pack(anchor="center", pady=(0, 4))
            else:
                area = ttk.Frame(bloque, style="Card.TFrame")
                area.pack(fill="x", expand=True)

                canvas = tk.Canvas(
                    area,
                    height=max(110, min(420, len(matriz) * 58 + 24)),
                    bg=self.app.WHITE,
                    highlightthickness=0,
                    bd=0,
                )
                barra = ttk.Scrollbar(
                    area,
                    orient="horizontal",
                    command=canvas.xview,
                )
                canvas.configure(xscrollcommand=barra.set)

                interior = ttk.Frame(canvas, style="Card.TFrame")
                ventana = canvas.create_window(
                    (0, 0),
                    window=interior,
                    anchor="nw",
                )

                tabla = crear_matriz_visual(
                    interior,
                    matriz,
                    cell_width=56,
                    pad=3,
                )
                tabla.pack(anchor="w", pady=(2, 4))

                def actualizar_region(_event=None, c=canvas):
                    c.configure(scrollregion=c.bbox("all"))

                interior.bind("<Configure>", actualizar_region)
                canvas.bind(
                    "<Configure>",
                    lambda event, c=canvas, w=ventana:
                        c.itemconfigure(w, height=event.height),
                )

                canvas.pack(fill="x", expand=True)
                barra.pack(fill="x", pady=(2, 0))

    def _mostrar_pasos_reduccion(self, interior, titulo, pasos, numero_variables):
        """Muestra una sección con cada paso de una reducción sobre una matriz aumentada."""
        seccion = self.app._agregar_seccion_analisis(interior, titulo)
        for paso in pasos:
            ttk.Label(seccion, text=f"{paso['titulo']}: {paso['operacion']}", style="Operation.TLabel",
                      wraplength=560).pack(anchor="w", pady=(8, 3))
            crear_matriz_visual(seccion, paso["matriz"], numero_variables).pack(anchor="w")

    def _mostrar_resultado(self, factorizacion, verificacion, resolucion):
        """Dibuja L, U, multiplicadores, pasos y, si hay `resolucion`, y, x y la comprobación A·x == b."""
        self._limpiar_resultado()
        interior = self.app._crear_area_desplazable(self.marco_resultado)
        matriz_L, matriz_U = factorizacion["matriz_L"], factorizacion["matriz_U"]

        seccion = self.app._agregar_seccion_analisis(interior, "Factorización A = L · U")
        self._mostrar_matrices_lado_a_lado(seccion, matriz_L, matriz_U)
        ttk.Label(seccion, text=verificacion["mensaje"],
                  style="Status.TLabel" if verificacion["es_correcta"] else "StatusBad.TLabel",
                  padding=10, wraplength=520).pack(anchor="w", pady=(12, 0))

        multiplicadores = factorizacion["multiplicadores"]
        seccion = self.app._agregar_seccion_analisis(
            interior, "Multiplicadores registrados en L",
            None if multiplicadores else "No hubo eliminaciones: L es la identidad.")
        for multiplicador in multiplicadores:
            ttk.Label(
                seccion, style="AnalysisBody.TLabel",
                text=f"l{_subindice(multiplicador['fila'] + 1)}{_subindice(multiplicador['columna'] + 1)}"
                     f" = {formatear_fraccion(multiplicador['valor'])}").pack(anchor="w", pady=1)

        pasos = factorizacion.get("pasos") or factorizacion["pasos_factorizacion"]
        seccion = self.app._agregar_seccion_analisis(interior, "Pasos de la eliminación")
        for paso in pasos:
            ttk.Label(seccion, text=f"{paso['titulo']}: {paso['operacion']}", style="Operation.TLabel",
                      wraplength=560).pack(anchor="w", pady=(8, 3))
            self._mostrar_matrices_lado_a_lado(seccion, paso["matriz_L"], paso["matriz_U"])

        if resolucion is None:
            return
        orden = len(matriz_L)
        self._mostrar_pasos_reduccion(interior, "Sustitución hacia adelante: Ly = b, reduciendo [L | b]",
                                      resolucion["pasos_adelante"], orden)
        seccion = self.app._agregar_seccion_analisis(interior, "Vector intermedio y")
        crear_vector_visual(seccion, resolucion["vector_y"], "y").pack(anchor="w")
        self._mostrar_pasos_reduccion(interior, "Sustitución hacia atrás: Ux = y, reduciendo [U | y]",
                                      resolucion["pasos_atras"], orden)
        seccion = self.app._agregar_seccion_analisis(interior, "Solución x")
        crear_vector_visual(seccion, resolucion["vector_x"], "x").pack(anchor="w")
        seccion = self.app._agregar_seccion_analisis(interior, "Comprobación A · x = b")
        crear_vector_visual(seccion, resolucion["producto_ax"], "A · x").pack(anchor="w")
        ttk.Label(seccion, text=resolucion["mensaje_comprobacion"],
                  style="Status.TLabel" if resolucion["comprobacion_exitosa"] else "StatusBad.TLabel",
                  padding=10, wraplength=520).pack(anchor="w", pady=(12, 0))

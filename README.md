# Calculadora de Álgebra Lineal

Proyecto integrador de Álgebra Lineal (MTM0120) — Grupo 4, Universidad Americana.

Aplicación de escritorio hecha con **Python estándar y Tkinter/ttk**. Todo el cálculo usa listas, bucles y `fractions.Fraction` (aritmética exacta); no se usa NumPy, SciPy ni funciones de álgebra lineal de `math`.

## Integrantes

- Rafael Antonio Arauz Navarro
- Patricia del Carmen Oquist Talavera
- Cristopher Rafael Santana Ríos
- Blanca Alejandra Zeledón Abea

## Funcionalidades

### Sistemas de ecuaciones
- Evaluación y resolución de sistemas Ax = b con eliminación de Gauss y Gauss-Jordan, paso a paso con matrices visuales.
- Clasificación del sistema (solución única, infinitas, inconsistente) y de si es homogéneo o heterogéneo.
- Botón **Ver Ax = b**: separa [A|b] en A, x y b como bloques visuales.

### Vectores en Rⁿ
- Suma, resta y multiplicación por escalar.
- Combinación lineal mediante el sistema equivalente V·c = b.
- Dependencia / independencia lineal (**L.I. / L.D.**): matriz escalonada reducida, pivotes, variables básicas y libres, y una relación no trivial cuando existe (`v₁ − 2v₂ + v₃ = 0`).

### Matrices
Cada operación es un **botón** agrupado por categoría: un clic calcula y muestra el procedimiento paso a paso (sin listas desplegables ni botón «Calcular»).
- **Básicas:** A + B, A − B, c·A (con su propio campo de escalar) y A·B, con validación de dimensiones.
- **Traspuesta:** Aᵀ, Bᵀ y (A·B)ᵀ (con comprobación de (A·B)ᵀ = BᵀAᵀ).
- **Inversa:** por **adjunta** (cofactores, adj(A) = Cᵀ) y por **Gauss-Jordan** ([A | I] → [I | A⁻¹]), ambas con comprobación A·A⁻¹ = I y aviso si la matriz es singular o no cuadrada.
- **Determinante:** por **cofactores** (Laplace por la fila con más ceros), por **reducción de filas** y por la **regla de Sarrus** (solo 3×3, con las diagonales a la vista); cada uno se comprueba contra otro método.
- **Sistema Ax = b:** **regla de Cramer** (xᵢ = det(Aᵢ)/det(A)); A es n×n y b es la primera columna de B. Muestra cada Aᵢ, su determinante y comprueba A·x = b.
- **Constructor visual de expresiones**: «Fijar A y B» las deja de solo lectura; luego se arman expresiones como (A·Bᵀ) − (A⁻¹·B) solo con clics (A, B, R1–R7, + − · ᵀ ⁻¹ y paréntesis). Los botones inválidos se deshabilitan. «Guardar resultado» envía el último resultado a la memoria (R1–R7, máximo 7; al llenarse se reemplaza el más antiguo con confirmación).
- **Verificador de propiedades** (`teoremas/verificador_propiedades.py`): comprueba por ambos lados 26 igualdades y omite con motivo las que no aplican (dimensiones, matriz no cuadrada, det = 0).
- **Traspuesta del producto**: comprueba (A·B)ᵀ = BᵀAᵀ y muestra AᵀBᵀ como contraejemplo.

Mejoras de uso en este módulo:
- Los botones se **deshabilitan** cuando las dimensiones no sirven (p. ej. Sarrus si A no es 3×3) y la línea de ayuda explica el motivo al pasar el cursor.
- Al cambiar las dimensiones, las casillas se regeneran **conservando lo ya escrito**.
- La operación activa queda resaltada y solo se leen las matrices que esa operación usa.

### Matriz por vector y propiedades
- Producto A·v, verificación de A(u+v) = Au + Av y A·v como combinación lineal de las columnas de A.
- Módulo de propiedades algebraicas con selector que conserva las matrices y vectores cargados:
  1. A + B = B + A
  2. (A + B) + C = A + (B + C)
  3. A + 0 = A
  4. r(A + B) = rA + rB
  5. (r + s)A = rA + sA
  6. r(sA) = (rs)A
  7. A(u + v) = Au + Av
  8. A(cu) = c(Au)
  9. A·B = B·A — contraejemplo: el producto de matrices no es conmutativo.

### Factorización LU y solución de Ax = b (Programa 6)
- **Factorización A = L·U** (`modulos/modulo_lu.py`) solo con reemplazos de fila: L (m×m, unos en la diagonal) guarda cada multiplicador y U es la forma escalonada (m×n). Si hace falta intercambiar filas se detiene con «La matriz no admite Factorización LU sin permutación (requiere pivoteo parcial PA = LU)».
- Verifica **L·U == A** con el producto de matrices de la Calculadora y, para A cuadrada, resuelve **Ly = b** (adelante) y **Ux = y** (atrás) reduciendo [L|b] y [U|y]; termina con **A·x == b**.
- Vista **«LU Factorización LU»** con L, U, y, x, los pasos, el logotipo ASCII y la opción «0. Ver Teoremas Clave del Módulo».
- **Verificador de propiedades** (`teoremas/verificador_propiedades.py`): calcula ambos miembros de 26 igualdades (suma y escalares, producto, transposición, inversa, determinantes y efecto de las operaciones de fila) y diagnostica «Se cumple» / «No se cumple»; cada intermedio se calcula una sola vez.
- Los módulos de cálculo son funciones puras: reciben listas anidadas y devuelven resultados, sin `input()` ni `print()`.

### Interfaz
- **Análisis de Resultados**: tipo de ejercicio, procedimiento, pivotes, variables libres, dimensiones, clasificación y explicación.
- Seis paletas de colores y combinación personalizada; el tema se guarda en `tema_interfaz.json`.
- Navegación por teclado entre casillas (flechas y Enter); la sección activa se resalta en la barra lateral.

## Requisitos

- Python 3 con Tkinter (incluido en la instalación estándar de Python).
- Sin dependencias externas.

## Ejecución

```bash
python main.py
```

También se puede abrir la carpeta en PyCharm, abrir `main.py` y pulsar ▶ Run.

### Pruebas

```bash
python -m pruebas.casos_prueba
```

Cubren la factorización LU y Ax = b con L y U, el verificador de 26 propiedades, el encadenamiento sin recálculo, Ax = b, operaciones vectoriales, combinación lineal, dependencia lineal, clasificación homogéneo/heterogéneo, operaciones matriciales, traspuesta, inversas (adjunta y Gauss-Jordan), determinantes (cofactores, reducción y Sarrus), regla de Cramer, dimensiones incompatibles y fracciones exactas.

## Estructura

```text
Algebra_calculadora.py/
├── main.py                       # punto de entrada
├── tema_interfaz.json            # tema de colores guardado
├── algoritmos/
│   ├── dependencia_lineal.py     # análisis L.I. / L.D.
│   ├── eliminacion_gaussiana.py  # reexporta modulos/modulo_gauss.py (compatibilidad)
│   ├── expresiones.py            # constructor y evaluador de expresiones
│   ├── matrices.py               # reexporta modulos/modulo_matrices.py (compatibilidad)
│   └── vectores.py               # operaciones y combinación lineal
├── interfaces/
│   ├── componentes/tarjeta.py
│   ├── ventana_matriz.py
│   ├── ventana_principal.py
│   ├── vista_lu.py               # vista de la factorización LU
│   └── ventana_proceso.py
├── modulos/
│   ├── modulo_gauss.py           # Gauss, Gauss-Jordan y clasificación de sistemas
│   ├── modulo_lu.py              # Programa 6: factorización LU y solución por doble sustitución
│   └── modulo_matrices.py        # Módulo III: operaciones, determinantes, inversas y Cramer
├── teoremas/
│   └── verificador_propiedades.py  # 26 propiedades con diagnóstico «Se cumple»/«No se cumple»
├── modelos/
│   ├── memoria_matrices.py       # A/B de solo lectura, pila R1–R7, constructor
│   └── sistema_ecuaciones.py
├── utilidades/
│   ├── formato.py
│   └── fracciones.py
└── pruebas/
    └── casos_prueba.py
```

## Historial de entregas

- **Programa 1** – Interfaz base (Tkinter/ttk, tarjetas, navegación) y eliminación de Gauss.
- **Programa 4** – Vectores, dependencia lineal, A·v, propiedades algebraicas y operaciones matriciales.
- **Programa 5** – Documentación del código (encabezados de módulo y *docstrings*) sin cambiar la lógica.
- **Programa 6** – Factorización LU y Ax = b por doble sustitución, verificador ampliado a 26 propiedades y encadenamiento de resultados.
- **Posteriores** – Traspuestas, inversa (adjunta y Gauss-Jordan), determinantes (cofactores, reducción y Sarrus), regla de Cramer, constructor visual de expresiones con memoria R1–R7, la propiedad 9 y el módulo de matrices rediseñado con botones.

Más detalle de cada entrega en [`README_local.md`](README_local.md).


### Verificación manual de L · U = A

En la vista de Factorización LU se agregó el botón «Ingresar L y U manualmente y
comprobar L · U = A». La matriz A se toma de la cuadrícula principal; el formulario
permite introducir L (m×m) y U (m×n), calcula el producto matricial con fracciones
exactas y muestra si coincide con A. Si no coincide, señala las posiciones y valores
diferentes.

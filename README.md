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
- **Modo calculadora**: «Usar resultado como A/B» reutiliza el último resultado; la expresión acumulada se muestra en el título («Matriz A = (A·B)ᵀ») y «Reiniciar expresión» la restablece.

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

Cubren Ax = b, operaciones vectoriales, combinación lineal, dependencia lineal, clasificación homogéneo/heterogéneo, operaciones matriciales, traspuesta, inversas (adjunta y Gauss-Jordan), determinantes (cofactores, reducción y Sarrus), regla de Cramer, dimensiones incompatibles y fracciones exactas.

## Estructura

```text
Algebra_calculadora.py/
├── main.py                       # punto de entrada
├── tema_interfaz.json            # tema de colores guardado
├── algoritmos/
│   ├── dependencia_lineal.py     # análisis L.I. / L.D.
│   ├── eliminacion_gaussiana.py  # Gauss, Gauss-Jordan, inversa [A|I]
│   ├── matrices.py               # operaciones, determinantes (cofactores, Sarrus), adjunta, Cramer
│   └── vectores.py               # operaciones y combinación lineal
├── interfaces/
│   ├── componentes/tarjeta.py
│   ├── ventana_matriz.py
│   ├── ventana_principal.py
│   └── ventana_proceso.py
├── modelos/
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
- **Posteriores** – Traspuestas, inversa (adjunta y Gauss-Jordan), determinantes (cofactores, reducción y Sarrus), regla de Cramer, modo calculadora, la propiedad 9 y el módulo de matrices rediseñado con botones.

Más detalle de cada entrega en [`README_local.md`](README_local.md).

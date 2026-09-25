# Programa 3 - Calculadora de Álgebra Lineal
## Grupo 4 - Universidad Americana

Proyecto integrador de Álgebra Lineal (MTM0120), construido sobre la interfaz del Programa 1. Se conservaron Tkinter/ttk, la distribución por tarjetas, colores, tipografías y navegación visual, agregando las funciones solicitadas en el Programa 3.

### Integrantes
- Rafael Antonio Arauz Navarro
- Patricia del Carmen Oquist Talavera
- Cristopher Rafael Santana Ríos
- Blanca Alejandra Zeledón Abea

## Funcionalidades del Programa 3

- Operaciones con vectores en R^n:
  - suma;
  - resta;
  - multiplicación por escalar.
- Evaluación de combinación lineal mediante el sistema equivalente Vc=b.
- Análisis de dependencia e independencia lineal de los vectores, incluyendo una relación no trivial cuando existe.
- Producto matriz–vector A·v con validación de dimensiones.
- Módulo de las 8 propiedades algebraicas solicitadas:
  1. A + B = B + A
  2. (A + B) + C = A + (B + C)
  3. A + 0 = A
  4. r(A + B) = rA + rB
  5. (r + s)A = rA + sA
  6. r(sA) = (rs)A
  7. A(u + v) = Au + Av
  8. A(cu) = c(Au)
- El selector de propiedades permite cambiar de una propiedad a otra conservando las mismas matrices y vectores cargados.
- El resultado muestra ambos lados de la igualdad y las dependencias de dimensiones/componentes requeridas.
- Operaciones matriciales:
  - suma y resta con validación de dimensiones;
  - multiplicación por escalar;
  - multiplicación A·B con validación columnas(A)=filas(B).
- Evaluación y resolución de sistemas Ax=b.
- Eliminación de Gauss y visualización paso a paso.
- Aritmética exacta con `Fraction`.

### Restricciones
El programa utiliza únicamente Python estándar y Tkinter/ttk. No utiliza NumPy, SciPy ni funciones avanzadas de `math`.

### Estructura

```text
Programa1_Grupo4/
├── main.py
├── algoritmos/
│   ├── eliminacion_gaussiana.py
│   ├── matrices.py
│   └── vectores.py
├── interfaces/
│   ├── componentes/tarjeta.py
│   ├── ventana_principal.py
│   └── ventana_proceso.py
├── modelos/
├── utilidades/
└── pruebas/
    └── casos_prueba.py
```

## Ejecución en PyCharm

1. Abrir la carpeta `Programa1_Grupo4` como proyecto.
2. Abrir `main.py`.
3. Ejecutar con el botón ▶ Run.
4. Desde la barra lateral se puede entrar a Entrada de Matriz, Proceso Gaussiano, Operaciones de Vectores y Operaciones Matriciales.

También se pueden ejecutar las pruebas desde la terminal de PyCharm:

```bash
python -m pruebas.casos_prueba
```

Las pruebas cubren Ax=b, operaciones vectoriales, combinación lineal, operaciones matriciales, dimensiones incompatibles y fracciones exactas.


### Funciones añadidas para el I Corte

- Módulo **A·v Matriz por Vector**:
  - calcula directamente A·v;
  - verifica paso a paso la propiedad distributiva A(u+v)=Au+Av;
  - expresa A·v como combinación lineal de las columnas de A usando los componentes de v como escalares.
- Botón **Ver Ax = b** en la entrada de sistemas:
  - separa automáticamente la matriz aumentada [A|b];
  - muestra la matriz de coeficientes A, el vector incógnita x y el vector de términos independientes b.
- Estas funciones permiten trabajar directamente los tres apartados del examen del I Corte sin usar bibliotecas externas.

## Mejoras de interfaz

- El texto de las ventanas de proceso ya no utiliza una franja blanca debajo del título.
- Las casillas numéricas limpian el `0` de ayuda al recibir el foco y lo restauran si quedan vacías.
- Las flechas izquierda/derecha/arriba/abajo y Enter permiten desplazarse entre casillas.
- Se incorporaron seis paletas de colores y una opción de combinación personalizada mediante selector de color.
- La selección de tema se guarda en `tema_interfaz.json` y se conserva al volver a abrir el programa.
- La sección activa de la barra lateral queda resaltada visualmente.
- Los vectores generadores se muestran con subíndices matemáticos (v₁, v₂, v₃, …).
- La eliminación de Gauss/Gauss-Jordan normaliza internamente los datos a `Fraction` para conservar exactitud también cuando el usuario introduce enteros.

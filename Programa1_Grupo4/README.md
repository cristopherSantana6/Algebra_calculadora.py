# Programa 1 - Linear Algebra Studio
## Grupo 4 - Universidad Americana

Proyecto de avance para Álgebra Lineal (MTM0120).

### Integrantes
- Rafael Antonio Arauz Navarro
- Patricia del Carmen Oquist Talavera
- Cristopher Rafael Santana Ríos
- Blanca Alejandra Zeledón Abea

## Estructura

```text
Programa1_Grupo4/
├── main.py
├── algoritmos/
│   ├── __init__.py
│   └── eliminacion_gaussiana.py
├── interfaces/
│   ├── __init__.py
│   ├── componentes/
│   │   ├── __init__.py
│   │   └── tarjeta.py
│   ├── ventana_principal.py
│   └── ventana_proceso.py
├── modelos/
│   ├── __init__.py
│   └── sistema_ecuaciones.py
├── pruebas/
│   ├── __init__.py
│   └── casos_prueba.py
├── recursos/
│   ├── iconos/
│   └── imagenes/
├── utilidades/
│   ├── __init__.py
│   ├── formato.py
│   └── fracciones.py
├── README.md
└── .gitignore
```

## Requisitos
- Python 3.x
- Tkinter
- No requiere librerías externas.

## Fracciones exactas

El programa acepta en las casillas:

```text
2
-3
1/2
-5/8
0.25
```

Internamente usa `Fraction` de la biblioteca estándar de Python, por lo que los resultados racionales no se redondean a decimal durante el cálculo.

Las matrices, soluciones y operaciones del proceso se muestran como enteros o fracciones, por ejemplo `1/2`, `-3/4` o `5`.

## Ejecución

Desde la carpeta raíz:

```bash
python main.py
```

## Pruebas

```bash
python -m pruebas.casos_prueba
```

Las pruebas cubren:
- solución única;
- infinitas soluciones;
- sistema inconsistente;
- solución exacta con entradas fraccionarias;
- lectura de fracciones y decimales.

## Funcionalidad actual

- Interfaz gráfica organizada por vistas.
- Generación dinámica de matrices aumentadas.
- Lectura de enteros, decimales y fracciones.
- Eliminación por filas con pivoteo.
- Aritmética racional exacta.
- Registro de pasos de eliminación.
- Visualización paso a paso con botones Anterior/Siguiente.
- Clasificación de los tres tipos de sistema.
- Sustitución regresiva para solución única.
- Verificación exacta de la solución.

## Próximas mejoras

- Parametrización completa de infinitas soluciones.
- Historial de ejercicios.
- Exportación de resultados.
- Más operaciones didácticas y ayudas visuales.

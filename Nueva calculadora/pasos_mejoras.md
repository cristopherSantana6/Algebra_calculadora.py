# Pasos de mejoras UI/UX

Auditoría del frontend Tkinter (`interfaces/ventana_principal.py`, `tema_interfaz.json`). Notas iniciales: **Interfaz 6,5/10 · UX 7/10**.

Se avanza de lo más fácil a lo más difícil, un paso a la vez: tras cada paso se muestra el cambio y se espera aprobación antes de seguir. Todo en Python/Tkinter, sin dependencias nuevas.

## Pasos

- [ ] **1. Renombrar constantes de color** (`TEAL`→`PRIMARIO`, `TEAL_DARK`→`PRIMARIO_OSCURO`, `CORAL`→`ACENTO`, `CORAL_DARK`→`ACENTO_OSCURO`) en `ventana_principal.py` (~147-157, `aplicar_paleta`, `configurar_estilos` y usos). Solo renombrado, sin cambio visual.
- [ ] **2. Pie de página y textos fijos** (`ventana_principal.py:701, 778`): quitar «Programa 5» fijo; el pie muestra el nombre de la vista actual.
- [ ] **3. Separar encabezado y fondo** en `tema_interfaz.json`: `background` `#F1EEF7`, `header` blanco; `Top.TFrame` con línea inferior de 1 px.
- [ ] **4. Tamaño mínimo de fuente 10 pt** y constantes de escala tipográfica (10/11/13/18/24) en `configurar_estilos`.
- [ ] **5. Unificar tipografía**: solo Segoe UI (interfaz) y Cambria Math (matemática); quitar Georgia y Consolas (`Header.TLabel`, `PageTitle`, `Operation.TLabel`, `tk.Text` de proceso).
- [ ] **6. Enter salta a la fila siguiente** en `preparar_navegacion`/`configurar_entrada` (`ventana_principal.py:607-664`).
- [ ] **7. Orden de Tab y foco visible**: orden lógico por casillas y botones; foco visible propio (borde `PRIMARIO`) en `TEntry`, `TSpinbox` y botones vía `estilo.map`.
- [ ] **8. Sidebar reversible**: reemplazar «Ampliar menú» de un solo uso (`ampliar_sidebar`, 705-715) por un toggle ☰ que expande y contrae.
- [ ] **9. Escala de espaciado**: constantes `ESPACIO = {xs: 4, s: 8, m: 16, l: 24, xl: 32}` y reemplazar los paddings sueltos (18, 24, 10, 25, 14...) por ellas.
- [ ] **10. Errores en línea en vez de `messagebox`**: casilla inválida con borde `danger` y mensaje bajo la tarjeta; `messagebox` solo en confirmaciones (memoria llena, nueva sesión). Empezar por entrada de sistemas y extender módulo por módulo.
- [ ] **11. Navegación coherente de procesos**: mostrar «Proceso Gaussiano»/«Gauss-Jordan» como vistas del área principal (o marcar con ↗ las que abren ventana) y registrar «proceso» en `botones_sidebar`.
- [ ] **12. Prueba en vivo y accesibilidad de estados**: ejecutar la app; revisar `bind_all("<MouseWheel>")` (443, 976), densidad de la vista de matrices en 1100×680 y añadir icono o texto (✓ / ✕) a los estados verde/rojo (`Status.TLabel`, `StatusBad.TLabel`).
- [ ] **13. Pivote y fila afectada resaltados** en los pasos de Gauss (`crear_matriz_visual` en `ventana_matriz.py` con celdas resaltadas + etiqueta `F₂ → F₂ − 3F₁`).
- [ ] **14. (Opcional) Matrices con corchetes `[ ]`** dibujados con `Canvas` en `crear_matriz_visual`, en lugar del recuadro por celda.
- [ ] **15. (Opcional) Reducir los 6 temas a 2** (claro y oscuro) con un solo color de énfasis; decisión de diseño a confirmar antes de tocar `TEMAS` y el selector de «Tema y colores».

## Verificación (cada paso)

- `python -m pruebas.casos_prueba` sigue pasando.
- `python main.py`: revisar la pantalla afectada en los temas y en el tamaño mínimo 1100×680.
- Mostrar qué cambió y esperar aprobación antes del siguiente paso.

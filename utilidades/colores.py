"""
Utilidades de color para garantizar un contraste legible (WCAG AA, 4.5:1) en cualquier tema.
Solo usa la biblioteca estándar: oscurece un color poco a poco hasta que se lea sobre sus fondos.
"""


def _a_rgb(color):
    """Convierte '#RRGGBB' en una tupla (r, g, b) de enteros 0-255."""
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def _a_hex(rgb):
    """Convierte una tupla (r, g, b) en '#RRGGBB'."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def luminancia(color):
    """Luminancia relativa de un color '#RRGGBB' según WCAG."""
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in _a_rgb(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(color_a, color_b):
    """Razón de contraste (1 a 21) entre dos colores '#RRGGBB'."""
    claro, oscuro = sorted((luminancia(color_a), luminancia(color_b)), reverse=True)
    return (claro + 0.05) / (oscuro + 0.05)


def asegurar_contraste(color, fondos, minimo=4.5):
    """Oscurece `color` en pasos del 2 % hacia negro hasta que supere `minimo` sobre todos los `fondos`.

    Si ya cumple, lo devuelve sin cambios, así cada tema conserva su identidad cuando es legible.
    """
    if isinstance(fondos, str):
        fondos = (fondos,)
    rgb = _a_rgb(color)
    for _ in range(50):
        actual = _a_hex(rgb)
        if all(contraste(actual, fondo) >= minimo for fondo in fondos):
            return actual
        rgb = tuple(int(c * 0.98) for c in rgb)
    return _a_hex(rgb)

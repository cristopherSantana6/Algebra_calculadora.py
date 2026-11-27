"""Pruebas unitarias de los métodos de Jacobi y Gauss-Seidel."""

import unittest

from algoritmos.metodos_iterativos import (
    preparar_sistema,
    resolver_gauss_seidel,
    resolver_jacobi,
    resolver_iterativos,
)


MATRIZ = [
    [10, -1, 2],
    [-1, 11, -1],
    [2, -1, 10],
]
VECTOR = [6, 22, -10]
SOLUCION = [1, 2, -1]


class PruebasMetodosIterativos(unittest.TestCase):

    def comprobar_solucion(self, resultado):
        self.assertTrue(resultado["convergio"])
        for obtenido, esperado in zip(resultado["solucion"], SOLUCION):
            self.assertAlmostEqual(obtenido, esperado, places=6)
        self.assertLessEqual(resultado["residuo"], 1e-5)

    def test_jacobi_converge(self):
        resultado = resolver_jacobi(
            MATRIZ, VECTOR, [0, 0, 0], 1e-8, 100
        )
        self.comprobar_solucion(resultado)

    def test_gauss_seidel_converge(self):
        resultado = resolver_gauss_seidel(
            MATRIZ, VECTOR, [0, 0, 0], 1e-8, 100
        )
        self.comprobar_solucion(resultado)

    def test_selector_de_metodo(self):
        resultado = resolver_iterativos(
            MATRIZ, VECTOR, [0, 0, 0],
            tolerancia=1e-8, max_iteraciones=100,
            metodo="Gauss-Seidel"
        )
        self.assertEqual(resultado["metodo"], "Gauss-Seidel")
        self.comprobar_solucion(resultado)

    def test_rechaza_matriz_no_cuadrada(self):
        with self.assertRaises(ValueError):
            preparar_sistema([[1, 2, 3], [4, 5, 6]], [1, 2])

    def test_rechaza_diagonal_nula(self):
        with self.assertRaises(ValueError):
            resolver_jacobi([[0, 1], [1, 2]], [1, 2])

    def test_rechaza_tolerancia_no_positiva(self):
        with self.assertRaises(ValueError):
            resolver_jacobi(MATRIZ, VECTOR, tolerancia=0)

    def test_reporta_limite_de_iteraciones(self):
        resultado = resolver_jacobi(
            MATRIZ, VECTOR, [0, 0, 0],
            tolerancia=1e-15, max_iteraciones=1
        )
        self.assertFalse(resultado["convergio"])
        self.assertEqual(resultado["iteraciones"], 1)

    def test_despeje_jacobi_usa_iteracion_anterior(self):
        despejes = resolver_jacobi(MATRIZ, VECTOR, [0, 0, 0])["despejes"]
        self.assertEqual(len(despejes), 3)
        self.assertEqual(despejes[0]["formula"], "x₁⁽ᵏ⁺¹⁾ = (6 + x₂⁽ᵏ⁾ − 2x₃⁽ᵏ⁾) / 10")
        self.assertEqual(despejes[0]["simplificada"], "x₁⁽ᵏ⁺¹⁾ = 0.6 + 0.1x₂⁽ᵏ⁾ − 0.2x₃⁽ᵏ⁾")
        self.assertNotIn("x₁⁽ᵏ⁺¹⁾ +", despejes[1]["formula"])

    def test_despeje_gauss_seidel_usa_valores_nuevos(self):
        despejes = resolver_gauss_seidel(MATRIZ, VECTOR, [0, 0, 0])["despejes"]
        self.assertEqual(despejes[2]["formula"], "x₃⁽ᵏ⁺¹⁾ = (−10 − 2x₁⁽ᵏ⁺¹⁾ + x₂⁽ᵏ⁺¹⁾) / 10")

    def test_primera_sustitucion_coincide_con_historial(self):
        for resolver in (resolver_jacobi, resolver_gauss_seidel):
            resultado = resolver(MATRIZ, VECTOR, [0, 0, 0])
            primera = resultado["historial"][1]["aproximacion"]
            for despeje, valor in zip(resultado["despejes"], primera):
                obtenido = despeje["primera_iteracion"].rsplit("= ", 1)[1].replace("−", "-")
                self.assertAlmostEqual(float(obtenido), valor, places=5)


if __name__ == "__main__":
    unittest.main()

import unittest
from algoritmos.newton_raphson import resolver_newton_raphson


class NewtonRaphsonTests(unittest.TestCase):
    def test_raiz_cuadrada_de_dos(self):
        resultado = resolver_newton_raphson("x**2 - 2", 1.5, 1e-8, 50)
        self.assertAlmostEqual(resultado["aproximacion"], 2 ** 0.5, places=7)
        self.assertLessEqual(resultado["residuo"], 1e-8)

    def test_convergencia_desde_raiz(self):
        resultado = resolver_newton_raphson("x**2 - 4", 2)
        self.assertEqual(resultado["iteraciones"], 0)
        self.assertEqual(resultado["aproximacion"], 2)

    def test_derivada_cero(self):
        resultado = resolver_newton_raphson("x**2 + 1", 0)
        self.assertIn("derivada es cero", resultado["estado"])


    def test_maximo_de_iteraciones_sin_convergencia(self):
        resultado = resolver_newton_raphson(
            "x**2 - 2", 1.5, 1e-30, 1
        )
        self.assertIn("máximo de iteraciones", resultado["estado"])
        self.assertEqual(resultado["iteraciones"], 1)
        self.assertEqual(resultado["max_iteraciones"], 1)
        self.assertIsNotNone(resultado["error"])
        self.assertGreater(resultado["residuo"], 1e-30)

    def test_registra_derivada_y_residuo_en_historial(self):
        resultado = resolver_newton_raphson("x**2 - 2", 1.5, 1e-8, 50)
        self.assertTrue(resultado["historial"])
        paso = resultado["historial"][0]
        self.assertIn("dfx", paso)
        self.assertIn("residuo", paso)
        self.assertIn("xnext", paso)


if __name__ == "__main__":
    unittest.main()

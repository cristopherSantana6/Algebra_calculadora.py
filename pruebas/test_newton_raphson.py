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


if __name__ == "__main__":
    unittest.main()

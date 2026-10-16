
"""
Pruebas funcionales de los algoritmos de Álgebra Lineal.
Verifica operaciones matriciales, vectoriales y resolución de sistemas.
Comprueba propiedades algebraicas y el manejo de dimensiones incompatibles.
Utiliza assert para detectar resultados incorrectos durante la ejecución.
"""

import ast
import sys
from fractions import Fraction
from pathlib import Path

from algoritmos.eliminacion_gaussiana import (
    eliminacion_gaussiana,
    es_homogeneo,
    gauss_jordan,
    inversa_gauss_jordan,
    obtener_clasificacion,
    resolver_solucion_unica,
    verificar_solucion,
)
from algoritmos.expresiones import (
    comprobar_traspuesta_del_producto,
    evaluar_tokens,
    siguientes_permitidos,
)
from algoritmos.matrices import (
    multiplicar_matrices,
    multiplicar_matriz_vector,
    multiplicar_matriz_escalar,
    restar_matrices,
    sumar_matrices,
    trasponer_matriz,
    determinante,
    determinante_cofactores,
    determinante_reduccion,
    determinante_sarrus,
    resolver_cramer,
    desarrollo_cofactores,
    inversa_por_adjunta,
    matriz_adjunta,
    matriz_cofactores,
)
from modulos.modulo_matrices import validar_matriz
from modulos.modulo_lu import (
    MENSAJE_SIN_PERMUTACION,
    factorizar_lu,
    resolver_con_lu,
    sustitucion_adelante,
    sustitucion_atras,
    verificar_factorizacion,
)
import teoremas.verificador_propiedades as verificador
from teoremas.verificador_propiedades import verificar_propiedades
from algoritmos.vectores import (
    analizar_dependencia_lineal,
    es_combinacion_lineal,
    multiplicar_escalar,
    restar_vectores,
    sumar_vectores,
)
from utilidades.colores import asegurar_contraste, contraste
from modelos.memoria_matrices import ConstructorExpresion, MatricesBase, PilaResultados
from utilidades.fracciones import formatear_fraccion, leer_fraccion


def ejecutar_casos():
    """Ejecuta las pruebas funcionales de los algoritmos de la calculadora.
       No recibe parámetros ni devuelve un resultado; utiliza assert y mensajes
       para indicar si las comprobaciones se completan correctamente.
       """

    # Sistema Ax=b: también valida la funcionalidad que ya tenía el Programa 1.
    matriz = [
        [Fraction(2), Fraction(-1), Fraction(1), Fraction(3)],
        [Fraction(1), Fraction(1), Fraction(1), Fraction(6)],
        [Fraction(1), Fraction(2), Fraction(-1), Fraction(2)],
    ]
    escalonada, pivotes, inconsistente, pasos = eliminacion_gaussiana(matriz, 3)
    clasificacion, _ = obtener_clasificacion(escalonada, 3, pivotes, inconsistente)
    assert clasificacion == "unica" and pasos
    solucion = resolver_solucion_unica(escalonada, 3, pivotes)
    assert verificar_solucion(matriz, solucion)
    print("✓ Ax=b: solución única y verificación correctas")

    reducida, pivotes_j, inconsistente_j, pasos_j = gauss_jordan(matriz, 3)
    assert not inconsistente_j and len(pivotes_j) == 3 and pasos_j
    solucion_j = [reducida[fila][3] for fila, _ in pivotes_j]
    assert verificar_solucion(matriz, solucion_j)
    assert any("÷" in paso["operacion"] for paso in pasos_j)
    print("✓ Gauss-Jordan: forma reducida, solución y formato de división correctos")

    # Vectores.
    a = [Fraction(1), Fraction(2), Fraction(3)]
    b = [Fraction(4), Fraction(5), Fraction(6)]
    assert sumar_vectores(a, b) == [Fraction(5), Fraction(7), Fraction(9)]
    assert restar_vectores(a, b) == [Fraction(-3), Fraction(-3), Fraction(-3)]
    assert multiplicar_escalar(a, Fraction(2)) == [Fraction(2), Fraction(4), Fraction(6)]
    print("✓ Vectores: suma, resta y escalar correctos")

    generadores = [
        [Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(1), Fraction(1)],
    ]
    combinado = [Fraction(2), Fraction(3), Fraction(5)]
    no_combinado = [Fraction(1), Fraction(1), Fraction(3)]
    assert es_combinacion_lineal(generadores, combinado)["es_combinacion"]
    assert not es_combinacion_lineal(generadores, no_combinado)["es_combinacion"]
    print("✓ Combinación lineal: casos sí/no correctos")

    independientes = analizar_dependencia_lineal([
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ])
    dependientes = analizar_dependencia_lineal([
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(4)],
    ])
    assert independientes["independiente"]
    assert not dependientes["independiente"]
    assert dependientes["relacion"] == [Fraction(-2), Fraction(1)]
    assert independientes["homogeneo"] and dependientes["homogeneo"]
    print("✓ Dependencia lineal: conjuntos independientes y dependientes correctos")

    # La salida debe ser la forma escalonada REDUCIDA, con pivotes y libres identificados.
    tres = analizar_dependencia_lineal([
        [Fraction(1), Fraction(2), Fraction(3)],
        [Fraction(4), Fraction(5), Fraction(6)],
        [Fraction(7), Fraction(8), Fraction(9)],
    ])
    assert not tres["independiente"] and tres["rango"] == 2
    assert tres["columnas_pivote"] == [0, 1] and tres["variables_libres"] == [2]
    assert tres["reducida"] == [
        [1, 0, -1, 0],
        [0, 1, 2, 0],
        [0, 0, 0, 0],
    ]
    assert tres["relacion"] == [Fraction(1), Fraction(-2), Fraction(1)]
    print("✓ Dependencia lineal: forma reducida, pivotes y variables libres correctos")

    # Homogéneo vs heterogéneo.
    assert es_homogeneo([[Fraction(1), Fraction(2), Fraction(0)]], 2)
    assert not es_homogeneo([[Fraction(1), Fraction(2), Fraction(5)]], 2)
    assert not es_combinacion_lineal(generadores, combinado)["homogeneo"]
    print("✓ Clasificación homogéneo / heterogéneo correcta")

    # Gauss no debe mostrar el paso innecesario «R ← R / (1)».
    _, _, _, pasos_uno = eliminacion_gaussiana(
        [[Fraction(1), Fraction(2), Fraction(3)], [Fraction(0), Fraction(1), Fraction(1)]], 2
    )
    assert not any("/ (1)" in paso["operacion"] for paso in pasos_uno)
    print("✓ Gauss: no divide filas cuyo pivote ya vale 1")

    # Matrices.
    A = [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]]
    B = [[Fraction(5), Fraction(6)], [Fraction(7), Fraction(8)]]
    assert sumar_matrices(A, B) == [[6, 8], [10, 12]]
    assert restar_matrices(A, B) == [[-4, -4], [-4, -4]]
    assert multiplicar_matriz_escalar(A, Fraction(2)) == [[2, 4], [6, 8]]
    assert multiplicar_matrices(A, B) == [[19, 22], [43, 50]]
    u = [Fraction(4), Fraction(-1)]
    v = [Fraction(-3), Fraction(5)]
    assert multiplicar_matriz_vector(A, [u[0] + v[0], u[1] + v[1]]) == [Fraction(9), Fraction(19)]
    assert [x + y for x, y in zip(multiplicar_matriz_vector(A, u), multiplicar_matriz_vector(A, v))] == [Fraction(9), Fraction(19)]
    print("✓ Producto matriz–vector y propiedad distributiva correctos")
    try:
        multiplicar_matrices([[1, 2, 3]], [[1, 2], [3, 4]])
        raise AssertionError("Debió rechazar dimensiones incompatibles.")
    except ValueError:
        pass
    print("✓ Matrices: suma, resta, escalar y multiplicación correctas")

    # Traspuesta: una matriz 2×3 pasa a ser 3×2 y (AB)ᵀ = BᵀAᵀ.
    A_t = [[Fraction(1), Fraction(2), Fraction(3)], [Fraction(4), Fraction(5), Fraction(6)]]
    B_t = [[Fraction(7), Fraction(8)], [Fraction(9), Fraction(10)], [Fraction(11), Fraction(12)]]
    assert trasponer_matriz(A_t) == [[1, 4], [2, 5], [3, 6]]
    assert trasponer_matriz(trasponer_matriz(A_t)) == A_t
    producto_t = multiplicar_matrices(A_t, B_t)
    assert producto_t == [[58, 64], [139, 154]]
    assert trasponer_matriz(producto_t) == [[58, 139], [64, 154]]
    assert trasponer_matriz(producto_t) == multiplicar_matrices(
        trasponer_matriz(B_t), trasponer_matriz(A_t)
    )
    print("✓ Traspuesta: Aᵀ, (Aᵀ)ᵀ = A y (AB)ᵀ = BᵀAᵀ correctas")

    # Inversa por el método de la adjunta: A⁻¹ = (1/det A)·adj(A).
    A_2 = [[Fraction(2), Fraction(1)], [Fraction(5), Fraction(3)]]
    inv_2 = inversa_por_adjunta(A_2)
    assert inv_2["determinante"] == 1
    assert inv_2["adjunta"] == [[3, -1], [-5, 2]]
    assert inv_2["inversa"] == [[3, -1], [-5, 2]]

    A_3 = [
        [Fraction(1), Fraction(2), Fraction(3)],
        [Fraction(0), Fraction(1), Fraction(4)],
        [Fraction(5), Fraction(6), Fraction(0)],
    ]
    assert determinante(A_3) == 1
    assert matriz_adjunta(A_3) == trasponer_matriz(matriz_cofactores(A_3))
    identidad_3 = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    assert multiplicar_matrices(A_3, inversa_por_adjunta(A_3)["inversa"]) == identidad_3

    A_frac = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(1, 4), Fraction(1)]]
    assert multiplicar_matrices(A_frac, inversa_por_adjunta(A_frac)["inversa"]) == [[1, 0], [0, 1]]
    assert inversa_por_adjunta([[Fraction(4)]])["inversa"] == [[Fraction(1, 4)]]

    for sin_inversa in ([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(4)]],   # singular
                        [[Fraction(1), Fraction(2), Fraction(3)]]):                # no cuadrada
        try:
            inversa_por_adjunta(sin_inversa)
            raise AssertionError("Debió rechazar una matriz sin inversa.")
        except ValueError:
            pass
    print("✓ Inversa por adjunta: det, cofactores, adj(A) = Cᵀ, A·A⁻¹ = I y casos sin inversa")

    # Inversa por Gauss-Jordan: [A | I] → [I | A⁻¹]; debe coincidir con la adjunta.
    assert inversa_gauss_jordan(A_2)["inversa"] == [[3, -1], [-5, 2]]
    gj_3 = inversa_gauss_jordan(A_3)
    assert gj_3["inversa"] == inversa_por_adjunta(A_3)["inversa"]
    assert multiplicar_matrices(A_3, gj_3["inversa"]) == identidad_3
    assert [fila[:3] for fila in gj_3["aumentada_final"]] == identidad_3
    assert any("÷" in paso["operacion"] for paso in gj_3["pasos"])
    assert inversa_gauss_jordan(A_frac)["inversa"] == inversa_por_adjunta(A_frac)["inversa"]
    assert inversa_gauss_jordan([[Fraction(4)]])["inversa"] == [[Fraction(1, 4)]]
    for sin_inversa in ([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(4)]],
                        [[Fraction(1), Fraction(2), Fraction(3)]]):
        try:
            inversa_gauss_jordan(sin_inversa)
            raise AssertionError("Debió rechazar una matriz sin inversa.")
        except ValueError:
            pass
    print("✓ Inversa por Gauss-Jordan: [I | A⁻¹], coincide con la adjunta y rechaza singulares")

    # Determinante por cofactores (Laplace): debe coincidir con el de eliminación.
    assert determinante_cofactores([[Fraction(7)]]) == 7
    assert determinante_cofactores(A_2) == 1
    assert determinante_cofactores(A_3) == 1
    A_4 = [
        [Fraction(1, 2), Fraction(0), Fraction(2), Fraction(-1)],
        [Fraction(3), Fraction(1), Fraction(0), Fraction(4)],
        [Fraction(0), Fraction(0), Fraction(5), Fraction(1, 3)],
        [Fraction(2), Fraction(-1), Fraction(1), Fraction(0)],
    ]
    assert determinante_cofactores(A_4) == determinante(A_4)
    assert determinante_cofactores([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(4)]]) == 0
    desarrollo = desarrollo_cofactores(A_3)
    assert desarrollo["fila"] == 1  # la fila 2 (0, 1, 4) tiene un cero
    assert desarrollo["terminos"][0]["det_menor"] is None  # a₂₁ = 0: no se calcula su menor
    assert sum(t["producto"] for t in desarrollo["terminos"]) == desarrollo["determinante"] == 1
    try:
        desarrollo_cofactores([[Fraction(1), Fraction(2), Fraction(3)]])
        raise AssertionError("Debió rechazar una matriz no cuadrada.")
    except ValueError:
        pass
    print("✓ Determinante por cofactores: 1×1 a 4×4, fila con más ceros y coincide con eliminación")

    # Determinante por reducción de filas: triangular, signo por intercambios y pasos.
    red_3 = determinante_reduccion(A_3)
    assert red_3["determinante"] == 1 == determinante_cofactores(A_3)
    assert all(red_3["triangular"][i][j] == 0 for i in range(3) for j in range(i))
    assert determinante_reduccion(A_4)["determinante"] == determinante_cofactores(A_4)
    con_intercambio = determinante_reduccion([[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]])
    assert con_intercambio["determinante"] == -1 and con_intercambio["signo"] == -1
    assert any(p["titulo"] == "Intercambio de filas" for p in con_intercambio["pasos"])
    singular = determinante_reduccion([[Fraction(1), Fraction(2)], [Fraction(2), Fraction(4)]])
    assert singular["determinante"] == 0 and singular["diagonal"] is None
    try:
        determinante_reduccion([[Fraction(1), Fraction(2), Fraction(3)]])
        raise AssertionError("Debió rechazar una matriz no cuadrada.")
    except ValueError:
        pass
    print("✓ Determinante por reducción de filas: triangular, signo por intercambios y coincide con cofactores")
    print("✓ Matrices: validación de dimensiones incompatibles correcta")

    # Fracciones exactas.
    assert leer_fraccion("1/2") == Fraction(1, 2)
    assert leer_fraccion("-5/8") == Fraction(-5, 8)
    assert leer_fraccion("0.25") == Fraction(1, 4)
    print("✓ Lectura de fracciones y decimales correcta")


    # Casos del I Corte: distributividad y producto matriz-vector.
    A_ex1 = [
        [Fraction(1, 2), Fraction(1, 3)],
        [Fraction(-1, 3), Fraction(1, 2)],
    ]
    u_ex1 = [Fraction(1), Fraction(0)]
    v_ex1 = [Fraction(0), Fraction(1)]
    suma_ex1 = sumar_vectores(u_ex1, v_ex1)
    izquierda_ex1 = multiplicar_matriz_vector(A_ex1, suma_ex1)
    derecha_ex1 = sumar_vectores(
        multiplicar_matriz_vector(A_ex1, u_ex1),
        multiplicar_matriz_vector(A_ex1, v_ex1),
    )
    assert izquierda_ex1 == derecha_ex1
    print("✓ I Corte: propiedad distributiva A(u+v)=Au+Av correcta")

    A_ex3 = [
        [Fraction(1, 2), Fraction(0), Fraction(1, 3)],
        [Fraction(0), Fraction(1, 2), Fraction(1, 3)],
        [Fraction(1, 3), Fraction(1, 3), Fraction(0)],
    ]
    v_ex3 = [Fraction(1), Fraction(1), Fraction(1)]
    producto_ex3 = multiplicar_matriz_vector(A_ex3, v_ex3)
    assert producto_ex3 == [Fraction(5, 6), Fraction(5, 6), Fraction(2, 3)]
    columnas_ex3 = [[fila[j] for fila in A_ex3] for j in range(3)]
    combinado_ex3 = [sum(v_ex3[j] * columnas_ex3[j][i] for j in range(3)) for i in range(3)]
    assert combinado_ex3 == producto_ex3
    print("✓ I Corte: A·v y combinación lineal de columnas correctas")

    # Regla de Sarrus (3×3) y regla de Cramer.
    F = Fraction
    m3 = [[F(2), F(0), F(1)], [F(1), F(3), F(2)], [F(1), F(1), F(1)]]
    sarrus = determinante_sarrus(m3)
    assert sarrus["determinante"] == determinante_cofactores(m3) == F(0)
    m3b = [[F(1), F(2), F(3)], [F(0), F(1), F(4)], [F(5), F(6), F(0)]]
    assert determinante_sarrus(m3b)["determinante"] == determinante_cofactores(m3b) == F(1)
    for invalida in ([[F(1), F(2)], [F(3), F(4)]], [[F(i + j) for j in range(4)] for i in range(4)]):
        try:
            determinante_sarrus(invalida)
            raise AssertionError("Sarrus debía rechazar una matriz que no es 3×3")
        except ValueError:
            pass
    print("✓ Regla de Sarrus correcta y coincide con cofactores")

    cramer2 = resolver_cramer([[F(2), F(1)], [F(1), F(3)]], [F(5), F(10)])
    assert cramer2["solucion"] == [F(1), F(3)]
    a_c = [[F(2), F(1), F(-1)], [F(-3), F(-1), F(2)], [F(-2), F(1), F(2)]]
    b_c = [F(8), F(-11), F(-3)]
    cramer3 = resolver_cramer(a_c, b_c)
    assert cramer3["solucion"] == [F(2), F(3), F(-1)]
    assert multiplicar_matriz_vector(a_c, cramer3["solucion"]) == b_c
    for a_mala, b_mala in (([[F(1), F(2)], [F(2), F(4)]], [F(1), F(2)]),
                           ([[F(1), F(2), F(3)], [F(4), F(5), F(6)]], [F(1), F(2)]),
                           ([[F(1), F(0)], [F(0), F(1)]], [F(1)])):
        try:
            resolver_cramer(a_mala, b_mala)
            raise AssertionError("Cramer debía rechazar este sistema")
        except ValueError:
            pass
    print("✓ Regla de Cramer correcta y valida det=0, no cuadrada y b incompatible")

    # Constructor visual de expresiones, pila R1–R7 y matrices base de solo lectura.
    A = [[F(1), F(2)], [F(3), F(4)]]
    B = [[F(0), F(1)], [F(1), F(1)]]
    base = MatricesBase()
    base.definir(A, B)
    try:
        base.definir(B, A)
        raise AssertionError("A y B no deben poder redefinirse")
    except RuntimeError:
        pass
    base.a[0][0] = F(99)  # modificar la copia no toca la original
    assert base.a == A and base.b == B

    esperado = restar_matrices(
        multiplicar_matrices(A, trasponer_matriz(B)),
        multiplicar_matrices(inversa_por_adjunta(A)["inversa"], B),
    )
    tokens = ["(", "A", "*", "B", "T", ")", "-", "(", "A", "INV", "*", "B", ")"]
    assert evaluar_tokens(tokens, base.contexto()) == esperado
    assert evaluar_tokens(["A", "+", "B", "*", "B"], base.contexto()) == sumar_matrices(A, multiplicar_matrices(B, B))
    print("✓ Expresión (A·Bᵀ) − (A⁻¹·B) evaluada y con precedencia correcta")

    constructor = ConstructorExpresion()
    assert siguientes_permitidos([]) >= {"A", "B", "R1", "("} and "+" not in siguientes_permitidos([])
    for token in ("(", "A", "T"):
        constructor.agregar(token)
    assert ")" in constructor.permitidos and not constructor.completa
    constructor.agregar(")")
    assert constructor.completa and constructor.texto == "(Aᵀ)" and ")" not in constructor.permitidos
    for invalido in ("A", "("):
        try:
            constructor.agregar(invalido)
            raise AssertionError("Token inválido aceptado")
        except ValueError:
            pass
    constructor.deshacer()
    assert constructor.texto == "(Aᵀ"
    print("✓ Constructor: transiciones, paréntesis y deshacer")

    pila = PilaResultados()
    for k in range(7):
        assert pila.guardar([[F(k)]]) == k
    assert pila.esta_llena and pila.cantidad == 7 and pila.indice_mas_antiguo == 0
    try:
        pila.guardar([[F(7)]])
        raise AssertionError("La pila llena debe rechazar sin confirmación")
    except OverflowError:
        pass
    assert pila.guardar([[F(7)]], reemplazar=True) == 0 and pila.obtener(0) == [[F(7)]]
    assert pila.indice_mas_antiguo == 1
    pila.eliminar(3)
    assert pila.cantidad == 6 and "R4" not in pila.contexto() and pila.guardar([[F(8)]]) == 3
    try:
        evaluar_tokens(["R5", "+", "A"], {"A": A})
        raise AssertionError("R5 vacío debía fallar")
    except ValueError:
        pass
    print("✓ Pila R1–R7: límite de 7, reemplazo del más antiguo y eliminación")

    prop = comprobar_traspuesta_del_producto(A, B)
    assert prop["se_cumple"] and not prop["incorrecta_se_cumple"]
    print("✓ (A·B)ᵀ = BᵀAᵀ se cumple y AᵀBᵀ falla como contraejemplo")

    # Módulo III: verificador de propiedades (modulos/modulo_matrices.py).
    A2, B2, C2 = [[2, 1], [5, 3]], [[1, 2], [0, 1]], [[3, 0], [1, 1]]
    props = verificar_propiedades(A2, B2, C2)
    assert len(props) == 26 and all(p["aplica"] for p in props)
    # Todas se cumplen salvo A·B = B·A, que es informativa (el producto no es conmutativo).
    assert all(p["cumple"] for p in props if not p["informativa"])
    assert [p for p in props if p["informativa"]][0]["cumple"] is False
    # Matriz no cuadrada o singular: las propiedades de det/inversa se omiten con motivo, sin fallar.
    no_cuadrada = {p["nombre"]: p for p in verificar_propiedades([[1, 2, 3], [4, 5, 6]])}
    assert not no_cuadrada["(A⁻¹)⁻¹ = A"]["aplica"] and "cuadrada" in no_cuadrada["(A⁻¹)⁻¹ = A"]["motivo"]
    assert not no_cuadrada["A + B = B + A"]["aplica"] and "Falta" in no_cuadrada["A + B = B + A"]["motivo"]
    singular = {p["nombre"]: p for p in verificar_propiedades([[1, 2], [2, 4]], B2)}
    assert not singular["(A⁻¹)⁻¹ = A"]["aplica"] and "singular" in singular["(A⁻¹)⁻¹ = A"]["motivo"]
    # Validación de entradas: solo enteros o fracciones.
    try:
        validar_matriz([[1, "x"], [2, 3]])
        assert False
    except ValueError:
        pass
    assert all(p["diagnostico"] == ("Se cumple" if p["cumple"] else "No se cumple") for p in props)
    # Matriz 3×3 con inversa: las 26 propiedades se calculan y solo A·B = B·A falla.
    props3 = verificar_propiedades([[2, 0, 1], [1, 3, 2], [0, 1, 4]], [[1, 2, 0], [0, 1, 1], [1, 0, 2]],
                                   [[1, 1, 0], [0, 2, 1], [3, 0, 1]])
    assert all(p["aplica"] for p in props3)
    assert [p["nombre"] for p in props3 if not p["cumple"]] == ["A · B = B · A  (el producto NO es conmutativo)"]
    print("✓ Verificador de propiedades: 26 igualdades, 'Se cumple'/'No se cumple', omisión con motivo y validación")

    # Programa 6: factorización LU y solución de Ax = b (modulos/modulo_lu.py).
    A_lu, b_lu = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]], [5, -2, 9]
    lu = factorizar_lu(A_lu)
    assert lu["matriz_L"] == [[1, 0, 0], [2, 1, 0], [-1, -1, 1]]
    assert lu["matriz_U"] == [[2, 1, 1], [0, -8, -2], [0, 0, 1]]
    assert verificar_factorizacion(A_lu, lu["matriz_L"], lu["matriz_U"])["es_correcta"]
    resolucion = resolver_con_lu(A_lu, b_lu)
    assert resolucion["vector_y"] == [5, -12, 2] and resolucion["vector_x"] == [1, 1, 2]
    assert resolucion["comprobacion_exitosa"] and resolucion["verificacion"]["es_correcta"]
    assert sustitucion_adelante(lu["matriz_L"], b_lu)["vector_y"] == [5, -12, 2]
    assert sustitucion_atras(lu["matriz_U"], [5, -12, 2])["vector_x"] == [1, 1, 2]
    # Fracciones exactas y matrices rectangulares: A = LU con L m×m y U m×n.
    for rectangular in ([[1, 2, 3], [4, 5, 6]], [[1, 2], [3, 4], [5, 6]], [[1, 2], [2, 4]]):
        factores = factorizar_lu(rectangular)
        assert len(factores["matriz_L"]) == len(rectangular) == len(factores["matriz_L"][0])
        assert verificar_factorizacion(rectangular, factores["matriz_L"], factores["matriz_U"])["es_correcta"]
    fraccionaria = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(1, 4), Fraction(5, 6)]]
    assert resolver_con_lu(fraccionaria, [1, 2])["comprobacion_exitosa"]
    # Pivote cero que exige permutar: se detiene con el mensaje de la tarea; una columna de ceros no lo exige.
    try:
        factorizar_lu([[0, 1], [1, 0]])
        assert False
    except ValueError as error:
        assert str(error) == MENSAJE_SIN_PERMUTACION
    assert verificar_factorizacion([[0, 2], [0, 4]], *[factorizar_lu([[0, 2], [0, 4]])[k] for k in ("matriz_L", "matriz_U")])["es_correcta"]
    # Resolver exige A cuadrada no singular y b de la longitud correcta.
    for matriz_mala, vector_malo in (([[1, 2], [2, 4]], [1, 2]), ([[1, 2, 3], [4, 5, 6]], [1, 2]), ([[1, 2], [3, 4]], [1])):
        try:
            resolver_con_lu(matriz_mala, vector_malo)
            assert False
        except ValueError:
            pass
    print("✓ Factorización LU: L y U, L·U == A, Ly = b, Ux = y, permutación, rectangulares y singulares")

    # Encadenamiento (Tarea 6, 4b): AB y BA se calculan una sola vez aunque varias propiedades los usen.
    A_enc, B_enc, C_enc = [[2, 0, 1], [1, 3, 2], [0, 1, 4]], [[1, 2, 0], [0, 1, 1], [1, 0, 2]], [[1, 1, 0], [0, 2, 1], [3, 0, 1]]
    llamadas = []
    producto_original = verificador.multiplicar_matrices
    verificador.multiplicar_matrices = lambda x, y: llamadas.append((x, y)) or producto_original(x, y)
    try:
        verificar_propiedades(A_enc, B_enc, C_enc)
    finally:
        verificador.multiplicar_matrices = producto_original
    a_fracc = [[Fraction(v) for v in fila] for fila in A_enc]
    b_fracc = [[Fraction(v) for v in fila] for fila in B_enc]
    assert sum(1 for x, y in llamadas if x == a_fracc and y == b_fracc) == 1
    assert sum(1 for x, y in llamadas if x == b_fracc and y == a_fracc) == 1
    # Escalares fraccionarios y una propiedad omitida no deja diagnóstico.
    assert all(p["aplica"] for p in verificar_propiedades(A_enc, B_enc, C_enc, Fraction(1, 2), Fraction(-3, 4)))
    assert all(p["diagnostico"] is None for p in verificar_propiedades([[1, 2, 3], [4, 5, 6]]) if not p["aplica"])
    print("✓ Encadenamiento: AB y BA se calculan una vez y los escalares fraccionarios se admiten")

    # Reglas de la tarea: módulos de cálculo sin input()/print() y sin librerías externas ni math.
    raiz = Path(__file__).resolve().parent.parent
    for archivo in list((raiz / "modulos").glob("*.py")) + list((raiz / "teoremas").glob("*.py")):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        llamados = {n.func.id for n in ast.walk(arbol) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        assert not llamados & {"print", "input"}, f"{archivo} usa print()/input()"
        importados = {n.module.split(".")[0] for n in ast.walk(arbol) if isinstance(n, ast.ImportFrom) and n.module}
        importados |= {alias.name.split(".")[0] for n in ast.walk(arbol) if isinstance(n, ast.Import) for alias in n.names}
        assert not importados & {"math", "numpy", "scipy", "sympy"}, f"{archivo} importa una librería prohibida"
    print("✓ Reglas: modulos/ y teoremas/ sin input(), print(), math ni librerías externas")

    # Contraste AA: un color legible no cambia y uno claro se oscurece hasta 4.5:1.
    assert asegurar_contraste("#22363B", "#FFFFFF") == "#22363B"
    coral = asegurar_contraste("#E87B70", "#FFFFFF")
    assert coral != "#E87B70" and contraste(coral, "#FFFFFF") >= 4.5
    gris = asegurar_contraste("#9AA6A8", ("#FFFFFF", "#EEF3F1"))
    assert min(contraste(gris, "#FFFFFF"), contraste(gris, "#EEF3F1")) >= 4.5
    print("✓ Contraste AA: asegurar_contraste conserva lo legible y oscurece lo demás")


if __name__ == "__main__":
    # La consola de Windows usa cp1252 y no puede imprimir ✓, ᵀ ni ⁻¹: se fuerza UTF-8.
    sys.stdout.reconfigure(encoding="utf-8")
    ejecutar_casos()

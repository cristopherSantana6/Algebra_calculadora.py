
"""
Descompone números enteros en base 10 y base 2.
Muestra las potencias, las operaciones y las conversiones
entre ambas bases.
"""


def validar_numero(numero, base):
    """Comprueba que el número pertenezca a la base indicada.
    Acepta enteros positivos y negativos.
    Rechaza los dígitos que no correspondan a la base.
    """
    numero = str(numero).strip()

    if not numero:
        raise ValueError("Debe ingresar un número.")

    if base not in (2, 10):
        raise ValueError("Solo se permiten las bases 2 y 10.")

    # Se permiten enteros positivos y negativos.
    signo = ""

    if numero[0] in ("-", "+"):
        signo = numero[0]
        numero = numero[1:]

    if not numero:
        raise ValueError("Debe ingresar al menos un dígito.")

    digitos_validos = "01" if base == 2 else "0123456789"

    if any(digito not in digitos_validos for digito in numero):
        raise ValueError(
            f"El número contiene dígitos no válidos para base {base}."
        )

    return signo, numero


def descomponer_numero(numero, base):
    """Descompone un número mediante las potencias de su base.
    Calcula su valor decimal y su representación binaria.
    Guarda los términos y las operaciones realizadas.
    """
    signo, digitos = validar_numero(numero, base)

    negativo = signo == "-" and any(d != "0" for d in digitos)
    valor_decimal = 0
    terminos = []
    operaciones = []

    cantidad = len(digitos)

    # Cada dígito se multiplica por la base elevada a su posición.
    for indice, digito in enumerate(digitos):
        potencia = cantidad - indice - 1
        valor_digito = int(digito)

        resultado = valor_digito * (base ** potencia)
        valor_decimal += resultado

        terminos.append(
            f"{valor_digito} × {base}^{potencia}"
        )

        operaciones.append({
            "digito": valor_digito,
            "potencia": potencia,
            "base": base,
            "resultado": resultado
        })

    if negativo:
        valor_decimal = -valor_decimal

    # Conversión a binario sin perder el signo.
    valor_absoluto = abs(valor_decimal)
    numero_binario = format(valor_absoluto, "b")

    if valor_decimal < 0:
        numero_binario = "-" + numero_binario

    numero_decimal = str(valor_decimal)

    # Mantener el número de origen tal como fue ingresado.
    numero_original = ("-" if negativo else "") + digitos

    resultado_conversion = (
        numero_binario if base == 10 else numero_decimal
    )

    base_destino = 2 if base == 10 else 10

    return {
        "numero_original": numero_original,
        "base_origen": base,
        "base_destino": base_destino,
        "numero_decimal": numero_decimal,
        "numero_binario": numero_binario,
        "resultado_conversion": resultado_conversion,
        "valor_decimal": valor_decimal,
        "terminos": terminos,
        "operaciones": operaciones,
        "negativo": negativo,
    }


def mostrar_procedimiento(datos):
    """Construye el procedimiento de la conversión posicional.
    Presenta la descomposición por potencias y las operaciones.
    Muestra la equivalencia entre las bases de origen y destino.
    """
    numero = datos["numero_original"]
    base = datos["base_origen"]
    base_destino = datos["base_destino"]

    terminos = datos["terminos"]
    operaciones = datos["operaciones"]

    signo_explicacion = (
        "El número es negativo. Se descompone su valor absoluto "
        "y se conserva el signo menos.\n\n"
        if datos["negativo"] else ""
    )

    # La descomposición se hace con magnitudes positivas.
    expresion = " + ".join(terminos)
    valores = [str(paso["resultado"]) for paso in operaciones]

    suma = " + ".join(valores)

    valor = abs(datos["valor_decimal"])
    resultado = datos["resultado_conversion"]

    explicacion = (
        f"NOTACIÓN POSICIONAL EN BASE {base}\n\n"
        f"Número ingresado: ({numero})_{base}\n\n"
        f"{signo_explicacion}"
        f"Descomposición por potencias:\n"
        f"{expresion}\n\n"
        f"Multiplicación de cada término:\n"
        f"{suma}\n\n"
        f"Suma de los términos:\n"
        f"{valor}\n\n"
        f"Conversión:\n"
        f"({numero})_{base} = ({resultado})_{base_destino}"
    )

    return explicacion


def convertir_decimal_binario(numero):
    """Convierte un número entero de base 10 a base 2.
    Utiliza la descomposición posicional para obtener el resultado.
    """
    datos = descomponer_numero(numero, 10)
    return datos["numero_binario"]


def convertir_binario_decimal(numero):
    """Convierte un número entero de base 2 a base 10.
    Utiliza la descomposición posicional para obtener el resultado.
    """
    datos = descomponer_numero(numero, 2)
    return datos["valor_decimal"]

"""
Algoritmo de Rastro Consciente (v2)
-------------------------------------
Logica para que un "explorador" sin mapa completo del salon (laberinto)
encuentre una salida a partir de una entrada.

Formato del laberinto:
    'A' = entrada
    'B' = salida
    '1' = muro
    '0' = pasillo (camino libre)

Idea del algoritmo:
  1. Sigue la pared con la mano derecha (prioridad de giro:
     derecha, frente, izquierda, atras).
  2. Lleva memoria de cuantas veces ha visitado cada casilla,
     para evitar quedar atrapado en ciclos infinitos.
"""

from collections import defaultdict

MURO = "1"
LIBRE = "0"
ENTRADA = "A"
SALIDA = "B"

# Direcciones como vectores (fila, columna)
ARRIBA = (-1, 0)
ABAJO = (1, 0)
IZQUIERDA = (0, -1)
DERECHA = (0, 1)


def girar_derecha(direccion):
    return {
        ARRIBA: DERECHA,
        DERECHA: ABAJO,
        ABAJO: IZQUIERDA,
        IZQUIERDA: ARRIBA,
    }[direccion]


def girar_izquierda(direccion):
    return {
        ARRIBA: IZQUIERDA,
        IZQUIERDA: ABAJO,
        ABAJO: DERECHA,
        DERECHA: ARRIBA,
    }[direccion]


def opuesta(direccion):
    return (-direccion[0], -direccion[1])


def casilla_en(pos, direccion):
    return (pos[0] + direccion[0], pos[1] + direccion[1])


def es_valida(matriz, pos):
    filas = len(matriz)
    columnas = len(matriz[0])
    f, c = pos
    if 0 <= f < filas and 0 <= c < columnas:
        return matriz[f][c] != MURO
    return False


def encontrar_simbolo(matriz, simbolo):
    """Busca en la matriz la posicion (fila, columna) de un simbolo dado."""
    for f, fila in enumerate(matriz):
        for c, valor in enumerate(fila):
            if valor == simbolo:
                return (f, c)
    raise ValueError(f"No se encontro el simbolo '{simbolo}' en el laberinto")


def rastro_consciente(matriz, direccion_inicial=DERECHA, verbose=False):
    entrada = encontrar_simbolo(matriz, ENTRADA)
    salida = encontrar_simbolo(matriz, SALIDA)

    filas = len(matriz)
    columnas = len(matriz[0])

    contador = defaultdict(int)
    posicion_actual = entrada
    direccion_actual = direccion_inicial

    limite_visitas = filas * columnas * 3
    pasos_totales = 0
    camino = []

    while posicion_actual != salida:
        pasos_totales += 1
        camino.append(posicion_actual)
        contador[posicion_actual] += 1

        if pasos_totales > limite_visitas:
            return None, camino  # sin solucion

        dir_derecha = girar_derecha(direccion_actual)
        dir_frente = direccion_actual
        dir_izq = girar_izquierda(direccion_actual)
        dir_atras = opuesta(direccion_actual)

        candidatas = [dir_derecha, dir_frente, dir_izq, dir_atras]
        opciones_validas = []

        for direccion in candidatas:
            vecino = casilla_en(posicion_actual, direccion)
            if es_valida(matriz, vecino):
                opciones_validas.append((direccion, vecino, contador[vecino]))

        if not opciones_validas:
            return None, camino  # encerrado, sin solucion

        # Elegir la opcion con menor numero de visitas
        mejor_opcion = opciones_validas[0]
        for opcion in opciones_validas:
            if opcion[2] < mejor_opcion[2]:
                mejor_opcion = opcion

        direccion_actual, posicion_actual, _ = mejor_opcion

        if verbose:
            print(f"Paso {pasos_totales}: -> {posicion_actual} (dir {direccion_actual})")

    camino.append(salida)
    return camino, camino


def imprimir_laberinto(matriz, camino=None):
    """
    Imprime el laberinto con un espacio entre cada simbolo para
    que no se vea amontonado. La entrada y la salida se conservan
    como 'A' y 'B'; el resto de la ruta se marca con 'o'.
    """
    camino_set = set(camino) if camino else set()
    # Excluimos entrada y salida de marcarse como "o" para que se sigan viendo A y B
    entrada = encontrar_simbolo(matriz, ENTRADA)
    salida = encontrar_simbolo(matriz, SALIDA)

    for f, fila in enumerate(matriz):
        celdas = []
        for c, valor in enumerate(fila):
            pos = (f, c)
            if pos == entrada:
                celdas.append("A")
            elif pos == salida:
                celdas.append("B")
            elif pos in camino_set:
                celdas.append("o")
            else:
                celdas.append(valor)
        print(" ".join(celdas))


if __name__ == "__main__":
    # 'A' = entrada, 'B' = salida, '1' = muro, '0' = pasillo
    #LABERINTO 1
    # laberinto = [
    #     ["A", "0", "1", "0", "0", "0"],
    #     ["1", "0", "1", "0", "1", "0"],
    #     ["0", "0", "0", "0", "1", "0"],
    #     ["0", "1", "1", "1", "1", "0"],
    #     ["0", "0", "0", "0", "0", "0"],
    #     ["1", "1", "1", "1", "1", "B"],
    # ]

    #LABERINTO 2
    # laberinto = [
    # ["A", "0", "1", "0", "0", "0", "1", "0", "0", "0"],
    # ["1", "0", "1", "0", "1", "0", "1", "0", "1", "0"],
    # ["1", "0", "0", "0", "1", "0", "0", "0", "1", "0"],
    # ["1", "1", "1", "0", "1", "1", "1", "0", "1", "0"],
    # ["0", "0", "1", "0", "0", "0", "1", "0", "0", "0"],
    # ["0", "1", "1", "1", "1", "0", "1", "1", "1", "0"],
    # ["0", "0", "0", "0", "1", "0", "0", "0", "0", "0"],
    # ["1", "1", "1", "0", "1", "1", "1", "1", "1", "B"],
    # ]

    #LABERINTO 3
    # laberinto = [
    # ["A", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"],
    # ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1"],
    # ["0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1"],
    # ["0", "1", "1", "1", "1", "1", "1", "1", "0", "1", "0", "1"],
    # ["0", "1", "0", "0", "0", "0", "0", "1", "0", "1", "0", "1"],
    # ["0", "1", "0", "1", "1", "1", "0", "1", "0", "1", "0", "1"],
    # ["0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1"],
    # ["0", "1", "0", "1", "0", "0", "0", "1", "0", "1", "0", "0"],
    # ["0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "0"],
    # ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "B"],
    # ]

    #LABERINTO 4
    # laberinto = [
    # ["A", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
    # ["1", "0", "1", "0", "1", "1", "1", "0", "1", "0", "1", "0"],
    # ["1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "1", "0"],
    # ["1", "1", "1", "1", "1", "0", "1", "1", "1", "0", "1", "0"],
    # ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1", "0"],
    # ["0", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "0"],
    # ["0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
    # ["1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "1"],
    # ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0"],
    # ["0", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "0"],
    # ["0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0"],
    # ["1", "1", "1", "0", "1", "0", "1", "1", "1", "1", "1", "B"],
    # ]

    #LABERINTO 5
    # laberinto = [
    # ["A", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0"],
    # ["1", "1", "1", "0", "1", "0", "1", "1", "1", "0", "1", "0", "1", "1", "0"],
    # ["0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "1", "0"],
    # ["0", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1", "0"],
    # ["0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0"],
    # ["1", "1", "1", "1", "1", "1", "1", "0", "1", "0", "1", "1", "1", "1", "0"],
    # ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0"],
    # ["0", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "0"],
    # ["0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0"],
    # ["0", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "0"],
    # ["0", "1", "0", "1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
    # ["0", "1", "0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "1", "0"],
    # ["0", "1", "0", "1", "0", "1", "0", "0", "0", "0", "0", "0", "0", "1", "0"],
    # ["0", "0", "0", "1", "0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "0"],
    # ["0", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "B"],
    # ]

    # LABERINTO 6 (20x20 - Múltiples Soluciones)
    laberinto = [
    ["A", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
    ["1", "1", "1", "0", "1", "0", "1", "1", "1", "0", "1", "0", "1", "1", "1", "0", "1", "0", "1", "0"],
    ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0"],
    ["0", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0"],
    ["1", "1", "1", "1", "1", "1", "1", "0", "1", "0", "1", "1", "1", "1", "1", "1", "1", "0", "1", "0"],
    ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
    ["0", "1", "1", "1", "1", "0", "1", "1", "1", "0", "1", "0", "1", "1", "1", "0", "1", "1", "1", "0"],
    ["0", "1", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "1", "0"],
    ["0", "1", "0", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "1", "0", "1", "0"],
    ["0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0"],
    ["1", "1", "0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "0", "1", "0", "1", "1", "1", "0"],
    ["0", "0", "0", "1", "0", "1", "0", "0", "0", "1", "0", "1", "0", "0", "0", "0", "1", "0", "0", "0"],
    ["0", "1", "1", "1", "0", "1", "0", "1", "0", "1", "0", "1", "0", "1", "1", "1", "1", "0", "1", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "1", "0"],
    ["1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "0"],
    ["0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
    ["0", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "0"],
    ["0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0"],
    ["1", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "0", "B"]
    ]
 

    print("Laberinto original:")
    imprimir_laberinto(laberinto)
    print()

    camino, recorrido = rastro_consciente(laberinto, verbose=False)

    print()
    if camino:
        print(f"Camino encontrado en {len(camino)} pasos:")
        print(camino)
        print()
        print("Laberinto con la ruta marcada ('o'):")
        imprimir_laberinto(laberinto, camino)
    else:
        print("No se encontro una salida (limite de pasos alcanzado).")
        print(f"Pasos explorados: {len(recorrido)}")
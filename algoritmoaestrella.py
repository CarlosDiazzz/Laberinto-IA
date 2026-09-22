"""
Algoritmo A* (A Estrella)
--------------------------
Implementacion basada en la estructura del articulo de DataCamp:
"El Algoritmo A*: Guia completa" (datacamp.com/es/tutorial/a-star-algorithm)

Adaptaciones respecto al articulo original:
    - El articulo usa una cuadricula numpy (0 = libre, 1 = obstaculo) con
      movimientos en 8 direcciones (incluye diagonales) y heuristica Euclidiana.
    - Aqui usamos el formato de laberinto con simbolos:
          'A' = entrada
          'B' = salida
          '1' = muro
          '0' = pasillo
      y solo 4 direcciones de movimiento (arriba, abajo, izquierda, derecha),
      por lo que la heuristica adecuada es la distancia MANHATTAN
      (tal como recomienda el propio articulo para mapas tipo cuadricula).

Estructura del nodo (igual que en el articulo):
    {
        'position': (fila, columna),
        'g': costo real desde la entrada,
        'h': estimacion heuristica hasta la salida,
        'f': g + h,
        'parent': nodo padre (para reconstruir la ruta)
    }
"""

from typing import List, Tuple, Dict, Optional
import heapq

MURO = "1"
ENTRADA = "A"
SALIDA = "B"


# ---------------------------------------------------------------
# Paso 1: Funcion para crear un nodo (igual estructura que DataCamp)
# ---------------------------------------------------------------
def crear_nodo(position: Tuple[int, int], g: float = float("inf"),
               h: float = 0.0, parent: Optional[Dict] = None) -> Dict:
    """
    Crea un nodo para el algoritmo A*.

    Args:
        position: coordenadas (fila, columna) del nodo
        g: costo desde la entrada hasta este nodo (por defecto: infinito)
        h: costo estimado desde este nodo hasta la salida (por defecto: 0)
        parent: nodo padre (por defecto: None)

    Returns:
        Diccionario con la informacion del nodo
    """
    return {
        "position": position,
        "g": g,
        "h": h,
        "f": g + h,
        "parent": parent,
    }


# ---------------------------------------------------------------
# Paso 2: Funciones auxiliares
# ---------------------------------------------------------------
def calcular_heuristica(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calcula la distancia estimada entre dos puntos usando distancia Manhattan.
    Se usa Manhattan (en vez de Euclidiana como en el articulo original)
    porque en este laberinto solo se permite moverse en 4 direcciones,
    no en diagonal.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)


def encontrar_simbolo(matriz: List[List[str]], simbolo: str) -> Tuple[int, int]:
    """Busca en la matriz la posicion (fila, columna) de un simbolo dado."""
    for f, fila in enumerate(matriz):
        for c, valor in enumerate(fila):
            if valor == simbolo:
                return (f, c)
    raise ValueError(f"No se encontro el simbolo '{simbolo}' en el laberinto")


def obtener_vecinos_validos(grid: List[List[str]],
                             position: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Obtiene todas las posiciones vecinas validas en la cuadricula.

    Args:
        grid: matriz de simbolos ('0' = pasillo, '1' = muro, 'A'/'B' = entrada/salida)
        position: posicion actual (fila, columna)

    Returns:
        Lista de posiciones vecinas validas
    """
    x, y = position
    filas = len(grid)
    columnas = len(grid[0])

    # Solo 4 movimientos (sin diagonales), a diferencia del articulo original
    movimientos_posibles = [
        (x + 1, y),  # Abajo
        (x - 1, y),  # Arriba
        (x, y + 1),  # Derecha
        (x, y - 1),  # Izquierda
    ]

    return [
        (nx, ny) for nx, ny in movimientos_posibles
        if 0 <= nx < filas and 0 <= ny < columnas  # dentro de la cuadricula
        and grid[nx][ny] != MURO                    # no es un muro
    ]


def reconstruir_camino(nodo_meta: Dict) -> List[Tuple[int, int]]:
    """
    Reconstruye el camino desde la meta hasta la entrada
    siguiendo los punteros "parent" de cada nodo.
    """
    camino = []
    actual = nodo_meta

    while actual is not None:
        camino.append(actual["position"])
        actual = actual["parent"]

    return camino[::-1]  # invertir para que quede de entrada -> salida


# ---------------------------------------------------------------
# Paso 3: Implementacion principal del algoritmo A*
# ---------------------------------------------------------------
def encontrar_camino(grid: List[List[str]]) -> List[Tuple[int, int]]:
    """
    Encuentra el camino optimo usando el algoritmo A*.

    Args:
        grid: matriz de simbolos con 'A' (entrada), 'B' (salida),
              '1' (muro) y '0' (pasillo)

    Returns:
        Lista de posiciones que representan el camino optimo,
        o lista vacia si no existe camino.
    """
    entrada = encontrar_simbolo(grid, ENTRADA)
    salida = encontrar_simbolo(grid, SALIDA)

    # Inicializar el nodo de entrada
    nodo_entrada = crear_nodo(
        position=entrada,
        g=0,
        h=calcular_heuristica(entrada, salida),
    )

    # Inicializar listas abierta y cerrada
    lista_abierta = [(nodo_entrada["f"], entrada)]   # cola de prioridad
    dict_abiertos = {entrada: nodo_entrada}           # busqueda rapida de nodos
    conjunto_cerrados = set()                         # nodos ya explorados

    while lista_abierta:
        # Obtener el nodo con menor valor f
        _, posicion_actual = heapq.heappop(lista_abierta)
        nodo_actual = dict_abiertos[posicion_actual]

        # Verificar si llegamos a la salida
        if posicion_actual == salida:
            return reconstruir_camino(nodo_actual)

        conjunto_cerrados.add(posicion_actual)

        # Explorar vecinos
        for pos_vecino in obtener_vecinos_validos(grid, posicion_actual):
            # Omitir si ya fue explorado
            if pos_vecino in conjunto_cerrados:
                continue

            # Calcular el nuevo costo tentativo del camino
            g_tentativo = nodo_actual["g"] + 1  # cada paso cuesta 1

            # Crear o actualizar el vecino
            if pos_vecino not in dict_abiertos:
                vecino = crear_nodo(
                    position=pos_vecino,
                    g=g_tentativo,
                    h=calcular_heuristica(pos_vecino, salida),
                    parent=nodo_actual,
                )
                heapq.heappush(lista_abierta, (vecino["f"], pos_vecino))
                dict_abiertos[pos_vecino] = vecino
            elif g_tentativo < dict_abiertos[pos_vecino]["g"]:
                # Se encontro un camino mejor hacia el vecino
                vecino = dict_abiertos[pos_vecino]
                vecino["g"] = g_tentativo
                vecino["f"] = g_tentativo + vecino["h"]
                vecino["parent"] = nodo_actual

    return []  # no se encontro camino


# ---------------------------------------------------------------
# Utilidad para imprimir el laberinto (formato espaciado)
# ---------------------------------------------------------------
def imprimir_laberinto(matriz: List[List[str]],
                        camino: Optional[List[Tuple[int, int]]] = None) -> None:
    camino_set = set(camino) if camino else set()
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


# ---------------------------------------------------------------
# Ejemplo de uso
# ---------------------------------------------------------------
if __name__ == "__main__":
    laberinto = [
        ["A", "0", "1", "0", "0", "0"],
        ["1", "0", "1", "0", "1", "0"],
        ["0", "0", "0", "0", "1", "0"],
        ["0", "1", "1", "1", "1", "0"],
        ["0", "0", "0", "0", "0", "0"],
        ["1", "1", "1", "1", "1", "B"],
    ]

    print("Laberinto original:")
    imprimir_laberinto(laberinto)
    print()

    camino = encontrar_camino(laberinto)

    if camino:
        print(f"Camino encontrado con {len(camino)} pasos!")
        print(camino)
        print()
        print("Laberinto con la ruta marcada ('o'):")
        imprimir_laberinto(laberinto, camino)
    else:
        print("No se encontro un camino!")
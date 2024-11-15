from queue import Queue, LifoQueue, PriorityQueue  # Importa clases de colas para BFS, DFS y algoritmos de prioridad
from puzzle2 import Puzzle  # Importa la clase Puzzle que maneja el estado y movimientos del puzzle

def bfs(estado_inicial, estado_objetivo):
    """Implementa Búsqueda en Anchura (BFS)."""
    visitados = set()  # Conjunto para guardar los estados ya visitados
    frontera = Queue()  # Cola FIFO para manejar la frontera en BFS
    puzzle_inicial = Puzzle(estado_inicial)  # Crea el estado inicial como un objeto Puzzle
    frontera.put((puzzle_inicial, []))  # Cada elemento en la frontera es una tupla (estado_actual, camino)

    while not frontera.empty():  # Mientras haya elementos en la frontera
        puzzle, camino = frontera.get()  # Extrae el primer elemento de la frontera
        estado_actual = puzzle.estado  # Obtiene el estado actual

        # Comprueba si se alcanzó el objetivo
        if puzzle.es_igual(estado_objetivo):
            return camino + [estado_actual]  # Devuelve el camino completo si se encontró solución

        # Marca el estado actual como visitado
        visitados.add(tuple(map(tuple, estado_actual)))

        # Genera movimientos posibles desde el estado actual
        for nuevo_estado in puzzle.generar_movimientos():
            # Verifica si el nuevo estado ya ha sido visitado
            if tuple(map(tuple, nuevo_estado)) not in visitados:
                # Agrega el nuevo estado a la frontera con el camino actualizado
                frontera.put((Puzzle(nuevo_estado), camino + [estado_actual]))

    return None  # Devuelve None si no se encuentra solución

def dfs(estado_inicial, estado_objetivo):
    """Implementa Búsqueda en Profundidad (DFS)."""
    visitados = set()  # Conjunto para almacenar los estados ya visitados
    frontera = LifoQueue()  # Pila LIFO para manejar la frontera en DFS
    puzzle_inicial = Puzzle(estado_inicial)  # Crea el estado inicial como objeto Puzzle
    frontera.put((puzzle_inicial, []))  # Agrega el estado inicial a la frontera

    while not frontera.empty():  # Mientras haya elementos en la frontera
        puzzle, camino = frontera.get()  # Extrae el último elemento de la frontera
        estado_actual = puzzle.estado  # Obtiene el estado actual

        # Comprueba si se alcanzó el objetivo
        if puzzle.es_igual(estado_objetivo):
            return camino + [estado_actual]  # Devuelve el camino si se encontró solución

        estado_tuple = tuple(map(tuple, estado_actual))  # Convierte el estado a una tupla para almacenar
        # Salta si el estado ya fue visitado
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)  # Marca el estado como visitado

        # Genera y agrega movimientos posibles a la frontera
        for nuevo_estado in puzzle.generar_movimientos():
            nuevo_puzzle = Puzzle(nuevo_estado)
            frontera.put((nuevo_puzzle, camino + [estado_actual]))  # Actualiza el camino al añadir el nuevo estado

    return None  # Devuelve None si no se encuentra solución

def heuristica_manhattan(estado, objetivo):
    """Calcula la distancia de Manhattan entre dos estados."""
    distancia = 0  # Variable para acumular la distancia de Manhattan
    for i in range(3):  # Itera sobre filas
        for j in range(3):  # Itera sobre columnas
            valor = estado[i][j]  # Obtiene el valor de la celda actual
            if valor != 0:  # Ignora la posición vacía (0)
                # Busca la posición del valor en el estado objetivo
                for x in range(3):
                    for y in range(3):
                        if objetivo[x][y] == valor:
                            # Suma la distancia de Manhattan
                            distancia += abs(x - i) + abs(y - j)
                            break
    return distancia  # Devuelve la distancia de Manhattan total

def astar(estado_inicial, estado_objetivo):
    """Implementa el algoritmo A*."""
    visitados = set()  # Conjunto para almacenar los estados visitados
    frontera = PriorityQueue()  # Cola de prioridad para manejar la frontera
    puzzle_inicial = Puzzle(estado_inicial)  # Crea el estado inicial como objeto Puzzle
    frontera.put((0, puzzle_inicial, []))  # Agrega el estado inicial con costo 0 a la frontera

    while not frontera.empty():  # Mientras haya elementos en la frontera
        _, puzzle, camino = frontera.get()  # Extrae el elemento con menor costo
        estado_actual = puzzle.estado  # Obtiene el estado actual

        # Comprueba si se alcanzó el objetivo
        if puzzle.es_igual(estado_objetivo):
            return camino + [estado_actual]  # Devuelve el camino completo si se encontró solución

        # Marca el estado actual como visitado
        visitados.add(tuple(map(tuple, estado_actual)))

        # Genera y evalúa cada movimiento posible
        for nuevo_estado in puzzle.generar_movimientos():
            if tuple(map(tuple, nuevo_estado)) not in visitados:
                # Calcula el costo del camino + heurística
                costo = len(camino) + 1 + heuristica_manhattan(nuevo_estado, estado_objetivo)
                # Agrega el nuevo estado a la frontera con el costo calculado
                frontera.put((costo, Puzzle(nuevo_estado), camino + [estado_actual]))

    return None  # Devuelve None si no se encuentra solución

def greedy(estado_inicial, estado_objetivo):
    """Implementa la Búsqueda Greedy."""
    visitados = set()  # Conjunto para almacenar los estados visitados
    frontera = PriorityQueue()  # Cola de prioridad para manejar la frontera
    puzzle_inicial = Puzzle(estado_inicial)  # Crea el estado inicial como objeto Puzzle
    # Agrega el estado inicial con la heurística de Manhattan a la frontera
    frontera.put((heuristica_manhattan(puzzle_inicial.estado, estado_objetivo), puzzle_inicial, []))

    while not frontera.empty():  # Mientras haya elementos en la frontera
        _, puzzle, camino = frontera.get()  # Extrae el elemento con menor heurística
        estado_actual = puzzle.estado  # Obtiene el estado actual

        # Comprueba si se alcanzó el objetivo
        if puzzle.es_igual(estado_objetivo):
            return camino + [estado_actual]  # Devuelve el camino completo si se encontró solución

        # Marca el estado actual como visitado
        visitados.add(tuple(map(tuple, estado_actual)))

        # Genera y evalúa cada movimiento posible
        for nuevo_estado in puzzle.generar_movimientos():
            if tuple(map(tuple, nuevo_estado)) not in visitados:
                # Agrega el nuevo estado a la frontera con la heurística calculada
                frontera.put((heuristica_manhattan(nuevo_estado, estado_objetivo), Puzzle(nuevo_estado), camino + [estado_actual]))

    return None  # Devuelve None si no se encuentra solución

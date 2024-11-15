import copy  # Importa el módulo copy para realizar copias profundas de estructuras de datos

class Puzzle:
    def __init__(self, estado):
        self.estado = estado  # Inicializa el estado del puzzle con el estado dado

    def encontrar_espacio_vacio(self):
        # Recorre la matriz para encontrar la posición del espacio vacío (representado por 0)
        for i in range(3):  # Recorre filas
            for j in range(3):  # Recorre columnas
                if self.estado[i][j] == 0:  # Verifica si la celda es el espacio vacío
                    return i, j  # Retorna las coordenadas del espacio vacío
        return None  # Retorna None si no se encuentra el espacio vacío

    def generar_movimientos(self):
        """Genera los movimientos posibles del espacio vacío y retorna una lista de estados resultantes."""
        movimientos = []  # Lista para almacenar los estados después de cada movimiento
        x, y = self.encontrar_espacio_vacio()  # Obtiene la posición del espacio vacío
        # Lista de direcciones posibles con desplazamientos en x e y
        direcciones = [("arriba", -1, 0), ("abajo", 1, 0), ("izquierda", 0, -1), ("derecha", 0, 1)]

        for direccion, dx, dy in direcciones:
            # Calcula las nuevas coordenadas del espacio vacío al moverlo en una dirección
            nuevo_x, nuevo_y = x + dx, y + dy
            # Verifica que las nuevas coordenadas estén dentro de los límites de la matriz
            if 0 <= nuevo_x < 3 and 0 <= nuevo_y < 3:
                # Crea una copia profunda del estado actual para aplicar el movimiento
                nuevo_estado = [fila[:] for fila in self.estado]
                # Intercambia el espacio vacío con el valor en las nuevas coordenadas
                nuevo_estado[x][y], nuevo_estado[nuevo_x][nuevo_y] = nuevo_estado[nuevo_x][nuevo_y], nuevo_estado[x][y]
                # Agrega el nuevo estado a la lista de movimientos
                movimientos.append(nuevo_estado)
        return movimientos  # Retorna la lista de estados resultantes de los movimientos posibles

    def es_igual(self, otro_estado):
        # Compara el estado actual con otro estado dado para verificar si son iguales
        return self.estado == otro_estado

    def __hash__(self):
        # Genera un hash del estado para poder usarlo en conjuntos o como clave en diccionarios
        return hash(tuple(map(tuple, self.estado)))

    def __repr__(self):
        # Define cómo se representará el objeto Puzzle cuando se imprima
        return repr(self.estado)

    def calcular_distancia_manhattan(self, objetivo):
        """Calcula la distancia de Manhattan entre el estado actual y el estado objetivo."""
        distancia = 0  # Variable para acumular la distancia total de Manhattan
        # Recorre cada celda en la matriz del estado actual
        for i in range(3):  # Filas
            for j in range(3):  # Columnas
                valor = self.estado[i][j]  # Obtiene el valor de la celda actual
                if valor != 0:  # Ignora el espacio vacío (0)
                    # Calcula la posición objetivo del valor en la matriz 3x3
                    objetivo_x, objetivo_y = divmod(valor - 1, 3)
                    # Suma la distancia de Manhattan entre la posición actual y la posición objetivo
                    distancia += abs(objetivo_x - i) + abs(objetivo_y - j)
        return distancia  # Retorna la distancia total de Manhattan

    def __lt__(self, otro):
        """Define la comparación menor que (<) entre dos objetos Puzzle.
        Utiliza la distancia de Manhattan respecto al estado objetivo para realizar la comparación."""
        # Compara la distancia de Manhattan de este puzzle con otro puzzle
        return self.calcular_distancia_manhattan([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) < otro.calcular_distancia_manhattan([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

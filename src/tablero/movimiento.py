from collections import deque
from src.tablero.direcciones import DIRECCION_POR_PASO

def calcular_alcance(mapa, inicio, movimiento, ocupadas):
    """Devuelve un diccionario {casilla: casilla_anterior} con todas las casillas
    a las que se puede llegar desde 'inicio' en 'movimiento' pasos o menos.
    'ocupadas' es un conjunto de casillas bloqueadas (otras unidades)."""
    desdeDondeVino = {inicio: None}        # desde dónde se llegó a cada casilla (también sirve de "visitadas") desdeDondeVino = {llegue: desdedonde}
    distancias = {inicio: 0}       # cuántos pasos cuesta llegar a cada casilla. distancia = {casilla: cuantosmovnecesito}
    cola = deque([inicio])         # Cola de casillas 

    while cola:
        actual = cola.popleft()                  # sale la primera de la cola
        if distancias[actual] == movimiento:     # ya no le quedan pasos: no se expande
            continue
        col, fila = actual
        for dcol, dfila in DIRECCION_POR_PASO:   # los 4 vecinos 
            vecina = (col + dcol, fila + dfila)
            if vecina in desdeDondeVino:                 # ya visitada
                continue
            if not mapa.esta_dentro(*vecina):    # fuera del mapa
                continue
            if vecina in ocupadas:               # hay alguien parado
                continue
            desdeDondeVino[vecina] = actual
            distancias[vecina] = distancias[actual] + 1
            cola.append(vecina)                  # entra al final de la cola
    return desdeDondeVino

def reconstruir_camino(desdeDondeVino, destino):
    """Lista de casillas desde el inicio (sin incluirlo) hasta 'destino'."""
    camino = []
    actual = destino
    while desdeDondeVino[actual] is not None:            # el inicio es el único sin padre
        camino.append(actual)
        actual = desdeDondeVino[actual]
    camino.reverse()                             # estaba de atrás hacia adelante
    return camino

def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])#La formula es: col + fila . Ej = max (2,3) = 2 + 3 = 5
def distancia_diagonal(a, b): #Hace lo mismo que distancia, pero la mide con las diagonales
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) #La formula es: max(col, fila). Ej = max (2,3) = 3
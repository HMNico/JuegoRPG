from src.tablero.direcciones import DIRECCION_POR_PASO
import random

def casillas_atacables(mapa, origen, alcance_min, alcance_max,ocupadas):
    col, fila = origen
    casillas = set()
    for dcol, dfila in DIRECCION_POR_PASO:
        for distancia in range(1, alcance_max + 1):
            casilla = (col + dcol * distancia, fila + dfila * distancia)
            if not mapa.esta_dentro(*casilla) or mapa.hay_pared(*casilla):
                break
            if distancia >= alcance_min:
                casillas.add(casilla)
            if casilla in ocupadas:
                break
    return casillas
def tirar_ataque(punteria):
    return random.randint(1, 100) <= punteria

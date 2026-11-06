#utilizo tile como objeto, aca calculo su posicion y la dibujo tambien
import random
import pygame
from config import TILE_ALTO, TILE_ANCHO, COLOR_BORDE, COLOR_TILE
from src.tablero.isometria import grilla_a_pantalla
from src.graficos.recursos import cargar_imagen
#Dibuja UN solo tile

VARIANTES = ["tiles/piso_pasto_1.png", "tiles/piso_pasto_2.png",
             "tiles/piso_pasto_3.png", "tiles/piso_pasto_seco.png"]
PESOS = [3, 3, 3, 1]
_capas = {}

def capa_de_color(color):
    if color not in _capas:
        capa = pygame.Surface((TILE_ANCHO, TILE_ALTO), pygame.SRCALPHA)
        medio_ancho, medio_alto = TILE_ANCHO // 2, TILE_ALTO // 2
        puntos = [(medio_ancho, 0), (TILE_ANCHO, medio_alto), (medio_ancho, TILE_ALTO), (0, medio_alto)]
        pygame.draw.polygon(capa, color + (130,), puntos)
        _capas[color] = capa
    return _capas[color]

class Tile:
    def __init__(self, col, fila):
        self.col = col
        self.fila = fila
        self.color = COLOR_TILE
        # Los puntos del rombo se calculan una sola vez, no en cada cuadro.
        self.puntos = self._calcular_puntos() 
        sorteo = random.Random(col * 1000 + fila)
        self.imagen = cargar_imagen(sorteo.choices(VARIANTES, PESOS)[0])           

    #calculo los puntos de la grilla a pixeles en la pantalla
    def _calcular_puntos(self):
        x, y = grilla_a_pantalla(self.col, self.fila)
        return [(x,y), 
                (x + TILE_ANCHO // 2, y + TILE_ALTO // 2),
                (x, y + TILE_ALTO),
                (x - TILE_ANCHO // 2, y + TILE_ALTO // 2)]

    def dibujar_tile(self, pantalla, color = None):
        x, y = self.puntos[0]
        esquina = (x - TILE_ANCHO //2, y)
        if self.imagen is None:
            pygame.draw.polygon(pantalla, color or self.color, self.puntos)
            pygame.draw.polygon(pantalla, color or COLOR_BORDE, self.puntos, 1) #el 1 es el grosor de la linea
            return
        pantalla.blit(self.imagen, esquina)
        if color is not None:
            pantalla.blit(capa_de_color(color), esquina)
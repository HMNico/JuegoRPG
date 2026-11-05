#utilizo tile como objeto, aca calculo su posicion y la dibujo tambien
import pygame
from config import TILE_ALTO, TILE_ANCHO, COLOR_BORDE, COLOR_TILE
from src.isometria import grilla_a_pantalla
#Dibuja UN solo tile

class Tile:
    def __init__(self, col, fila):
        self.col = col
        self.fila = fila
        self.color = COLOR_TILE
        # Los puntos del rombo se calculan una sola vez, no en cada cuadro.
        self.puntos = self._calcular_puntos()    

    #calculo los puntos de la grilla a pixeles en la pantalla
    def _calcular_puntos(self):
        x, y = grilla_a_pantalla(self.col, self.fila)
        return [(x,y), 
                (x + TILE_ANCHO // 2, y + TILE_ALTO // 2),
                (x, y + TILE_ALTO),
                (x - TILE_ANCHO // 2, y + TILE_ALTO // 2)]

    def dibujar_tile(self, pantalla, color = None):
        pygame.draw.polygon(pantalla, color or self.color, self.puntos)
        pygame.draw.polygon(pantalla, color or COLOR_BORDE, self.puntos, 1) #el 1 es el grosor de la linea
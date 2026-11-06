import pygame
from config import (TILE_ANCHO, TILE_ALTO, ALTURA_PARED, COLOR_PARED_TECHO,
                    COLOR_PARED_IZQ, COLOR_PARED_DER, COLOR_PARED_BORDE)
from src.tablero.isometria import grilla_a_pantalla
from src.graficos.recursos import cargar_imagen

class Pared:
    def __init__(self, col, fila):
        self.col = col
        self.fila = fila
        self.imagen = cargar_imagen("tiles/pared.png")
        x, y = grilla_a_pantalla(col, fila)
        self.esquina = (x - TILE_ANCHO // 2, y - ALTURA_PARED)
        medio_ancho, medio_alto = TILE_ANCHO // 2, TILE_ALTO // 2
        # Las 4 esquinas del rombo en el piso (como en Tile)
        arriba = (x, y)
        derecha = (x + medio_ancho, y + medio_alto)
        abajo = (x, y + TILE_ALTO)
        izquierda = (x - medio_ancho, y + medio_alto)

        def subir(punto):
            return (punto[0], punto[1] - ALTURA_PARED)

        # Se dibujan en este orden: primero las caras y, al final, el techo encima
        self.caras = [
            ([izquierda, abajo, subir(abajo), subir(izquierda)], COLOR_PARED_IZQ),
            ([abajo, derecha, subir(derecha), subir(abajo)], COLOR_PARED_DER),
            ([subir(arriba), subir(derecha), subir(abajo), subir(izquierda)], COLOR_PARED_TECHO),
        ]

    def orden_de_dibujo(self):
        return (self.col + self.fila, True)

    def dibujar(self, pantalla, seleccionada=False):
        if self.imagen is not None:
            pantalla.blit(self.imagen, self.esquina)
            return        
        for puntos, color in self.caras:
            pygame.draw.polygon(pantalla, color, puntos)
            pygame.draw.polygon(pantalla, COLOR_PARED_BORDE, puntos, 1)
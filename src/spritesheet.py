"""Recorta una hoja de sprites (spritesheet) en cuadros individuales."""
import pygame
from config import FILAS_HOJA, PROPORCION_PIES, ESCALA_SPRITE
from src.recursos import cargar_imagen

_cache = {}


class HojaSprites:
    def __init__(self, imagen, columnas, filas, escala=1):
        ancho_cuadro = imagen.get_width() // columnas
        alto_cuadro = imagen.get_height() // filas
        self.pies= (int(ancho_cuadro / 2 * escala)), (int(alto_cuadro * PROPORCION_PIES * escala))
        
        self.filas = filas
        self.col= columnas
        # self.cuadros[fila][col] -> una imagen (Surface) por cuadro
        self.cuadros = []
        for f in range(filas):
            fila = []
            for c in range(columnas):
                rect = (c * ancho_cuadro, f * alto_cuadro, ancho_cuadro, alto_cuadro)
                cuadro = imagen.subsurface(rect)
                if escala != 1:
                    tamaño = (int(ancho_cuadro * escala), int(alto_cuadro * escala)) #lo parseo a int porque es una escala de 0.5
                    cuadro = pygame.transform.scale(cuadro, tamaño)
                fila.append(cuadro)
            self.cuadros.append(fila)
    def obtener(self, fila, col=0):
        """Devuelve el cuadro de la fila y columna indicadas."""
        return self.cuadros[fila][col]     


def cargar_hoja(nombre, columnas):
    """Carga y recorta una hoja una sola vez; las demás veces la reutiliza."""
    if nombre not in _cache:
        imagen = cargar_imagen(nombre) #cargo la HojaSprite entera
        _cache[nombre] = (HojaSprites(imagen, columnas, FILAS_HOJA, ESCALA_SPRITE)
                        if imagen else None) #Al crear una HojaSprite, la crea ya recortada.
    return _cache[nombre]    
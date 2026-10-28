"""Carga de imágenes desde disco, con caché para no cargarlas dos veces."""
import os
import pygame
from config import CARPETA_SPRITES

_cache = {}

#Me carga la imagen sin cortar
def cargar_imagen(nombre, alto=None, pixel_art=True):
    """Carga assets/sprites/<nombre>. Si se indica 'alto', la escala
    manteniendo la proporción. Devuelve None si el archivo no existe."""
    clave = (nombre, alto)
    if clave in _cache:
        return _cache[clave]

    ruta = os.path.join(CARPETA_SPRITES, nombre)
    if not os.path.exists(ruta):
        print(f"[AVISO] No se encontró el sprite: {ruta}")
        _cache[clave] = None
        return None

    imagen = pygame.image.load(ruta).convert_alpha()

    if alto is not None:
        ancho = round(imagen.get_width() * alto / imagen.get_height())
        if pixel_art:
            imagen = pygame.transform.scale(imagen, (ancho, alto))
        else:
            imagen = pygame.transform.smoothscale(imagen, (ancho, alto))

    _cache[clave] = imagen
    return imagen
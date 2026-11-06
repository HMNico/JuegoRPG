import pygame
from config import (COLOR_BOTON, COLOR_BOTON_HOVER, COLOR_BOTON_DESHABILITADO, COLOR_BORDE_BOTON, COLOR_TEXTO, COLOR_TEXTO_DESHABILITADO)
from src.audio import sonido

class Boton:
    def __init__(self, texto, centro, accion, ancho=240, alto=50):
        self.texto = texto
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = centro
        self.accion = accion            # la FUNCIÓN que se ejecuta al hacer clic
        self.habilitado = True

    def esta_encima(self, pos):
        return self.rect.collidepoint(pos)

    def manejar_evento(self, evento):
        if (self.habilitado and evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1 and self.esta_encima(evento.pos)):
            self.accion()
            sonido.efecto("boton")
            return True
        return False

    def dibujar(self, pantalla, fuente):
        if not self.habilitado:
            fondo, color_texto = COLOR_BOTON_DESHABILITADO, COLOR_TEXTO_DESHABILITADO
        elif self.esta_encima(pygame.mouse.get_pos()):
            fondo, color_texto = COLOR_BOTON_HOVER, COLOR_TEXTO
        else:
            fondo, color_texto = COLOR_BOTON, COLOR_TEXTO
        pygame.draw.rect(pantalla, fondo, self.rect, border_radius=8)
        pygame.draw.rect(pantalla, COLOR_BORDE_BOTON, self.rect, width=2, border_radius=8)
        imagen = fuente.render(self.texto, True, color_texto)
        pantalla.blit(imagen, imagen.get_rect(center=self.rect.center))    
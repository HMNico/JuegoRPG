import pygame
from config import ANCHO, COLOR_FONDO, COLOR_TEXTO, TITULO
from src.escenas.escena import Escena
from src.interfaz.boton import Boton

class MenuPrincipal(Escena):
    def __init__(self, juego):
        super().__init__(juego)
        self.fuente_titulo = pygame.font.SysFont(None, 90)
        self.fuente = pygame.font.SysFont(None, 36)
        centro_x = ANCHO // 2
        self.botones = [
            Boton("Jugar", (centro_x, 360), juego.nueva_partida),
            Boton("Opciones", (centro_x, 430), juego.abrir_opciones),
            Boton("Cómo jugar", (centro_x, 500), juego.abrir_controles),
            Boton("Salir", (centro_x, 570), juego.salir),
        ]

    def manejar_evento(self, evento):
        for boton in self.botones:
            if boton.manejar_evento(evento):
                break

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        titulo = self.fuente_titulo.render(TITULO, True, COLOR_TEXTO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 200)))
        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente)
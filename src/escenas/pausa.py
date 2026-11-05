import pygame
from config import ANCHO, ALTO, COLOR_TEXTO
from src.escenas.escena import Escena
from src.interfaz.boton import Boton

class Pausa(Escena):
    def __init__(self, juego, partida):
        super().__init__(juego)
        self.partida = partida                 # la partida en curso, para volver a ella
        self.fuente_titulo = pygame.font.SysFont(None, 80)
        self.fuente = pygame.font.SysFont(None, 36)
        self.sombra = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self.sombra.fill((0, 0, 0, 160))
        centro_x = ANCHO // 2
        self.botones = [
            Boton("Continuar", (centro_x, 330), self.continuar),
            Boton("Opciones", (centro_x, 400), juego.abrir_opciones),
            Boton("Menú principal", (centro_x, 470), juego.ir_al_menu),
        ]

    def continuar(self):
        self.juego.cambiar_escena(self.partida)

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.continuar()
            return
        for boton in self.botones:
            if boton.manejar_evento(evento):
                break

    def dibujar(self, pantalla):
        self.partida.dibujar(pantalla)
        pantalla.blit(self.sombra, (0, 0))
        titulo = self.fuente_titulo.render("PAUSA", True, COLOR_TEXTO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 220)))
        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente)
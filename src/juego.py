import pygame
from config import ANCHO, ALTO, FPS, TITULO
from src.partida import Partida

class Juego:
    """Tiene la ventana y el bucle principal. Le pasa todo a la escena actual."""
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.escena = Partida(self)

    def cambiar_escena(self, escena):
        self.escena = escena

    def salir(self):
        self.corriendo = False

    def ejecutar(self):
        while self.corriendo:
            tiempo = self.reloj.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                else:
                    self.escena.manejar_evento(evento)
            self.escena.actualizar(tiempo)
            self.escena.dibujar(self.pantalla)
            pygame.display.flip()
        pygame.quit()
import pygame
from config import ANCHO, ALTO, FPS, TITULO
from src.escenas.partida import Partida
from src.escenas.menu import MenuPrincipal
from src.escenas.fin_de_partida import FinDePartida
from src.escenas.pausa import Pausa
from src.escenas.opciones import Opciones

class Juego:
    """Tiene la ventana y el bucle principal. Le pasa todo a la escena actual."""
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.escena = None
        self.ir_al_menu()
        self.volumenes = {"Música": 0.7, "Efectos": 0.7}
            

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

    def ir_al_menu(self):
        self.cambiar_escena(MenuPrincipal(self))

    def nueva_partida(self):
        self.cambiar_escena(Partida(self))

    def fin_de_partida(self, resultado, resumen):
        self.cambiar_escena(FinDePartida(self, resultado, resumen))

    def pausar(self, partida):
        self.cambiar_escena(Pausa(self, partida))

    def abrir_opciones(self):
        self.cambiar_escena(Opciones(self, self.escena))
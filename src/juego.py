import pygame
from config import ANCHO, ALTO, FPS, TITULO
from src.escenas.partida import Partida
from src.escenas.menu import MenuPrincipal
from src.escenas.fin_de_partida import FinDePartida
from src.escenas.pausa import Pausa
from src.escenas.opciones import Opciones
from src.audio import sonido

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
        self.volumenes = sonido.volumenes
        self.totales = {}
        sonido.iniciar()
            

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
        sonido.musica("musica_menu")
        self.cambiar_escena(MenuPrincipal(self))

    def nueva_partida(self, numero_nivel=1):
        sonido.detener_musica()
        if numero_nivel == 1:
            self.totales = {}
        self.cambiar_escena(Partida(self, numero_nivel))

    def fin_de_partida(self, resultado, resumen, numero_nivel):
        if resultado == "victoria":
            for clave, valor in resumen.items():
                self.totales[clave] = self.totales.get(clave, 0) + valor        
        self.cambiar_escena(FinDePartida(self, resultado, resumen, numero_nivel))

    def pausar(self, partida):
        self.cambiar_escena(Pausa(self, partida))

    def abrir_opciones(self):
        self.cambiar_escena(Opciones(self, self.escena))

import pygame
from config import ANCHO, COLOR_FONDO, COLOR_TEXTO, COLOR_VICTORIA, COLOR_DERROTA
from src.escenas.escena import Escena
from src.interfaz.boton import Boton

class FinDePartida(Escena):
    def __init__(self, juego, resultado, resumen):
        super().__init__(juego)
        self.resultado = resultado
        self.resumen = resumen
        self.fuente_titulo = pygame.font.SysFont(None, 100)
        self.fuente = pygame.font.SysFont(None, 36)
        centro_x = ANCHO // 2
        self.botones = [
            Boton("Reintentar", (centro_x, 500), juego.nueva_partida),
            Boton("Menú principal", (centro_x, 570), juego.ir_al_menu),
        ]

    def manejar_evento(self, evento):
        for boton in self.botones:
            if boton.manejar_evento(evento):
                break

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        if self.resultado == "victoria":
            texto, color = "VICTORIA", COLOR_VICTORIA
        else:
            texto, color = "DERROTA", COLOR_DERROTA
        titulo = self.fuente_titulo.render(texto, True, color)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 180)))

        for i, (nombre, valor) in enumerate(self.resumen.items()):
            linea = self.fuente.render(f"{nombre}: {valor}", True, COLOR_TEXTO)
            pantalla.blit(linea, linea.get_rect(center=(ANCHO // 2, 290 + i * 40)))

        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente)
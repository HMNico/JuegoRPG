import pygame
from config import ANCHO, COLOR_FONDO, COLOR_TEXTO, COLOR_VICTORIA, COLOR_DERROTA
from src.escenas.escena import Escena
from src.interfaz.boton import Boton
from src.tablero.nivel import existe_nivel
from src.audio import sonido

class FinDePartida(Escena):
    def __init__(self, juego, resultado, resumen, numero_nivel):
        super().__init__(juego)
        centro_x = ANCHO // 2
        self.resultado = resultado
        sonido.efecto("victoria" if resultado == "victoria" else "derrota")
        self.ultimo_nivel = resultado == "victoria" and not existe_nivel(numero_nivel + 1)
        if self.ultimo_nivel:
            self.resumen = juego.totales
            self.subtitulo = "Total de la partida"
        else:
            self.resumen = resumen
            self.subtitulo = None
        if resultado == "derrota":
            primero = Boton("Reintentar", (centro_x, 530), lambda: juego.nueva_partida(numero_nivel))
        elif self.ultimo_nivel:
            primero = Boton("Jugar de nuevo", (centro_x, 530), lambda: juego.nueva_partida(1))
        else:
            primero = Boton("Siguiente nivel", (centro_x, 530), lambda: juego.nueva_partida(numero_nivel + 1))
        self.botones = [primero, Boton("Menú Principal", (centro_x, 600), juego.ir_al_menu)]
        self.fuente_titulo = pygame.font.SysFont(None, 100)
        self.fuente_sub = pygame.font.SysFont(None, 50)
        self.fuente = pygame.font.SysFont(None, 36)

    def manejar_evento(self, evento):
        for boton in self.botones:
            if boton.manejar_evento(evento):
                break

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        if self.ultimo_nivel:
            texto, color = "Has ganado", COLOR_VICTORIA
        elif self.resultado == "victoria":
            texto, color = "VICTORIA", COLOR_VICTORIA
        else:
            texto, color = "DERROTA", COLOR_DERROTA
        titulo = self.fuente_titulo.render(texto, True, color)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 180)))
        if self.subtitulo:
            sub = self.fuente_sub.render(self.subtitulo, True, COLOR_TEXTO)
            pantalla.blit(sub, sub.get_rect(center=(ANCHO // 2, 245)))
        for i, (nombre, valor) in enumerate(self.resumen.items()):
            linea = self.fuente.render(f"{nombre}: {valor}", True, COLOR_TEXTO)
            pantalla.blit(linea, linea.get_rect(center=(ANCHO // 2, 290 + i * 40)))

        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente)
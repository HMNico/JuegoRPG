import pygame
from config import ANCHO, COLOR_FONDO, COLOR_TEXTO
from src.escenas.escena import Escena
from src.interfaz.boton import Boton
from src.audio import sonido

class Opciones(Escena):
    PASO = 0.1

    def __init__(self, juego, anterior):
        super().__init__(juego)
        self.anterior = anterior               # la escena a la que vuelve
        self.fuente_titulo = pygame.font.SysFont(None, 80)
        self.fuente = pygame.font.SysFont(None, 36)
        centro_x = ANCHO // 2
        self.filas = []
        self.botones = []
        self.botones_volumen = {}
        for i, nombre in enumerate(juego.volumenes):
            y = 300 + i * 80
            self.filas.append((nombre, y))
            menos = Boton("-", (centro_x + 80, y), lambda n=nombre: self.cambiar(n, -self.PASO), ancho=50)
            mas = Boton("+", (centro_x + 150, y), lambda n=nombre: self.cambiar(n, self.PASO), ancho=50)
            self.botones += [menos, mas]
            self.botones_volumen[nombre] = (menos, mas)
        self.botones.append(Boton("Volver", (centro_x, 520), self.volver))
        self.actualizar_botones()

    def cambiar(self, nombre, delta):
        sonido.cambiar_volumen(nombre, self.juego.volumenes[nombre] + delta)
        self.actualizar_botones()

    def actualizar_botones(self):
        for nombre, (menos, mas) in self.botones_volumen.items():
            volumen = self.juego.volumenes[nombre]
            menos.habilitado = volumen > 0
            mas.habilitado = volumen < 1

    def volver(self):
        self.juego.cambiar_escena(self.anterior)

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.volver()
            return
        for boton in self.botones:
            if boton.manejar_evento(evento):
                break

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        titulo = self.fuente_titulo.render("OPCIONES", True, COLOR_TEXTO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 180)))
        for nombre, y in self.filas:
            porcentaje = int(self.juego.volumenes[nombre] * 100)
            texto = self.fuente.render(f"{nombre}: {porcentaje}%", True, COLOR_TEXTO)
            pantalla.blit(texto, texto.get_rect(midright=(ANCHO // 2 + 30, y)))
        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente)
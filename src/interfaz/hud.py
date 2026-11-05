import pygame
from config import (ANCHO, ALTO, ALTO_PANEL, COLOR_PANEL, COLOR_BORDE_BOTON, COLOR_TEXTO,
                    COLOR_BARRA_VIDA, COLOR_BARRA_FONDO, DURACION_CARTEL)
from src.interfaz.boton import Boton
from src.unidades.aliado import Aliado

class HUD:
    def __init__(self, partida):
        self.partida = partida
        self.rect = pygame.Rect(0, ALTO - ALTO_PANEL, ANCHO, ALTO_PANEL)
        self.fuente = pygame.font.SysFont(None, 26)
        self.fuente_nombre = pygame.font.SysFont(None, 34)
        self.fuente_cartel = pygame.font.SysFont(None, 72)
        y = self.rect.centery
        self.boton_atacar = Boton("Atacar (A)", (590, y), lambda: partida.alternar_modo("atacar"), ancho=150)
        self.boton_especial = Boton("Especial (E)", (750, y), lambda: partida.alternar_modo("especial"), ancho=150)
        self.boton_terminar = Boton("Fin turno", (910, y), partida.terminar_turno_jugador, ancho=150)
        self.botones = [self.boton_atacar, self.boton_especial, self.boton_terminar]
        self.cartel = None
        self.tiempo_cartel = 0

    def contiene(self, pos):
        return self.rect.collidepoint(pos)

    def manejar_evento(self, evento):
        """Devuelve True si el evento era para el HUD (y entonces no tiene que llegar al mapa)."""
        for boton in self.botones:
            if boton.manejar_evento(evento):
                return True
        return evento.type == pygame.MOUSEBUTTONDOWN and self.contiene(evento.pos)

    def mostrar_cartel(self, texto):
        self.cartel = texto
        self.tiempo_cartel = DURACION_CARTEL

    def actualizar(self, tiempo):
        p = self.partida
        u = p.unidad_seleccionada
        puede_ordenar = p.turno == "jugador" and not p.hay_accion_en_curso() and isinstance(u, Aliado)
        self.boton_atacar.habilitado = puede_ordenar and u.puede_atacar()
        self.boton_especial.habilitado = puede_ordenar and u.puede_usar_especial()
        if isinstance(u, Aliado) and u.enfriamiento > 0:
            self.boton_especial.texto = f"Especial ({u.enfriamiento})"
        else:
            self.boton_especial.texto = "Especial (E)"
        self.boton_terminar.habilitado = p.turno == "jugador" and not p.hay_accion_en_curso()
        if self.tiempo_cartel > 0:
            self.tiempo_cartel -= tiempo

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_PANEL, self.rect)
        pygame.draw.line(pantalla, COLOR_BORDE_BOTON, self.rect.topleft, self.rect.topright, 2)
        self.dibujar_unidad(pantalla)
        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente)
        self.dibujar_cartel(pantalla)

    def dibujar_unidad(self, pantalla):
        u = self.partida.unidad_seleccionada
        x, y = self.rect.left + 20, self.rect.top + 15
        if u is None:
            pantalla.blit(self.fuente.render("Seleccioná una unidad", True, COLOR_TEXTO), (x, y))
            return
        pantalla.blit(self.fuente_nombre.render(u.nombre, True, COLOR_TEXTO), (x, y))

        barra = pygame.Rect(x, y + 34, 200, 16)
        lleno = barra.copy()
        lleno.width = int(barra.width * u.vida / u.vida_max)
        pygame.draw.rect(pantalla, COLOR_BARRA_FONDO, barra)
        pygame.draw.rect(pantalla, COLOR_BARRA_VIDA, lleno)
        pygame.draw.rect(pantalla, COLOR_BORDE_BOTON, barra, 1)
        vida = self.fuente.render(f"{u.vida}/{u.vida_max}", True, COLOR_TEXTO)
        pantalla.blit(vida, (barra.right + 10, barra.top - 1))

        especial = "listo" if u.enfriamiento == 0 else f"en {u.enfriamiento} turnos"
        lineas = [f"Movimiento: {u.movimiento_restante}/{u.movimiento}   Daño: {u.ataque}   Alcance: {u.alcance_min}-{u.alcance_max}",
                  f"Puntería: {u.punteria}%   Especial: {especial}"]
        for i, linea in enumerate(lineas):
            pantalla.blit(self.fuente.render(linea, True, COLOR_TEXTO), (x, y + 60 + i * 24))

    def dibujar_cartel(self, pantalla):
        if self.tiempo_cartel <= 0:
            return
        imagen = self.fuente_cartel.render(self.cartel, True, COLOR_TEXTO)
        imagen.set_alpha(min(255, int(255 * self.tiempo_cartel / 400)))
        pantalla.blit(imagen, imagen.get_rect(center=(ANCHO // 2, 60)))
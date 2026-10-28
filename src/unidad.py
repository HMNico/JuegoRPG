"""Una unidad del juego (soldado aliado o enemigo)."""
from typing import Self

import pygame
from config import (COLOR_ALIADO, COLOR_SOMBRA, DURACION_CUADRO, DURACION_PASO)
from src.isometria import grilla_a_pantalla, centro_de_casilla
from src.spritesheet import cargar_hoja
from src.direcciones import FILA_DIRECCION, DIRECCION_POR_PASO

RADIO = 12  # radio del círculo que se usa si no hay sprite


class Unidad:
    COOLDOWN_ATAQUE = 2
    def __init__(self, nombre, col, fila, vida_max, movimiento, ataque,
                 hojas=None):
        self.nombre = nombre
        self.col = col
        self.fila = fila
        self.vida_max = vida_max
        self.vida = vida_max
        self.ataque = ataque
        self.movimiento = movimiento

        # --- Turno ---
        self.movimiento_restante = movimiento
        self.ya_ataco = False
        self.enfriamiento = 0
        # --- Movimiento ---
        self.camino = []
        self.progreso = 0.0

        # --- Aspecto ---
        self.direccion = "SE"                              # hacia dónde mira (ver direcciones.py)
        self.accion = "quieto"                             # qué animación usa
        self.animaciones = {}                              # {"quieto": HojaSprites, ...}
        self.cuadro_actual = 0          # qué columna de la hoja se muestra
        self.tiempo_acumulado = 0                          # ms que lleva mostrándose ese cuadro
        if hojas:
            for accion, (archivo, columnas) in hojas.items():
                hoja = cargar_hoja(archivo, columnas)
                if hoja:
                    self.animaciones[accion] = hoja

    #Es el actualizar main. Para no llamar a todos los actualizar distintos
    def actualizar(self, tiempo):
        self.actualizar_movimiento(tiempo)
        self.actualizar_sprite(tiempo)

    def caminar(self, camino):
        self.camino = list(camino)
        self.movimiento_restante -= len(camino)
        if self.camino:
            self.mirar_hacia(self.camino[0])
            self.cambiar_accion("caminar")

    def esta_caminando(self):
        return len(self.camino) > 0

    def mirar_hacia(self, casilla):
        paso = (casilla[0] - self.col, casilla[1] - self.fila)
        self.direccion = DIRECCION_POR_PASO[paso]

    def actualizar_movimiento(self, tiempo):
        if not self.esta_caminando():
            return
        self.progreso += tiempo / DURACION_PASO #ESTA VIAJANDO A LA CASILLA
        while self.progreso >= 1 and self.esta_caminando(): #
            self.progreso -= 1
            self.col, self.fila = self.camino.pop(0)
            if self.esta_caminando():
                self.mirar_hacia(self.camino[0])
        if not self.esta_caminando():
            self.progreso= 0.0
            self.cambiar_accion("quieto")    



    def actualizar_sprite(self, tiempo):
        hoja = self.animaciones.get(self.accion)
        if hoja is None:
            return
        self.tiempo_acumulado += tiempo
        while self.tiempo_acumulado >=  DURACION_CUADRO:
            self.tiempo_acumulado -= DURACION_CUADRO
            self.cuadro_actual = (self.cuadro_actual + 1) % hoja.col

    def cambiar_accion(self, accion):
        """Cambia de animación y la empieza desde el primer cuadro."""
        if accion != self.accion:
            self.accion = accion
            self.cuadro_actual = 0
            self.tiempo_acumulado = 0

    # --- Turno funciones (reglas)---
    def iniciar_turno(self):
        self.movimiento_restante = self.movimiento
        self.ya_ataco = False
        if self.enfriamiento > 0:
            self.enfriamiento -= 1
    def puede_moverse(self):
        return self.movimiento_restante > 0 and not self.ya_ataco  #Si ya ataco, termina su turno y por ende, no puede moverse

    def puede_atacar(self):
        return not self.ya_ataco 
    def puede_actuar(self):
        return self.puede_moverse() or self.puede_atacar() #Puede hacer algo si puede moverse o si puede atacar
    def puede_usar_especial(self):
        return not self.puede_atacar() and self.enfriamiento == 0 #Puede usar especial si ya se reseteo el cooldown y no ataco normal



    def recibir_daño(self, cantidad):
        self.vida = max(0, self.vida - cantidad)
        self.cambiar_accion("hit" if self.esta_vivo() else "muerte")

    def esta_vivo(self):
        return self.vida > 0

    def centro_en_pantalla(self):
        """Píxel del centro del tile donde está parada la unidad."""
        x, y = centro_de_casilla(self.col, self.fila)
        if self.esta_caminando():
            x2, y2= centro_de_casilla(*self.camino[0])
            x = x + (x2 - x) * self.progreso
            y = y + (y2 - y) * self.progreso
        return int(x), int(y)

    def dibujar(self, pantalla, seleccionada=False):
        cx, cy = self.centro_en_pantalla()

        # 1) Anillo de selección (en el piso)
        if seleccionada:
            pygame.draw.ellipse(pantalla, self.COLOR_SELECCION, (cx - 22, cy - 11, 44, 22), 2)  

        # 2) Cuerpo
        hoja = self.animaciones.get(self.accion)
        if hoja:
            cuadro = hoja.obtener(FILA_DIRECCION[self.direccion], self.cuadro_actual)
            pies_x, pies_y = hoja.pies
            pantalla.blit(cuadro, (cx - pies_x,
                                   cy - pies_y))
        else:
            # Sin sprite: sombra + círculo, como antes
            pygame.draw.ellipse(pantalla, COLOR_SOMBRA, (cx - 12, cy - 5, 24, 10))
            cuerpo = (cx, cy - RADIO)
            pygame.draw.circle(pantalla, COLOR_ALIADO, cuerpo, RADIO)
            pygame.draw.circle(pantalla, (0, 0, 0), cuerpo, RADIO, width=1)
#Este archivo es el bucle principal
import pygame
from config import ANCHO, ALTO, FPS, TITULO, COLUMNAS, FILAS, COLOR_FONDO,  COLOR_TEXTO, COLOR_HOVER, COLOR_HOVER_ENEMIGO, COLOR_HOVER_ALIADO
from src import enemigo
from src.unidad import Unidad
from src.enemigo import Enemigo
from src.aliado import Aliado
from src.mapa import Mapa
from src.medico import Medico
from src.soldado import Soldado
from src.francotirador import Francotirador
from src.zombie import Zombie
from src.spitter import Spitter
from src.explosive import Explosive
from src.movimiento import *
from collections import deque




class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.fuente = pygame.font.SysFont(None, 26)
        self.mapa = Mapa(COLUMNAS, FILAS)
        self.tile_hover = None

        self.aliados = [
            Medico("Ana", 4, 12),
            Soldado("Bruno", 7, 10),       
            Francotirador("Pedro", 10, 12),]  
        self.enemigos = [
            Spitter("Spitter", 4, 2),
            Zombie("Zombie",7, 4),
            Explosive("Explosive", 10, 2),
            ]
        self.unidad_seleccionada = None
        self.unidad_en_movimiento = None           
        self.objetivo = None
        self.alcance = {}    

        # Turnos
        self.ronda = 1
        self.iniciar_turno("jugador")  
    def ejecutar(self):
        """Bucle principal: eventos → lógica → dibujo."""
        while self.corriendo:
            tiempo = self.reloj.tick(FPS)
            self.manejar_eventos()
            self.actualizar(tiempo)
            self.dibujar()
            
        pygame.quit()

    #eventos 
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.al_hacer_clic(*evento.pos)                
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.terminar_turno_jugador()

    def al_hacer_clic(self, x, y):
        if self.turno != "jugador":
            return
        if self.unidad_en_movimiento is not None:
            return
        tile = self.mapa.tile_en_pantalla(x, y)
        if tile is None:                      # clic fuera del mapa
            return
        casilla = (tile.col, tile.fila)
        unidad = self.unidad_en(*casilla) #Dame la unidad de la (x, y) que clickeo el mouse
        if unidad is not None: #Si no hay, quiere decir que esta clickeando en un lugar donde no hay aliado
            self.seleccionar(unidad)
            return
        if casilla in self.alcance:
            self.mover(self.unidad_seleccionada, casilla, self.alcance)
        #self.unidad_seleccionada = self.unidad_en(tile.col, tile.fila)

    def unidad_en(self, col, fila):
        """Devuelve la unidad parada en (col, fila), o None."""
        for unidad in self.aliados + self.enemigos:
            if unidad.col == col and unidad.fila == fila:
                return unidad
        return None

    def seleccionar(self, unidad):
        self.unidad_seleccionada = unidad
        self.actualizar_alcance()
        #self.alcance = self.calcular_alcance_unidad(unidad) if isinstance(unidad, Aliado) else {}

    def calcular_alcance_unidad(self, unidad):
        ocupadas = {(u.col, u.fila) for u in self.aliados + self.enemigos if u is not unidad} #devuelve una lista de par (x,y) de los pjs
        return calcular_alcance(self.mapa, (unidad.col, unidad.fila), unidad.movimiento_restante, ocupadas)

    def actualizar_alcance(self):
        """Recalcula el área azul de la unidad seleccionada (si corresponde)."""
        u = self.unidad_seleccionada
        if self.turno == "jugador" and isinstance(u, Aliado) and u.puede_moverse():
            self.alcance = self.calcular_alcance_unidad(u)
        else:
            self.alcance = {}
    # ---------- Turnos ----------
    def iniciar_turno(self, bando):
        self.turno = bando
        unidades = self.aliados if bando == "jugador" else self.enemigos
        for unidad in unidades:
            unidad.iniciar_turno()
            if bando == "enemigo":
                self.cola_enemigos = deque(e for e in self.enemigos if e.esta_vivo())

    def terminar_turno_jugador(self):
        if self.turno != "jugador" or self.unidad_en_movimiento is not None:
            return
        self.unidad_seleccionada = None
        self.alcance = {}
        self.iniciar_turno("enemigo")

    def jugar_turno_enemigo(self):
        if self.unidad_en_movimiento is not None:      # hay un enemigo caminando: esperar
            return
        if not self.cola_enemigos:                     # ya jugaron todos
            self.ronda += 1
            self.iniciar_turno("jugador")
            return
        enemigo = self.cola_enemigos.popleft()         # le toca al siguiente
        alcance = self.calcular_alcance_unidad(enemigo)
        destino = enemigo.elegir_destino(alcance, self.aliados)
        if destino is not None and destino != (enemigo.col, enemigo.fila):
            self.mover(enemigo, destino, alcance)        

    def mover(self, unidad : Unidad, destino, alcance):
        camino = reconstruir_camino(alcance, destino)
        unidad.caminar(camino)
        self.unidad_en_movimiento = unidad 
        self.alcance = {}

    def color_del_hover(self):
        if self.tile_hover is None:
            return COLOR_HOVER
        unidad = self.unidad_en(self.tile_hover.col, self.tile_hover.fila)
        if isinstance(unidad, Enemigo):
            return COLOR_HOVER_ENEMIGO
        elif isinstance(unidad, Aliado):
            return COLOR_HOVER_ALIADO
        return COLOR_HOVER


    #logica
    def actualizar(self, tiempo):
        for unidad in self.aliados + self.enemigos:
            unidad.actualizar(tiempo)
        u = self.unidad_en_movimiento
        if u is not None and not u.esta_caminando():
            self.unidad_en_movimiento = None
            self.actualizar_alcance()
        self.tile_hover = self.mapa.tile_en_pantalla(*pygame.mouse.get_pos())
        if self.turno == "enemigo":
            self.jugar_turno_enemigo()

    #dibujar
    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        self.mapa.dibujar(self.pantalla, self.tile_hover, self.color_del_hover(), self.alcance)
        self.dibujar_aliados()
        self.dibujar_enemigos()
        self.dibujar_info()
        self.dibujar_turno()    
        pygame.display.flip()

    def dibujar_aliados(self):
        for aliado in sorted(self.aliados, key=lambda u: u.col + u.fila):
            aliado.dibujar(self.pantalla, aliado is self.unidad_seleccionada)
    def dibujar_enemigos(self):
        for enemigo in sorted(self.enemigos, key=lambda u: u.col + u.fila):
            enemigo.dibujar(self.pantalla, enemigo is self.unidad_seleccionada)


    # info para el HUD
    def dibujar_info(self):
        u = self.unidad_seleccionada
        if u is None:
            return
        especial = "listo" if u.enfriamiento == 0 else f"en {u.enfriamiento} turnos"
        lineas = [u.nombre,
                  f"Vida: {u.vida}/{u.vida_max}",
                  f"Movimiento: {u.movimiento_restante}/{u.movimiento}",
                  f"Especial: {especial}",
                  f"Ataque: {u.ataque}",
                  f"Mira hacia: {u.direccion}"]
        for i, texto in enumerate(lineas):
            imagen = self.fuente.render(texto, True, COLOR_TEXTO)
            self.pantalla.blit(imagen, (20, 20 + i * 26))

    def dibujar_turno(self):
        texto = "TURNO DEL JUGADOR" if self.turno == "jugador" else "TURNO ENEMIGO"
        lineas = [f"{texto} - Ronda {self.ronda}", "Enter: terminar turno"]
        for i, linea in enumerate(lineas):
            imagen = self.fuente.render(linea, True, COLOR_TEXTO)
            self.pantalla.blit(imagen, (ANCHO - imagen.get_width() - 20, 20 + i * 26))
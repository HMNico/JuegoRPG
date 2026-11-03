#Este archivo es el bucle principal
import pygame
from config import ANCHO, ALTO, FPS, TITULO, COLUMNAS, FILAS, COLOR_FONDO,  COLOR_TEXTO, COLOR_HOVER, COLOR_HOVER_ENEMIGO, COLOR_HOVER_ALIADO, COLOR_DAÑO, COLOR_FALLO, COLOR_ZONA_ATAQUE, COLOR_ZONA_CURA, COLOR_CURA
from src.mapa import Mapa
from src.unidad import Unidad
from src.enemigo import Enemigo
from src.aliado import Aliado
from src.medico import Medico
from src.soldado import Soldado
from src.francotirador import Francotirador
from src.zombie import Zombie
from src.spitter import Spitter
from src.explosive import Explosive
from src.jefe import Jefe
from src.combate import casillas_atacables, tirar_ataque
from src.efectos import TextoFlotante, EfectoAnimado
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
        self.cola_enemigos = deque()

        #Ataque
        self.modo = "mover" #Modos: mover o atacar o especial
        self.atacables = set()
        self.direccion_previa = None #Donde miraba antes de entrar en modo ataque

        self.ataque_en_curso = None
        self.textos = []
        self.efectos = []
        self.enemigo_actual = None

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
                if evento.button == 1: #1 significa click izquierdo
                    self.al_hacer_clic(*evento.pos)
                elif evento.button == 3: #3 significa click derecho
                    self.cancelar_ataque()
                    self.alcance= {}
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    self.terminar_turno_jugador()
                elif evento.key == pygame.K_a:
                    self.alternar_modo("atacar")       
                elif evento.key == pygame.K_e:
                    self.alternar_modo("especial")

    def algun_aliado_puede_actuar(self):
        return any(a.puede_actuar() for a in self.aliados if a.esta_vivo())

    def al_hacer_clic(self, x, y):
        if self.modo == "atacar":
            if self.objetivo is not None:
                self.atacar(self.unidad_seleccionada, self.unidad_en(*self.objetivo))
            return
        if self.modo == "especial":
            if self.objetivo is not None:
                self.usar_especial(self.unidad_seleccionada, self.objetivo)
            return
        if self.turno != "jugador":
            return
        if self.hay_accion_en_curso():
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
            if unidad.esta_vivo() and unidad.col == col and unidad.fila == fila:
                return unidad
        return None

    def seleccionar(self, unidad):
        self.cancelar_ataque()
        self.unidad_seleccionada = unidad
        self.actualizar_alcance()
        #self.alcance = self.calcular_alcance_unidad(unidad) if isinstance(unidad, Aliado) else {}

    def calcular_alcance_unidad(self, unidad):
        ocupadas = self.casillas_ocupadas(excepto=unidad) | self.mapa.paredes
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
        if self.turno != "jugador" or self.hay_accion_en_curso():
            return
        self.cancelar_ataque()
        self.unidad_seleccionada = None
        self.alcance = {}
        self.iniciar_turno("enemigo")

    def jugar_turno_enemigo(self):
        if self.hay_accion_en_curso():      # hay un enemigo caminando o atacando: esperar
            return
        if self.enemigo_actual is not None:
            enemigo = self.enemigo_actual
            self.enemigo_actual = None
            a_tiro = self.aliados_a_tiro(enemigo, (enemigo.col, enemigo.fila))
            objetivo = enemigo.elegir_objetivo(a_tiro)
            if objetivo is not None:
                self.atacar(enemigo, objetivo)
            return

        if not self.cola_enemigos:                     # ya jugaron todos
            self.ronda += 1
            self.iniciar_turno("jugador")
            return
        
        enemigo = self.cola_enemigos.popleft()         # le toca al siguiente
        alcance = self.calcular_alcance_unidad(enemigo)
        casillas_de_ataque = {c for c in alcance if self.aliados_a_tiro(enemigo, c)}
        destino = enemigo.elegir_destino(alcance, self.aliados, casillas_de_ataque)

        if destino is not None and destino != (enemigo.col, enemigo.fila):
            self.mover(enemigo, destino, alcance)

        self.enemigo_actual = enemigo

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

    def casillas_ocupadas(self, excepto=None):
        return {(o.col, o.fila) for o in self.aliados + self.enemigos if o.esta_vivo() and o is not excepto}

    #Ataque
    def alternar_modo(self, modo):
        if self.modo == modo:
            self.cancelar_ataque()
            self.alcance = {}
            return
        self.cancelar_ataque() #si estoy en el otro modo, salgo primero de ese
        u = self.unidad_seleccionada
        if self.turno != "jugador" or self.hay_accion_en_curso():
            return
        if not isinstance(u,Aliado):
            return
        if modo == "atacar":
            if not u.puede_atacar():
                return
            ocupadas = self.casillas_ocupadas(excepto=u)
            self.atacables = casillas_atacables(self.mapa, (u.col, u.fila), u.alcance_min, u.alcance_max, ocupadas)
        else:
            if not u.puede_usar_especial():
                return
            ocupadas = self.casillas_ocupadas(excepto=u)
            zona = u.zona_especial(self.mapa, ocupadas)
            self.atacables = {c for c in zona if self.unidad_en(*c) is None or self.puede_apuntar_especial(u, c)}
            if not self.atacables:
                return
        self.modo = modo
        self.direccion_previa = u.direccion
        self.alcance = {}

    def cancelar_ataque(self):
        if self.modo == "mover":
            return
        self.unidad_seleccionada.direccion = self.direccion_previa
        self.modo = "mover"
        self.atacables = set()
        self.objetivo = None
        self.actualizar_alcance()

    def atacar(self, atacante, objetivo):
        acierto = tirar_ataque(atacante.punteria)
        atacante.iniciar_ataque(objetivo)
        self.ataque_en_curso = ("atacar", atacante, objetivo, acierto)
        #Se "sale del modo ataque", ya que realizo un ataque
        self.modo = "mover"
        self.atacables = set()
        self.objetivo = None
        self.alcance= {}

    def resolver_ataque(self):
        tipo, atacante, objetivo, acierto = self.ataque_en_curso
        if atacante.esta_atacando():
            return
        self.ataque_en_curso = None
        if tipo == "especial":
            self.resolver_especial(atacante, objetivo)
            self.actualizar_alcance()
            return
        x, y = objetivo.centro_en_pantalla()
        if acierto:
            objetivo.mirar_hacia((atacante.col, atacante.fila))
            objetivo.recibir_daño(atacante.ataque)
            self.textos.append(TextoFlotante(f"-{atacante.ataque}", COLOR_DAÑO, x, y - 70))
        else:
            self.textos.append(TextoFlotante("FALLÓ", COLOR_FALLO, x, y - 70))
        self.actualizar_alcance()
    def hay_accion_en_curso(self):
        return self.unidad_en_movimiento is not None or self.ataque_en_curso is not None

    def aliados_a_tiro(self, unidad, desde):
        ocupadas = self.casillas_ocupadas(excepto=unidad)
        zona = casillas_atacables(self.mapa, desde, unidad.alcance_min, unidad.alcance_max, ocupadas)
        return [a for a in self.aliados if a.esta_vivo() and (a.col, a.fila) in zona]

    def actualizar_objetivo(self):
        u = self.unidad_seleccionada
        self.objetivo = None
        if self.tile_hover is not None:
            casilla = (self.tile_hover.col, self.tile_hover.fila)
            if casilla in self.atacables and self.es_objetivo_valido(casilla):
                self.objetivo = casilla
        if self.objetivo is not None and self.objetivo != (u.col, u.fila):
            u.mirar_hacia(self.objetivo)
        else:
            u.direccion = self.direccion_previa

    def es_objetivo_valido(self, casilla):
        u = self.unidad_seleccionada
        if self.modo == "atacar":
            return isinstance(self.unidad_en(*casilla), Enemigo)
        return self.puede_apuntar_especial(u, casilla)

    def puede_apuntar_especial(self, u, casilla):
        if u.APUNTA_A_CASILLA:
            return True
        unidad = self.unidad_en(*casilla)
        return unidad is not None and u.es_objetivo_especial(unidad)

    def usar_especial(self, unidad, objetivo):
        unidad.iniciar_especial(objetivo)
        self.ataque_en_curso = ("especial", unidad, objetivo, True)
        self.modo = "mover"
        self.atacables = set()
        self.objetivo = None
        self.alcance = {}

    def resolver_especial(self,atacante, casilla_objetivo):
        for casilla in atacante.area_especial(casilla_objetivo):
            if not self. mapa.esta_dentro(*casilla):
                continue
            if atacante.EFECTO_ESPECIAL is not None:
                self.mostrar_efecto(atacante.EFECTO_ESPECIAL, casilla)
            unidad = self.unidad_en(*casilla)
            if unidad is not None:
                self.mostrar_resultado_especial(atacante.aplicar_especial(unidad), unidad)

    def mostrar_efecto(self, efecto, casilla):
        abajo, arriba, columnas = efecto
        self.efectos.append(EfectoAnimado(abajo, columnas, casilla, "debajo"))
        self.efectos.append(EfectoAnimado(arriba, columnas, casilla, "encima"))

    def mostrar_resultado_especial(self, resultado, objetivo):
        if resultado is None:
            return
        tipo, cantidad = resultado
        x, y = objetivo.centro_en_pantalla()
        if tipo == "curacion":
            self.mostrar_curacion(objetivo)
            self.textos.append(TextoFlotante(f"+{cantidad}", COLOR_CURA, x, y - 70))
        elif tipo == "daño":
            self.textos.append(TextoFlotante(f"-{cantidad}", COLOR_DAÑO, x, y -70))
        elif tipo == "fallo":
            self.textos.append(TextoFlotante(f"-{cantidad}", COLOR_FALLO, x, y -70))            
    #logica
    def actualizar(self, tiempo):
        for unidad in self.aliados + self.enemigos:
            unidad.actualizar(tiempo)
        u = self.unidad_en_movimiento
        if u is not None and not u.esta_caminando():
            self.unidad_en_movimiento = None
            self.actualizar_alcance()
        if self.ataque_en_curso is not None:
            self.resolver_ataque()
        for efecto in self.efectos:
            efecto.actualizar(tiempo)
        self.efectos = [e for e in self.efectos if not e.terminado()]
        for texto in self.textos:
            texto.actualizar(tiempo)
        self.textos = [t for t in self.textos if not t.terminado()]
        self.tile_hover = self.mapa.tile_en_pantalla(*pygame.mouse.get_pos())
        if self.turno == "enemigo":
            self.jugar_turno_enemigo()
        if (self.turno == "jugador" and not self.hay_accion_en_curso() and any(a.esta_vivo() for a in self.aliados) and not self.algun_aliado_puede_actuar()):
            self.terminar_turno_jugador()
        if self.modo != "mover":
            self.actualizar_objetivo()

    #dibujar
    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        color_zona = COLOR_ZONA_CURA if self.modo == "especial" else COLOR_ZONA_ATAQUE
        self.mapa.dibujar(self.pantalla, self.tile_hover, self.color_del_hover(), self.alcance, self.atacables, color_zona)
        self.dibujar_efectos("debajo")
        self.dibujar_unidades()
        self.dibujar_efectos("encima")
        for texto in self.textos:
            texto.dibujar(self.pantalla, self.fuente)
        self.dibujar_info()
        self.dibujar_turno()    
        pygame.display.flip()

    def dibujar_efectos(self, capa):
        for efecto in self.efectos:
            if efecto.capa == capa:
                efecto.dibujar(self.pantalla)

    def mostrar_curacion(self, unidad):
        casilla = (unidad.col, unidad.fila)
        self.efectos.append(EfectoAnimado("curar_efecto_abajo.png", 3, casilla, "debajo"))
        self.efectos.append(EfectoAnimado("curar_efecto_arriba.png", 3, casilla, "encima"))

    def dibujar_unidades(self):
        unidades = self.aliados + self.enemigos
        for unidad in sorted(unidades, key=lambda unidad: (unidad.esta_vivo(), unidad.col + unidad.fila)):
            unidad.dibujar(self.pantalla, unidad is self.unidad_seleccionada)


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
                  f"Mira hacia: {u.direccion}",
                  f"Daño: {u.ataque} Alcance: {u.alcance_min} - {u.alcance_max}",
                  f"Punteria: {u.punteria}%"]
        for i, texto in enumerate(lineas):
            imagen = self.fuente.render(texto, True, COLOR_TEXTO)
            self.pantalla.blit(imagen, (20, 20 + i * 26))

    def dibujar_turno(self):
        texto = "TURNO DEL JUGADOR" if self.turno == "jugador" else "TURNO ENEMIGO"
        lineas = [f"{texto} - Ronda {self.ronda}", "Enter: terminar turno", "A - Atacar E - Especial"]
        if self.objetivo is not None:
            u = self.unidad_seleccionada
            unidadObjetivo = self.unidad_en(*self.objetivo)
            if self.modo == "atacar":
                lineas.append(f"Atacar a {unidadObjetivo.nombre}: {u.punteria}% (daño {u.ataque})")
            elif unidadObjetivo is not None:
                lineas.append(f"Especial sobre {unidadObjetivo.nombre}")
            else:
                col, fila = self.objetivo
                lineas.append(f"Especial en la casilla: ({col}, {fila})")
        for i, linea in enumerate(lineas):
            imagen = self.fuente.render(linea, True, COLOR_TEXTO)
            self.pantalla.blit(imagen, (ANCHO - imagen.get_width() - 20, 20 + i * 26))
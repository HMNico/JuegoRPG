#Este archivo es el bucle principal
import pygame
from config import ANCHO, COLUMNAS, FILAS, COLOR_FONDO,  COLOR_TEXTO, COLOR_HOVER, COLOR_HOVER_ENEMIGO, COLOR_HOVER_ALIADO, COLOR_DAÑO, COLOR_FALLO, COLOR_ZONA_ATAQUE, COLOR_ZONA_CURA, COLOR_CURA, PAUSA_ENTRE_ENEMIGOS, PAUSA_ANTES_DE_ATACAR, PAUSA_FIN
from src.escenas.escena import Escena
from src.tablero.mapa import Mapa
from src.unidades.unidad import Unidad
from src.unidades.enemigo import Enemigo
from src.unidades.aliado import Aliado
from src.unidades.medico import Medico
from src.unidades.soldado import Soldado
from src.unidades.francotirador import Francotirador
from src.unidades.zombie import Zombie
from src.unidades.spitter import Spitter
from src.unidades.explosive import Explosive
from src.unidades.jefe import Jefe
from src.tablero.combate import casillas_atacables, tirar_ataque
from src.graficos.efectos import TextoFlotante, EfectoAnimado
from src.tablero.movimiento import *
from src.tablero.isometria import centro_de_casilla
from collections import deque
from src.interfaz.hud import HUD

class Partida(Escena):
    def __init__(self, juego):
        super().__init__(juego)
        self.pantalla = juego.pantalla
        self.fuente = pygame.font.SysFont(None, 26)
        self.mapa = Mapa(COLUMNAS, FILAS)
        self.tile_hover = None

        self.aliados = [
            Medico("Ana", 5, 12),
            Soldado("Bruno", 7, 10),       
            Francotirador("Pedro", 10, 12),]  
        self.enemigos = [
            #Spitter("Spitter", 4, 2),
            Spitter("Spitter", 5, 10),
            Zombie("Zombie",7, 4),
            Explosive("Explosive", 6, 8),
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
        self.paso_enemigo = None # "mover" o "atacar"
        self.espera = 0 

        #puntaje de las casillas (la utilizo para prioridad)
        self.fuente_chica = pygame.font.SysFont(None, 18)
        self.mostrar_puntaje = False
        # Turnos
        self.ronda = 1
        self.hud = HUD(self)
        self.iniciar_turno("jugador")  

        #Interfaz
        self.resultado= None
        self.espera_fin = 0

    #eventos 
    def manejar_evento(self, evento):
        if self.resultado is not None:
            return
        if self.hud.manejar_evento(evento):
            return        
        if evento.type == pygame.MOUSEBUTTONDOWN:
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
            elif evento.key == pygame.K_n:
                self.mostrar_puntaje = not self.mostrar_puntaje
            elif evento.key == pygame.K_ESCAPE:
                if self.modo != "mover":
                    self.cancelar_ataque()
                else:
                    self.juego.pausar(self)

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
        self.hud.mostrar_cartel("TU TURNO" if bando == "jugador" else "TURNO ENEMIGO")

    def terminar_turno_jugador(self):
        if self.turno != "jugador" or self.hay_accion_en_curso():
            return
        self.cancelar_ataque()
        self.unidad_seleccionada = None
        self.alcance = {}
        self.iniciar_turno("enemigo")

    def jugar_turno_enemigo(self, tiempo):
        if self.hay_accion_en_curso():      # hay un enemigo caminando o atacando: esperar
            return
        if self.espera>0:
            self.espera -= tiempo
            return
        
        # Elegir al siguiente enemigo (o devolver el turno)
        if self.enemigo_actual is None:
            if not self.cola_enemigos:
                self.unidad_seleccionada = None
                self.ronda += 1
                self.iniciar_turno("jugador")
                return
            self.enemigo_actual = self.cola_enemigos.popleft()
            self.unidad_seleccionada = self.enemigo_actual
            self.paso_enemigo = "mover"
            self.espera = PAUSA_ENTRE_ENEMIGOS
            return
        enemigo = self.enemigo_actual

        #moverse
        if self.paso_enemigo == "mover":
            alcance = self.calcular_alcance_unidad(enemigo)
            destino = enemigo.elegir_destino(alcance, self)
            if destino is not None and destino != (enemigo.col, enemigo.fila):
                self.mover(enemigo, destino, alcance)
            self.paso_enemigo = "atacar"
            self.espera = PAUSA_ANTES_DE_ATACAR
            return

        #atacar
        self.enemigo_actual = None
        casilla_especial = enemigo.elegir_especial(self)
        if casilla_especial is not None:
            self.usar_especial(enemigo, casilla_especial)
            return
        a_tiro = self.aliados_a_tiro(enemigo, (enemigo.col, enemigo.fila))
        objetivo = enemigo.elegir_objetivo(a_tiro)
        if objetivo is not None:
            self.atacar(enemigo, objetivo)

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
        if atacante.esta_atacando() and not atacante.llego_al_impacto():
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

    def amenazas_en(self, casilla, unidad): 
        ocupadas = self.casillas_ocupadas(excepto=unidad) | {casilla} #Las casillas de los vivos (menos la del enemigo a chequear), mas 
        return [a for a in self.aliados if a.esta_vivo() and casilla in casillas_atacables(self.mapa, (a.col, a.fila), a.alcance_min, a.alcance_max, ocupadas)]

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
        atacante.despues_del_especial()

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

    def comprobar_fin(self):
        if not any(e.esta_vivo() for e in self.enemigos):
            self.resultado = "victoria"
        elif not any(a.esta_vivo() for a in self.aliados):
            self.resultado = "derrota"
        if self.resultado is not None:
            self.espera_fin = PAUSA_FIN
            self.cancelar_ataque()
            self.unidad_seleccionada = None
            self.alcance = {}    

    def resumen(self):
        return {
            "Rondas jugadas": self.ronda,
            "Enemigos eliminados": sum(1 for e in self.enemigos if not e.esta_vivo()),
            "Aliados perdidos": sum(1 for a in self.aliados if not a.esta_vivo()),
        }  
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
        pos = pygame.mouse.get_pos()
        self.tile_hover = None if self.hud.contiene(pos) else self.mapa.tile_en_pantalla(*pos)
        self.hud.actualizar(tiempo)
        if self.resultado is None and not self.hay_accion_en_curso():
            self.comprobar_fin()
        if self.resultado is not None:
            self.espera_fin -= tiempo
            if self.espera_fin <= 0:
                self.juego.fin_de_partida(self.resultado, self.resumen())
            return
        if self.turno == "enemigo":
            self.jugar_turno_enemigo(tiempo)
        if (self.turno == "jugador" and not self.hay_accion_en_curso() and not self.algun_aliado_puede_actuar()):
            self.terminar_turno_jugador()
        if self.modo != "mover":
            self.actualizar_objetivo()

    #dibujar
    def dibujar(self, pantalla):
        self.pantalla.fill(COLOR_FONDO)
        color_zona = COLOR_ZONA_CURA if self.modo == "especial" else COLOR_ZONA_ATAQUE
        self.mapa.dibujar(self.pantalla, self.tile_hover, self.color_del_hover(), self.alcance, self.atacables, color_zona)
        self.dibujar_efectos("debajo")
        self.dibujar_unidades()
        self.dibujar_efectos("encima")
        if self.mostrar_puntaje and isinstance(self.unidad_seleccionada, Enemigo):
            self.dibujar_puntaje(self.unidad_seleccionada)
        for texto in self.textos:
            texto.dibujar(self.pantalla, self.fuente)
        self.dibujar_turno()
        self.hud.dibujar(self.pantalla)    

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

    def dibujar_puntaje(self, enemigo):
        vivos = [a for a in self.aliados if a.esta_vivo()]
        if not vivos:
            return
        ocupadas = self.casillas_ocupadas(excepto=enemigo) | self.mapa.paredes
        alcance = calcular_alcance(self.mapa, (enemigo.col, enemigo.fila), enemigo.movimiento, ocupadas)
        for casilla in alcance:
            nota = enemigo.puntuar_casilla(casilla, self, vivos)
            x, y = centro_de_casilla(*casilla)
            imagen = self.fuente_chica.render(str(nota), True, COLOR_TEXTO)
            self.pantalla.blit(imagen, (x - imagen.get_width() // 2, y - imagen.get_height() // 2))

    def dibujar_turno(self):
        texto = "Tu turno" if self.turno == "jugador" else "Turno enemigo"
        imagen = self.fuente.render(f"Ronda {self.ronda} - {texto}", True, COLOR_TEXTO)
        self.pantalla.blit(imagen, (ANCHO - imagen.get_width() - 20, 20))
        self.dibujar_info_objetivo()

    def dibujar_info_objetivo(self):
        if self.objetivo is None:
            return
        u = self.unidad_seleccionada
        if self.modo == "atacar":
            texto = f"{u.punteria}%  |  daño {u.ataque}"
        elif self.unidad_en(*self.objetivo) is not None:
            texto = "Usar especial"
        else:
            return
        x, y = centro_de_casilla(*self.objetivo)
        imagen = self.fuente.render(texto, True, COLOR_TEXTO)
        caja = imagen.get_rect(center=(x, y - 85)).inflate(12, 6)
        pygame.draw.rect(self.pantalla, (20, 20, 30), caja, border_radius=4)
        self.pantalla.blit(imagen, imagen.get_rect(center=caja.center))
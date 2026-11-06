import pygame
from config import ANCHO, COLOR_FONDO, COLOR_TEXTO, COLOR_SELECCION_ALIADO, COLOR_SELECCION_ENEMIGO
from src.escenas.escena import Escena
from src.interfaz.boton import Boton

CONTROLES = [
    ("Clic izquierdo", "Seleccionar, mover y atacar"),
    ("Clic derecho", "Cancelar el ataque o el especial"),
    ("A", "Modo ataque"),
    ("E", "Modo especial"),
    ("Enter", "Terminar el turno"),
    ("Esc", "Cancelar / Pausa"),
    ("N", "Ver cómo piensa un enemigo"),
]
ALIADOS = [
    ("Soldado", "Granada en área (3x3)"),
    ("Médico", "Cura 4 de vida"),
    ("Francotirador", "Disparo potente a distancia"),
]
ENEMIGOS = [
    ("Zombie", "Va por el más débil"),
    ("Spitter", "Escupe de lejos y se cubre"),
    ("Explosive", "Explota cerca de 2 o más aliados"),
    ("Jefe", "Smash en área; se enfurece"),
]

class Controles(Escena):
    def __init__(self, juego, anterior):
        super().__init__(juego)
        self.anterior = anterior
        self.fuente_titulo = pygame.font.SysFont(None, 70)
        self.fuente_seccion = pygame.font.SysFont(None, 34)
        self.fuente = pygame.font.SysFont(None, 26)
        self.botones = [Boton("Volver", (ANCHO // 2, 700), self.volver)]

    def volver(self):
        self.juego.cambiar_escena(self.anterior)

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.volver()
            return
        for boton in self.botones:
            if boton.manejar_evento(evento):
                break

    def dibujar_seccion(self, pantalla, titulo, filas, x, y, color_nombre):
        pantalla.blit(self.fuente_seccion.render(titulo, True, COLOR_TEXTO), (x, y))
        for i, (nombre, descripcion) in enumerate(filas):
            fila_y = y + 42 + i * 30
            pantalla.blit(self.fuente.render(nombre, True, color_nombre), (x, fila_y))
            pantalla.blit(self.fuente.render(descripcion, True, COLOR_TEXTO), (x + 160, fila_y))
        return y + 42 + len(filas) * 30

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        titulo = self.fuente_titulo.render("CÓMO JUGAR", True, COLOR_TEXTO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 70)))
        self.dibujar_seccion(pantalla, "Controles", CONTROLES, 60, 140, COLOR_SELECCION_ALIADO)
        fin = self.dibujar_seccion(pantalla, "Tus unidades", ALIADOS, 560, 140, COLOR_SELECCION_ALIADO)
        self.dibujar_seccion(pantalla, "Enemigos", ENEMIGOS, 560, fin + 30, COLOR_SELECCION_ENEMIGO)
        reglas = ["Cada unidad puede moverse y atacar una vez por turno. Atacar termina su turno.",
                  "Las paredes cortan el movimiento y la línea de tiro. Ganás al eliminar a todos los enemigos."]
        for i, linea in enumerate(reglas):
            imagen = self.fuente.render(linea, True, COLOR_TEXTO)
            pantalla.blit(imagen, imagen.get_rect(center=(ANCHO // 2, 560 + i * 32)))
        for boton in self.botones:
            boton.dibujar(pantalla, self.fuente_seccion)
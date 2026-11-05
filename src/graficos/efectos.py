from config import DURACION_CUADRO
from src.graficos.spritesheet import cargar_hoja
from src.tablero.isometria import centro_de_casilla

class EfectoAnimado:
    def __init__(self, archivo,columna, casilla, capa):
        self.hoja = cargar_hoja(archivo, columna, filas=1) #los sprites de los efectos de curacion tienen 1 sola fina
        self.casilla= casilla
        self.capa= capa #"debajo" o "encima" de las unidades
        self.cuadro_actual = 0
        self.tiempo_acumulado = 0
        self.termino = self.hoja is None

    def actualizar(self, tiempo):
        if self.termino:
            return
        self.tiempo_acumulado += tiempo
        while self.tiempo_acumulado >= DURACION_CUADRO:
            self.tiempo_acumulado -= DURACION_CUADRO
            if self.cuadro_actual + 1 < self.hoja.col:
                self.cuadro_actual += 1
            else:
                self.termino = True
                return
    def terminado(self):
        return self.termino
    def dibujar(self, pantalla):
        if self.termino:
            return
        cx, cy = centro_de_casilla(*self.casilla)
        cuadro = self.hoja.obtener(0, self.cuadro_actual)
        pies_x, pies_y = self.hoja.pies
        pantalla.blit(cuadro, (cx - pies_x, cy - pies_y))

class TextoFlotante:
    DURACION = 900       # ms que se ve
    VELOCIDAD = 0.04     # píxeles que sube por cada ms

    def __init__(self, texto, color, x, y):
        self.texto = texto
        self.color = color
        self.x = x
        self.y = y
        self.tiempo = 0

    def actualizar(self, tiempo):
        self.tiempo += tiempo
        self.y -= self.VELOCIDAD * tiempo

    def terminado(self):
        return self.tiempo >= self.DURACION

    def dibujar(self, pantalla, fuente):
        imagen = fuente.render(self.texto, True, self.color)
        pantalla.blit(imagen, (self.x - imagen.get_width() // 2, int(self.y)))
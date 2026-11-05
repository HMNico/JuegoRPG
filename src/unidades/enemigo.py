from src.unidad import Unidad
from config import COLOR_SELECCION_ENEMIGO
from src.movimiento import distancia


class Enemigo(Unidad):
    COLOR_SELECCION = COLOR_SELECCION_ENEMIGO
    #Variables que tienen peso a la hora de decidir
    PESO_ATAQUE = 100 
    PESO_DISTANCIA = 1
    PESO_VIDA = 2
    PESO_PELIGRO = 0
    def elegir_destino(self, alcance, partida):
        vivos = [a for a in partida.aliados if a.esta_vivo()]
        if not vivos:
            return None
        return max(alcance, key=lambda c: self.puntuar_casilla(c, partida, vivos))

    def puntuar_casilla(self, casilla, partida, vivos):
        puntaje = 0
        a_tiro = partida.aliados_a_tiro(self, casilla)
        if a_tiro:
            puntaje += max(self.puntuar_objetivo(a) for a in a_tiro)
        puntaje -= self.PESO_DISTANCIA * self.distancia_de_interes(casilla, vivos)
        if self.PESO_PELIGRO:
            puntaje -= self.PESO_PELIGRO * len(partida.amenazas_en(casilla, self))
        return puntaje
    
    def puntuar_objetivo(self, aliado):
        return self.PESO_ATAQUE - self.PESO_VIDA * aliado.vida
    
    def elegir_objetivo(self, aliados_a_tiro):
        if not aliados_a_tiro:
            return None
        return max(aliados_a_tiro, key=self.puntuar_objetivo)
    
    def distancia_de_interes(self, casilla, vivos): #Por defecto (si no se sobreescibe) va al aliado mas cerca
        return min(distancia(casilla, (a.col, a.fila)) for a in vivos)

    def elegir_especial(self, partida):
        return None
    
from src.unidad import Unidad
from config import COLOR_SELECCION_ENEMIGO
from src.movimiento import distancia


class Enemigo(Unidad):
    COLOR_SELECCION = COLOR_SELECCION_ENEMIGO
    def elegir_destino(self, alcance, aliados, casillas_de_ataque):
        if casillas_de_ataque:
            return min(casillas_de_ataque, key=lambda c: distancia(c, (self.col, self.fila)))
        vivos = [a for a in aliados if a.esta_vivo()]
        if not vivos:
            return None

        def distancia_al_mas_cercano(casilla):
            return min(distancia(casilla, (a.col, a.fila)) for a in vivos)

        return min(alcance, key=distancia_al_mas_cercano)

    def elegir_objetivo(self, aliados_a_tiro):
        if not aliados_a_tiro:
            return None
        return min(aliados_a_tiro, key=lambda a: a.vida)
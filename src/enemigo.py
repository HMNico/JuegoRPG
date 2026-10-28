from src.unidad import Unidad
from config import COLOR_SELECCION_ENEMIGO
from src.movimiento import distancia


class Enemigo(Unidad):
    COLOR_SELECCION = COLOR_SELECCION_ENEMIGO
    def elegir_destino(self, alcance, aliados):
        """De las casillas alcanzables, la que lo deja más cerca del aliado más cercano."""
        vivos = [a for a in aliados if a.esta_vivo()]
        if not vivos:
            return None

        def distancia_al_mas_cercano(casilla):
            return min(distancia(casilla, (a.col, a.fila)) for a in vivos)

        return min(alcance, key=distancia_al_mas_cercano)
    
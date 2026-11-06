from src.unidades.unidad import Unidad
from config import COLOR_SELECCION_ALIADO


class Aliado(Unidad):
    COLOR_SELECCION = COLOR_SELECCION_ALIADO
    SONIDO_ATAQUE = "disparo"
from src.aliado import Aliado
from src.movimiento import calcular_alcance


SPRITES_SOLDADO = {
    "quieto": ("soldado_idle.png", 4),
    "atacar": ("soldado_attack.png", 4), 
    "special":("soldado_grenade.png", 6),
    "caminar": ("soldado_walk.png", 4),
    "hit":("soldado_hit.png", 4),
    "muerte":("soldado_death.png", 7),
}

class Soldado(Aliado):
    COOLDOWN_ESPECIAL = 3
    APUNTA_A_CASILLA = True
    EFECTO_ESPECIAL = ("grenade_back.png","grenade_front.png", 8)
    DANO_ESPECIAL = 5
    LANZAMIENTO_MIN= 3
    LANZAMIENTO_MAX = 5
    def __init__(self, nombre, col, fila,):
        super().__init__(nombre, col, fila, vida_max= 14, movimiento= 3, ataque= 4, alcance_min=1, alcance_max=3, punteria= 80, hojas=SPRITES_SOLDADO)
    def zona_especial(self, mapa, ocupadas):
        origen = (self.col, self.fila)
        lejos = set(calcular_alcance(mapa, origen, self.LANZAMIENTO_MAX, mapa.paredes))
        cerca = set(calcular_alcance(mapa, origen, self.LANZAMIENTO_MIN - 1, mapa.paredes))
        return lejos - cerca
    def area_especial(self, casilla):
        col, fila = casilla
        area = set()
        for dcol in (-1, 0, 1):
            for dfila in (-1, 0, 1):
                area.add((col+dcol, fila+ dfila))
        return area
    def aplicar_especial(self, objetivo):
        objetivo.recibir_daño(self.DANO_ESPECIAL)
        return ("daño", self.DANO_ESPECIAL)
from src.unidades.aliado import Aliado
from src.tablero.movimiento import calcular_alcance

SPRITES_MEDIC = {
    "quieto": ("medic_idle.png", 4),
    "atacar": ("medic_attack.png", 4), 
    "caminar": ("medic_walk.png", 4),
    "hit":("medic_hit.png", 4),
    "muerte":("medic_death.png", 7),
    "special":("medic_heal.png", 6),
}

class Medico(Aliado):
    COOLDOWN_ESPECIAL = 2
    CURACION = 4
    ALCANCE_CURACION = 3
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max= 10, movimiento= 4, ataque= 2, alcance_min= 1,alcance_max= 3, punteria= 80, hojas=SPRITES_MEDIC)
    def zona_especial(self, mapa, ocupadas):
        return set(calcular_alcance(mapa, (self.col, self.fila), self.ALCANCE_CURACION, mapa.paredes))
    def es_objetivo_especial(self, unidad):
        return isinstance(unidad, Aliado) and unidad.esta_vivo()
    def aplicar_especial(self, objetivo):
        curado = objetivo.curar(self.CURACION)
        return ("curacion", curado)
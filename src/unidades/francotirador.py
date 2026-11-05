from src.aliado import Aliado
from src.enemigo import Enemigo
from src.combate import casillas_atacables, tirar_ataque

SPRITES_FRANCOTIRADOR = {
    "quieto": ("sniper_idle.png", 4),
    "atacar": ("sniper_attack.png", 4), 
    "special":("sniper_spattack.png", 6),
    "caminar": ("sniper_walk.png", 4),
    "hit":("sniper_hit.png", 4),
    "muerte":("sniper_death.png", 7),
}

class Francotirador(Aliado):
    COOLDOWN_ESPECIAL = 5
    DANO_ESPECIAL = 10
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=10, movimiento=3, ataque=7, alcance_min=5,alcance_max=6, punteria= 75, hojas=SPRITES_FRANCOTIRADOR)
    def zona_especial(self, mapa, ocupadas):
        return casillas_atacables(mapa, (self.col, self.fila), self.alcance_min, self.alcance_max, ocupadas)
    def es_objetivo_especial(self, unidad):
        return isinstance(unidad, Enemigo) and unidad.esta_vivo()
    def aplicar_especial(self, objetivo):
        if not tirar_ataque(self.punteria):
            return ("fallo", 0)
        objetivo.mirar_hacia((self.col, self.fila))
        objetivo.recibir_daño(self.DANO_ESPECIAL)
        return ("Daño", self.DANO_ESPECIAL)
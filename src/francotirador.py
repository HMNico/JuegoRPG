from src.aliado import Aliado

SPRITES_FRANCOTIRADOR = {
    "quieto": ("sniper_idle.png", 4),
    "disparo": ("sniper_attack.png", 4), 
    "special":("sniper_spattack.png", 6),
    "caminar": ("sniper_walk.png", 4),
    "hit":("sniper_hit.png", 4),
    "muerte":("sniper_death.png", 7),
}

class Francotirador(Aliado):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=8, movimiento=3, ataque=6, hojas=SPRITES_FRANCOTIRADOR)

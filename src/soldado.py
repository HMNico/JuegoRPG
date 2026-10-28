from src.aliado import Aliado

SPRITES_SOLDADO = {
    "quieto": ("soldado_idle.png", 4),
    "disparo": ("soldado_attack.png", 4), 
    "special":("soldado_grenade.png", 6),
    "caminar": ("soldado_walk.png", 4),
    "hit":("soldado_hit.png", 4),
    "muerte":("soldado_death.png", 7),
}

class Soldado(Aliado):
    def __init__(self, nombre, col, fila,):
        super().__init__(nombre, col, fila, vida_max= 12, movimiento= 3, ataque= 4, hojas=SPRITES_SOLDADO)
    
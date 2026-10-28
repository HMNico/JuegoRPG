from src.enemigo import Enemigo

SPRITES_JEFE = {
    "quieto": ("boss_idle.png", 4),
    "disparo": ("boss_attack.png", 4), 
    "special":("boss_spattack.png", 6),
    "caminar": ("boss_walk.png", 4),
    "hit":("boss_hit.png", 4),
    "muerte":("boss_death.png", 7),
}

class Jefe(Enemigo):
    def __init__(self, nombre, col, fila, vida_max, movimiento, ataque, hojas=None):
        super().__init__(nombre, col, fila, vida_max, movimiento, ataque, hojas)
        self.direccion  = "SO"

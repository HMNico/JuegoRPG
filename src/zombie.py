from src.enemigo import Enemigo

SPRITES_ZOMBIE = {
    "quieto": ("boss_idle.png", 4),
    "disparo": ("boss_attack.png", 4), 
    "special":("boss_attack.png", 6),
    "caminar": ("boss_walk.png", 4),
    "hit":("boss_hit.png", 4),
    "muerte":("boss_death.png", 7),
}

class Zombie(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=20, movimiento=4, ataque=3, hojas=SPRITES_ZOMBIE)
        self.direccion  = "SO"

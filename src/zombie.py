from src.enemigo import Enemigo

SPRITES_ZOMBIE = {
    "quieto": ("zombie_idle.png", 4),
    "atacar": ("zombie_attack.png", 5), 
    "caminar": ("zombie_walk.png", 4),
    "hit":("zombie_hit.png", 4),
    "muerte":("zombie_death.png", 7),
}

class Zombie(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=8, movimiento=4, ataque=3, alcance_min= 1, alcance_max= 1, punteria= 85, hojas=SPRITES_ZOMBIE)
        self.direccion  = "SO"

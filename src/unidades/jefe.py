from src.unidades.enemigo import Enemigo

SPRITES_JEFE = {
    "quieto": ("boss_idle.png", 4),
    "atacar": ("boss_attack.png", 5), 
    "special":("boss_spattack.png", 7),
    "caminar": ("boss_walk.png", 4),
    "hit":("boss_hit.png", 4),
    "muerte":("boss_death.png", 7),
}

class Jefe(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=40, movimiento=2, ataque=6, alcance_min=1, alcance_max=1, punteria= 85, hojas=SPRITES_JEFE)
        self.direccion  = "SO"

from src.enemigo import Enemigo

SPRITES_EXPLOSIVE = {
    "quieto": ("explosive_idle.png", 4),
    "disparo": ("explosive_attack.png", 4), 
    "special":("explosive_spattack.png", 6),
    "caminar": ("explosive_walk.png", 4),
    "hit":("explosive_hit.png", 4),
    "muerte":("explosive_death.png", 7),
}

class Explosive(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=20, movimiento=4, ataque=3, hojas=SPRITES_EXPLOSIVE)
        self.direccion  = "SO"

from src.enemigo import Enemigo

SPRITES_EXPLOSIVE = {
    "quieto": ("explosive_idle.png", 4),
    "atacar": ("explosive_attack.png", 5), 
    "special":("explosive_spattack.png", 6),
    "caminar": ("explosive_walk.png", 4),
    "hit":("explosive_hit.png", 4),
    "muerte":("explosive_death.png", 7),
}

class Explosive(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=10, movimiento=3, ataque=4, alcance_min=1, alcance_max=1, punteria= 80,hojas=SPRITES_EXPLOSIVE)
        self.direccion  = "SO"

from src.enemigo import Enemigo

SPRITES_SPITTER = {
    "quieto": ("spitter_idle.png", 4),
    "atacar": ("spitter_attack.png", 5), 
    "special":("spitter_spattack.png", 6),
    "caminar": ("spitter_walk.png", 4),
    "hit":("spitter_hit.png", 4),
    "muerte":("spitter_death.png", 7),
}

class Spitter(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=6, movimiento=3, ataque=3, alcance_min=3, alcance_max=4, punteria= 65, hojas=SPRITES_SPITTER)
        self.direccion  = "SO"

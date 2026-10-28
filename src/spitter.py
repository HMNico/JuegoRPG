from src.enemigo import Enemigo

SPRITES_SPITTER = {
    "quieto": ("spitter_idle.png", 4),
    "disparo": ("spitter_attack.png", 4), 
    "special":("spitter_spattack.png", 6),
    "caminar": ("spitter_walk.png", 4),
    "hit":("spitter_hit.png", 4),
    "muerte":("spitter_death.png", 7),
}

class Spitter(Enemigo):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=20, movimiento=4, ataque=3, hojas=SPRITES_SPITTER)
        self.direccion  = "SO"

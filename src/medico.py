from src.aliado import Aliado

SPRITES_MEDIC = {
    "quieto": ("medic_idle.png", 4),
    "disparo": ("medic_attack.png", 4), 
    "caminar": ("medic_walk.png", 4),
    "hit":("medic_hit.png", 4),
    "muerte":("medic_death.png", 7),
}

class Medico(Aliado):
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max= 10, movimiento= 4, ataque= 3, hojas=SPRITES_MEDIC)
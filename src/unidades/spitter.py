from src.unidades.enemigo import Enemigo
from src.unidades.medico import Medico

SPRITES_SPITTER = {
    "quieto": ("spitter_idle.png", 4),
    "atacar": ("spitter_attack.png", 5), 
    "special":("spitter_spattack.png", 6),
    "caminar": ("spitter_walk.png", 4),
    "hit":("spitter_hit.png", 4),
    "muerte":("spitter_death.png", 7),
}

class Spitter(Enemigo):
    PESO_PELIGRO = 30
    BONUS_Medico = 50
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=6, movimiento=3, ataque=3, alcance_min=3, alcance_max=4, punteria= 65, hojas=SPRITES_SPITTER)
        self.direccion  = "SO"

    def puntuar_objetivo(self, aliado):
        puntaje = super().puntuar_objetivo(aliado)
        if isinstance(aliado, Medico):
            puntaje += self.BONUS_Medico
        return puntaje

    def distancia_de_interes(self, casilla, vivos, juego):
        Medicos = [a for a in vivos if isinstance(a, Medico)]
        return super().distancia_de_interes(casilla, Medicos or vivos, juego)    
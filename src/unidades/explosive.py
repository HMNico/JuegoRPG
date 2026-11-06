from src.unidades.enemigo import Enemigo
from src.unidades.aliado import Aliado

SPRITES_EXPLOSIVE = {
    "quieto": ("explosive_idle.png", 4),
    "atacar": ("explosive_attack.png", 5), 
    "special":("explosive_spattack.png", 10),
    "caminar": ("explosive_walk.png", 4),
    "hit":("explosive_hit.png", 4),
    "muerte":("explosive_death.png", 7),
}

class Explosive(Enemigo):
    RADIO_EXPLOSION = 1
    DAÑO_EXPLOSION = 8
    PESO_GRUPO = 60
    VIDA_BAJA = 3
    CUADRO_IMPACTO = 6
    SONIDO_ESPECIAL = "explosion"
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=10, movimiento=3, ataque=4, alcance_min=1, alcance_max=1, punteria= 80,hojas=SPRITES_EXPLOSIVE)
        self.direccion  = "SO"


    def elegir_especial(self, juego):
        if not self.puede_usar_especial():
            return None
        vivos = [a for a in juego.aliados if a.esta_vivo()]
        cerca = self.aliados_en_area((self.col, self.fila), vivos)
        if len(cerca) >= 2 or (cerca and self.vida <= self.VIDA_BAJA):
            return (self.col, self.fila)
        return None

    def area_especial(self, casilla):
        col, fila = casilla
        r = self.RADIO_EXPLOSION
        return {(col + dcol, fila + dfila)
                for dcol in range(-r, r + 1)
                for dfila in range(-r, r + 1)}

    def aplicar_especial(self, objetivo):
        if not isinstance(objetivo, Aliado):
            return None
        objetivo.recibir_daño(self.DAÑO_EXPLOSION)
        return ("daño", self.DAÑO_EXPLOSION)

    def despues_del_especial(self):
        self.vida = 0
        self.desaparecer_al_terminar = True 
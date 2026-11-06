from src.unidades.enemigo import Enemigo
from src.unidades.aliado import Aliado


SPRITES_JEFE = {
    "quieto": ("boss_idle.png", 4),
    "atacar": ("boss_attack.png", 5), 
    "special":("boss_spattack.png", 7),
    "caminar": ("boss_walk.png", 4),
    "hit":("boss_hit.png", 4),
    "muerte":("boss_death.png", 7)
}
SPRITES_JEFE_ENRAGE = {
    "enrage": ("boss_enrage.png", 9),
    "quieto": ("boss_enrage_idle.png", 4),
    "atacar":  ("boss_enrage_attack.png", 5),
    "special": ("boss_enrage_spattack.png", 7),
    "caminar": ("boss_enrage_walk.png", 4),
    "hit": ("boss_enrage_hit.png", 4),
    "muerte": ("boss_enrage_death.png", 7)
}

class Jefe(Enemigo):
    COOLDOWN_ESPECIAL = 3
    DAÑO_SMASH = 7
    CUADRO_IMPACTO = 4
    PESO_GRUPO = 60
    SONIDO_ESPECIAL = "smash"
    def __init__(self, nombre, col, fila):
        super().__init__(nombre, col, fila, vida_max=25, movimiento=2, ataque=6, alcance_min=1, alcance_max=1, punteria= 85, hojas=SPRITES_JEFE)
        self.direccion  = "SO"
        self.enfurecido = False
        self.animaciones_furia = self.cargar_animaciones(SPRITES_JEFE_ENRAGE)

    def area_especial(self, casilla):
        col, fila = casilla
        return {(col + dcol, fila + dfila)
                for dcol in (-1, 0, 1)
                for dfila in (-1, 0, 1)}

    def elegir_especial(self, partida):
        if not self.puede_usar_especial():
            return None
        vivos = [a for a in partida.aliados if a.esta_vivo()]
        if len(self.aliados_en_area((self.col, self.fila), vivos)) >= 2:
            return (self.col, self.fila)
        return None

    def aplicar_especial(self, objetivo):
        if not isinstance(objetivo, Aliado):
            return None
        objetivo.mirar_hacia((self.col, self.fila))
        objetivo.recibir_daño(self.DAÑO_SMASH)
        return ("daño", self.DAÑO_SMASH)

    def recibir_daño(self, cantidad):
        super().recibir_daño(cantidad)
        if not self.enfurecido and self.esta_vivo() and self.vida <= self.vida_max // 2:
            self.enfurecer()

    def enfurecer(self):
        self.enfurecido = True
        self.movimiento += 1
        self.ataque += +1
        self.mensaje = "¡EL JEFE SE ENFURECE!"
        self.animaciones = self.animaciones_furia
        self.cambiar_accion("enrage")
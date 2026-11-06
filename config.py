# Constantes del juego


#Sobre la pantalla
#ANCHO, ALTO = 1280, 720
ANCHO, ALTO = 1024, 768
FPS = 60
TITULO = "Juego RPG"

#Tamaño de tiles
TILE_ANCHO = 64   # ancho del rombo isométrico
TILE_ALTO = 32    # alto (siempre la mitad del ancho)

#Colores
COLOR_FONDO = (20, 20, 30)
COLOR_TILE = (70, 110, 70)
COLOR_BORDE = (40, 60, 40)
COLOR_HOVER = (200, 200, 80)
COLOR_HOVER_ENEMIGO = (200, 60, 60)
COLOR_HOVER_ALIADO = (0, 128, 0)
COLOR_ALCANCE = (60, 110, 170)
COLOR_ALIADO = (70, 130, 220)
COLOR_SELECCION_ALIADO = (255, 230, 90)
COLOR_SELECCION_ENEMIGO = (255, 0, 0)
COLOR_SOMBRA = (30, 45, 30)
COLOR_TEXTO = (230, 230, 230)
COLOR_ZONA_ATAQUE = (110, 60, 60)
COLOR_ZONA_ESPECIAL = (160, 90, 210)
COLOR_CURA = (120, 255, 140)
COLOR_DAÑO = (255, 90, 90)
COLOR_FALLO = (200, 200, 200)
COLOR_AREA_IMPACTO = (230, 140, 40)

#Escenas
PAUSA_FIN = 1500 # ms entre el último golpe y la pantalla final
COLOR_VICTORIA = (120, 220, 120)
COLOR_DERROTA = (220, 80, 80)
COLOR_BOTON = (50, 70, 95)
COLOR_BOTON_HOVER = (80, 115, 150)
COLOR_BOTON_DESHABILITADO = (45, 45, 55)
COLOR_BORDE_BOTON = (200, 200, 215)
COLOR_TEXTO_DESHABILITADO = (120, 120, 130)

#HUD
ALTO_PANEL = 130
COLOR_PANEL = (28, 30, 42)
COLOR_BARRA_VIDA = (90, 200, 110)
COLOR_BARRA_FONDO = (70, 40, 45)
DURACION_CARTEL = 1200      # ms que se ve el cartel de turno

#Espera
PAUSA_ENTRE_ENEMIGOS = 400
PAUSA_ANTES_DE_ATACAR = 250
#Mapa
FILAS, COLUMNAS = 15, 15
ORIGEN_X, ORIGEN_Y = ANCHO // 2,  100  # dónde se dibuja la casilla (0,0)

#### SPRITES ####
import os
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_SPRITES = os.path.join(CARPETA_BASE, "assets", "sprites")
CARPETA_MAPAS = os.path.join(CARPETA_BASE, "assets", "mapas")
CARPETA_SONIDOS = os.path.join(CARPETA_BASE, "assets", "sonidos")
FILAS_HOJA = 4 #Las spritesheets tienen 4 filas todas (4 direcciones)
PROPORCION_PIES = 0.94 #los pies estan al 94% del alto del cuadro
ESCALA_SPRITE = 0.5          # se dibuja a la mitad de tamaño
DURACION_CUADRO = 120

#Paredes
ALTURA_PARED = 30
COLOR_PARED_TECHO = (150, 150, 160)
COLOR_PARED_IZQ = (105, 105, 118)
COLOR_PARED_DER = (80, 80, 92)
COLOR_PARED_BORDE = (50, 50, 60)

#Movimiento
DURACION_PASO = 300
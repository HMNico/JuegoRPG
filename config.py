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
#Mapa
FILAS, COLUMNAS = 15, 15
ORIGEN_X, ORIGEN_Y = ANCHO // 2,  100  # dónde se dibuja la casilla (0,0)

#### SPRITES ####
import os
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_SPRITES = os.path.join(CARPETA_BASE, "assets", "sprites")
FILAS_HOJA = 4 #Las spritesheets tienen 4 filas todas (4 direcciones)
PROPORCION_PIES = 0.94 #los pies estan al 94% del alto del cuadro
ESCALA_SPRITE = 0.5          # se dibuja a la mitad de tamaño
DURACION_CUADRO = 120

#Movimiento
DURACION_PASO = 300
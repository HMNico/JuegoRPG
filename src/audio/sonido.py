import os
import pygame
from config import CARPETA_SONIDOS

volumenes = {"Música": 0.7, "Efectos": 0.7}    # de 0.0 a 1.0
_efectos = {}                                    # caché: {"disparo": Sound, ...}
_activo = True                                   # False si la computadora no tiene audio

def iniciar():
    global _activo
    try:
        pygame.mixer.init()
    except pygame.error as error:
        print(f"[AVISO] Sin audio: {error}")
        _activo = False

def efecto(nombre):
    if not _activo:
        return
    if nombre not in _efectos:
        ruta = os.path.join(CARPETA_SONIDOS, f"{nombre}.wav")
        try:
            _efectos[nombre] = pygame.mixer.Sound(ruta)
        except (pygame.error, FileNotFoundError):
            print(f"[AVISO] No se encontró el sonido: {ruta}")
            _efectos[nombre] = None
    sonido = _efectos[nombre]
    if sonido is not None:
        sonido.set_volume(volumenes["Efectos"])
        sonido.play()

def musica(nombre):
    if not _activo:
        return
    ruta = os.path.join(CARPETA_SONIDOS, f"{nombre}.wav")
    try:
        pygame.mixer.music.load(ruta)
    except pygame.error:
        print(f"[AVISO] No se encontró la música: {ruta}")
        return
    pygame.mixer.music.set_volume(volumenes["Música"])
    pygame.mixer.music.play(loops=-1, fade_ms=800)

def cambiar_volumen(nombre, valor):
    volumenes[nombre] = round(min(1.0, max(0.0, valor)), 1)
    if nombre == "Música":
        aplicar_volumen_musica()

def detener_musica():
    if _activo:
        pygame.mixer.music.fadeout(600)

def aplicar_volumen_musica():
    if _activo:
        pygame.mixer.music.set_volume(volumenes["Música"])
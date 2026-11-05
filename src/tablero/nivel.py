import json
import os
from config import CARPETA_MAPAS
from src.tablero.mapa import Mapa
from src.unidades.aliado import Aliado
from src.unidades.medico import Medico
from src.unidades.soldado import Soldado
from src.unidades.francotirador import Francotirador
from src.unidades.zombie import Zombie
from src.unidades.spitter import Spitter
from src.unidades.explosive import Explosive
from src.unidades.jefe import Jefe

# Qué clase crear para cada letra del mapa
UNIDADES = {"M": Medico, "S": Soldado, "F": Francotirador,
            "z": Zombie, "s": Spitter, "e": Explosive, "J": Jefe}
NOMBRES = {"M": "Ana", "S": "Bruno", "F": "Pedro"}

def ruta_nivel(numero):
    return os.path.join(CARPETA_MAPAS, f"nivel{numero}.json")

def existe_nivel(numero):
    return os.path.exists(ruta_nivel(numero))

def cargar_nivel(numero):
    ruta = ruta_nivel(numero)
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    filas = datos["mapa"]
    ancho = len(filas[0])
    for i, linea in enumerate(filas):
        if len(linea) != ancho:
            raise ValueError(f"{ruta}: la fila {i} tiene {len(linea)} casillas y debería tener {ancho}")

    mapa = Mapa(ancho, len(filas))
    aliados, enemigos = [], []
    for fila, linea in enumerate(filas):
        for col, letra in enumerate(linea):
            if letra == "#":
                mapa.agregar_pared(col, fila)
            elif letra in UNIDADES:
                unidad = crear_unidad(letra, col, fila)
                if isinstance(unidad, Aliado):
                    aliados.append(unidad)
                else:
                    enemigos.append(unidad)
            elif letra != ".":
                raise ValueError(f"{ruta}: letra desconocida '{letra}' en la columna {col}, fila {fila}")
    refuerzos = datos.get("refuerzos", [])
    for r in refuerzos:
        if r["tipo"] not in UNIDADES:
            raise ValueError(f"{ruta}: Tipo de refuerzo desconocido '{r['tipo']}'")
    return datos["nombre"], mapa, aliados, enemigos, refuerzos

def crear_unidad(letra, col, fila):
    clase = UNIDADES[letra]
    return clase(NOMBRES.get(letra, clase.__name__), col, fila)
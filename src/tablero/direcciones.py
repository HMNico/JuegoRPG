# En qué fila de la hoja de sprites está cada dirección
FILA_DIRECCION = {
    "SE": 0,
    "SO": 1,
    "NE": 2,
    "NO": 3,      
}

# Hacia dónde mira en la pantalla según el paso en la grilla (dcol, dfila).
DIRECCION_POR_PASO = {
    (1, 0): "SE", (0, 1): "SO",   
    (-1, 0): "NO", (0, -1): "NE",
}

def signo(n):
    """1 si n es positivo, -1 si es negativo, 0 si es cero."""
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0
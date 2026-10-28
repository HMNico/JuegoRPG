# En qué fila de la hoja de sprites está cada dirección
FILA_DIRECCION = {
    "SE": 0,
    "SO": 1,
    "NO": 2,      
    "NE": 3,
}

# Hacia dónde mira en la pantalla según el paso en la grilla (dcol, dfila).
DIRECCION_POR_PASO = {
    (1, 0): "SE", (0, 1): "SO",   
    (-1, 0): "NO", (0, -1): "NE",
}

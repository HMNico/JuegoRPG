from config import TILE_ANCHO, TILE_ALTO, ORIGEN_X, ORIGEN_Y


#La conversion de una grilla normal(cuadrada) a una grilla isometrica(45 grados y achicada a la mitad el alto)
def grilla_a_pantalla(col, fila):
    """Convierte una casilla en la posición de la esquina superior del rombo."""
    x = (col - fila) * (TILE_ANCHO // 2) + ORIGEN_X
    y = (col + fila) * (TILE_ALTO // 2) + ORIGEN_Y
    return x, y

# Es el hover de la posicion del mouse
def pantalla_a_grilla(mx, my):
    """Convierte la posición del mouse en una casilla (col, fila)."""
    a = (mx - ORIGEN_X) / (TILE_ANCHO / 2)
    b = (my - ORIGEN_Y) / (TILE_ALTO / 2)
    return int((a + b) // 2), int((b - a) // 2)

#Necesito saber el centro de cualquier casilla, para el movimiento. Que sea de una casilla a otra, pero calculandolo desde el centro
def centro_de_casilla(col, fila):
    """Píxel del centro del rombo de la casilla (col, fila)."""
    x, y = grilla_a_pantalla(col, fila)
    return x, y + TILE_ALTO // 2
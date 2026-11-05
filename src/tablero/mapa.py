from src.tablero.tile import Tile
from src.tablero.isometria import pantalla_a_grilla
from config import COLOR_HOVER, COLOR_ALCANCE, COLOR_ZONA_ATAQUE


#Creo la Clase mapa, un mapa con x cantidad de objetos Tile
class Mapa:
    def __init__(self, columnas, filas):
        self.columnas = columnas
        self.filas = filas
        self.paredes = set()
        # Lista de listas: self.tiles[fila][col]. En self.tiles. tiles_fila es una fila del mapa. Al quedar ordenado, se vuelve matriz
        self.tiles = []
        for fila in range(filas):
            tiles_fila= []
            for col in range(columnas):
                tiles_fila.append(Tile(col, fila))
            self.tiles.append(tiles_fila)


    def esta_dentro(self, col, fila):
        """True si (col, fila) es una casilla válida del mapa."""
        return 0 <= col < self.columnas and 0 <= fila < self.filas

    def obtener_tile(self, col, fila):
        """Devuelve el Tile en (col, fila), o None si está fuera del mapa."""
        if self.esta_dentro(col, fila):
            return self.tiles[fila][col]
        return None
    
    def tile_en_pantalla(self, x, y):
        """Devuelve el Tile que está bajo el píxel (x, y), o None."""
        casillax,casillay = pantalla_a_grilla(x,y)
        return self.obtener_tile(casillax, casillay) 
    
    def dibujar(self, pantalla, tile_hover=None, color_hover= COLOR_HOVER, alcance=(), atacables=(), color_zona=COLOR_ZONA_ATAQUE):
        for fila in self.tiles:
            for tile in fila:
                if tile is tile_hover:
                    color = color_hover if tile is tile_hover else None
                elif (tile.col, tile.fila) in alcance:
                    color = COLOR_ALCANCE
                elif (tile.col, tile.fila) in atacables:
                    color = color_zona
                else:
                    color = None
                tile.dibujar_tile(pantalla, color)

    def hay_pared(self, col, fila):
        return (col, fila) in self.paredes
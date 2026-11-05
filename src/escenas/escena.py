class Escena:
    def __init__(self, juego):
        self.juego = juego  # para poder pedirle cosas: cambiar de escena, salir...

    def manejar_evento(self, evento):
        pass

    def actualizar(self, tiempo):
        pass

    def dibujar(self, pantalla):
        pass
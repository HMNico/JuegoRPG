Explicacion de los archivos mas importantes:

1- config.py: Son las constantes que utilizo en todo el proyecto

2- main.py: Simplemente ejecuta el juego. Mi idea era que haya el minimo codigo aqui

3- mapa.py: Creacion del mapa/grilla(como objeto propio) Esto facilita a la hora de la dinamica del juego (movimientos, seleccion, ataques, etc). Mapa, es una clase que crea un Mapa, con los tiles como objeto Tile, entonces tengo muchos objetos creados que puedo hacer lo que quiera.

4- tile.py: La clase tile. Simplemente facilita el codigo ya que modula todo
5- Spritesheet.py y recursos.py: dos archivos que se utilizan para la particion de los diferentes sprites

6- Todas las clases de los diferentes personajes: 

Primero esta unidad.py. De esta heredan todos, ya que tienen las funciones y atributos generales de todo personaje.
Segundo, aliado.py y enemigo.py. De estas heredan los dos bandos de personajes: Enemigo(explosive, spitter, zombie y jefe) y Aliado(soldado,medico,francotirador).
Por ultimo, los difernetes personajes.

Fases de creacion del proyecto
Roadmap que fui siguiendo (Recomendado por la IA)

1. Base	Entorno, estructura del proyecto, bucle del juego
2. Grilla isométrica: Dibujar el mapa, convertir pantalla ↔ casilla, hover	✅ Hecha
3. Unidades	Clase Unidad, selección con clic y más: herencia (Aliado/Enemigo y cada personaje), sprites, direcciones y animaciones✅ Hecha
4. Movimiento	Pathfinding (BFS/A*), alcance de movimiento	✅ Hecha
5. Sistema de turnos	Turno del jugador y del enemigo, puntos de acción	Pendiente
6. Combate	Ataque, probabilidad de acierto, cobertura (estilo XCOM) y habilidades de cada personaje	Pendiente
7. IA enemiga	Acercarse, atacar, cubrirse (decidir_turno)	Pendiente
8. Estados del juego	Menú, juego, victoria/derrota, cambio de nivel	Pendiente
9. Niveles	Mapas desde archivos, niveles 1 y 2	Pendiente
10. Jefe final	Jefe con habilidades y fases propias	Pendiente (la clase Jefe ya existe)
11. Arte y audio	Sprites, animaciones, música y efectos	🟡 Adelantada: ya tienes sprites y animaciones; faltan escenario y sonido
12. Pulido	Interfaz, balance, corrección de errores	Pendiente

# Tarea 2: DCCAMPO :school_satchel:

## Consideraciones generales :octocat:

El juego esta casi en su totalidad , solo falto lo de que los objetos en el suelo hágannos despawn, también se asumió que el 
Jugador parte en la mitad del mapa y no en una roca, y que él y tamaño maximo del mapa es de 14 de ancho y 29 de largo.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Ventana inicio: Hecha completa a prueba de error de input.
   
* Jugador: Movimiento completo y fluido con los 4 sprites, no atraviesa rocas y no se sale del mapa.

* Cultivos: Completo, crecen con el tiempo y cuando duerme tambien crecen.
   * Choclo: No hice que al recolectarlo siguiera estando la semilla , (lo de ser continuo)
   
* Herramienta: Funciones completas.
   
* Aparicion espontanea: Completa (pero no hice que no spawnearan donde esta el jugador)
* Recursos: Me faltó hacer que desaparezcan con el tiempo.
* Tienda y casa : Implementadas funcionan a la perfeccion.
* Inventario: funciona a la perfeccion el drag and drop
* Ventanas: 5 Ventanas , una del inicio , una del juego , una tienda, una de perder y una de ganar.(todas listas)
* "Trucos" : Hice que al apretar la tecla "O" se agregara dinero.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```ventanajuego.py``` en ```T02```
2. ```ventanatienda.py``` en ```T02```
3. ```character.py``` en ```T02```
4. ```ventanainicio.py``` en ```T02```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. PyQt5.QtWidgets (QWidget, QLabel, QLineEdit, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QProgressBar)
2.PyQt5.QtCore (pyqtSignal, Qt, QRect, QSize, QMetaObject, QTimer, QThread)
3.PyQt5.QtGui (QPixmap, QFont, QMovie, QBrush, QColor, QPalette, QIcon, QDrag)
4. os 
5. random

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Character.py```: Contiene a ```Character```, ```ClaseB```, (es el backend del personaje y sus movimientos)...
2. ```parametros_generales```: Contiene los valores modularizados

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. De la ayudantia de mario bros, para realizar la actualizacion del sprite del personaje.


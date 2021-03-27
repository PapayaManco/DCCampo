from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import QTest
from PyQt5.QtCore import  QRect
from parametros_generales import (VEL_MOVIMIENTO, N)

class Character(QObject):

    update_character_signal = pyqtSignal(str)
    tienda_signal = pyqtSignal()
    recoger_signal = pyqtSignal(str)
    casa_signal = pyqtSignal()
    
    def __init__(self, x, y):
        super().__init__()
        self.direction = 'D'
        self._x = x
        self._y = y
        self.initial_y = y
        self.tamano = []
        self.bloques_roca = []
        self.hitbox_character = QRect(self._x, self._y+10 , 15 , 10)
        self.pos_tienda = QRect(0,0,0,0)
        self.tienda = True
        self.casa = True
        self.pos_reco = []
        self.ubic_c = QRect(0,0,0,0)
        # Se inicializa nula la señal de actualizar la interfaz
        self.update_window_signal = None

        # Se conecta la señal de actualizar datos del personaje
        self.update_character_signal.connect(self.move)

    def update_window_character(self, position='stand'):
        if self.update_window_signal:
            self.update_window_signal.emit({
                'x': self.x,
                'y': self.y,
                'direction': self.direction,
                'position': position
            })

    def definir_espacio(self, data):
        self.tamano = data
    def lista_bloques_roca(self, bloques):
        self.bloques_roca=[]
        for bloque in bloques:
            self.bloques_roca.append(QRect(bloque.x(), bloque.y(), N , N))

    def ubic_tienda(self, tienda):
        self.pos_tienda = QRect(tienda[0].pos().x(), tienda[0].pos().y(), 2*N, 2*N)

    def entrar_tienda(self):
        if self.pos_tienda.intersects(self.hitbox_character) and self.tienda:
            self.tienda = False
            self.tienda_signal.emit()
        if not self.pos_tienda.intersects(self.hitbox_character) and not self.tienda:
            self.tienda = True

    def entrar_casa(self):
        if self.ubic_c.intersects(self.hitbox_character) and self.casa:
            self.casa = False
            self.casa_signal.emit()
        if not self.ubic_c.intersects(self.hitbox_character) and not self.casa:
            self.casa = True

    def colisiones(self):
        for i in self.bloques_roca:
            if i.intersects(self.hitbox_character):
                return False
        return True

    def ubic_recoger(self, lista_r):
        self.pos_reco = lista_r

    def ubic_casa(self, lista):
        self.ubic_c = QRect(lista[0].pos().x(), lista[0].pos().y(), 2*N, 2*N)

    def recoger(self):
        c=0
        for i in self.pos_reco:
            if self.hitbox_character.contains(i[0]+10,i[1]+10):
                self.borrar_recoger.emit(c)
                self.recoger_signal.emit(i[2])
            c += 1

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if 300 < value < 310 + (self.tamano[1]-1) * N and self.colisiones() :
            self.anterior = self.hitbox_character
            self._y_anterior = self._y
            self._y = value
            self.hitbox_character = QRect(self._x, self._y+15 , 16 , 15)
            if self.colisiones() == False:
                self._y = self._y_anterior
                self.hitbox_character = self.anterior
            else:
                self.update_window_character('walk')
            self.entrar_tienda()
            self.recoger()
            self.entrar_casa()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if 40 < value < 40 + (self.tamano[0] * N)-10 and self.colisiones():
            self.anterior = self.hitbox_character
            self._x_anterior = self._x
            self._x = value
            self.hitbox_character = QRect(self._x, self._y+15 , 16 , 15)
            if self.colisiones() == False:
                self._x = self._x_anterior
                self.hitbox_character = self.anterior
            else:
                self.update_window_character('walk')
            self.entrar_tienda()
            self.recoger()
            self.entrar_casa()

    def move(self, event):
        if event == 'R':
            self.direction = 'R'
            self.x += VEL_MOVIMIENTO
        elif event == 'L':
            self.direction = 'L'
            self.x -= VEL_MOVIMIENTO
        elif event == 'U':
            self.direction = 'U'
            self.y -= VEL_MOVIMIENTO
        elif event == 'D':
            self.direction = 'D'
            self.y += VEL_MOVIMIENTO

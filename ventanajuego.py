from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QProgressBar)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QMetaObject, QTimer, QThread)
from PyQt5.QtGui import (QPixmap, QFont, QMovie, QBrush, QColor, QPalette, QIcon, QDrag)
from character import Character
import os
import sys
from parametros_generales import (N, sprites_paths, objetos_paths, stages_alca, stages_choclo,
                                ENERGIA_JUGADOR, PROB_ARBOL, PROB_ORO)
import random

from parametros_plantas import TIEMPO_CHOCLOS , TIEMPO_ALCACHOFAS


class VentanaJuego(QWidget):
    update_window_signal = pyqtSignal(dict)
    agregar_dinero = pyqtSignal(int)
    tamano_signal = pyqtSignal(list)
    tienda_signal = pyqtSignal()
    clicked = pyqtSignal()
    listas_signal = pyqtSignal(list)
    arar_signal =pyqtSignal(list)
    aparecer_signal = pyqtSignal(list)
    chop_signal = pyqtSignal(list)
    cosechar_signal = pyqtSignal(list)
    recoger_signal = pyqtSignal(str)
    borrar_recoger = pyqtSignal(int)
    casa_signal = pyqtSignal()
    ganar_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def f_timer(self):
        self.timer0 = QTimer(self)
        self.timer0.setInterval(1000)
        self.timer0.start()
        self.timer0.timeout.connect(self.actualizar_tiempo)
    def init_gui(self):
        self.pastos = {
            1: "sprites/mapa/tile000.png",
            2: "sprites/mapa/tile001.png",
            3: "sprites/mapa/tile002.png",
            4: "sprites/mapa/tile006.png",
        }

        #se crea personaje
        self.backend_character = Character(420, 470)
        self._frame = 1
        # Se definen los otros atributos internos de la instancia
        self.front_character = None
        self.current_sprite = None
        self.update_character_signal = None

        self.setGeometry(300, 150, 1150, 750)
        self.setWindowTitle('DCCampo     Also try Initial P!')

        icon = QIcon()
        icon.addPixmap(QPixmap("sprites/otros/fish.png"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        palette = QPalette()
        brush = QBrush(QColor(101, 136, 93))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        self.setPalette(palette)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        self.setPalette(palette)

        self.fondo_juego = QLabel(self)
        self.fondo_juego.setGeometry(QRect(20, 290, 841, 451))
        self.fondo_juego.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.fondo_juego.setLayoutDirection(Qt.LeftToRight)
        self.fondo_juego.setPixmap(QPixmap("sprites/otros/window_template.jpg"))
        self.fondo_juego.setScaledContents(True)

        self.box_base = []
        self.lista_bloques=[]
        self.lista_over=[]
        #crear grilla base y grillas de bloques y drops
        pos_x = 40
        pos_y = 310
        #max_y=690 max_x=830
        for y in range(0,15):#Veces que N cabe en la distancia de Y
            for x in range(0,30): #veces que N cabe en la distancia de x
                self.bloque_base = QLabel("",self)
                self.bloque_base.setGeometry(QRect(pos_x, pos_y, N, N))
                self.box_base.append(QRect(pos_x, pos_y, N, N))

                num=random.randint(1,10)
                if 1<= num <=7:
                    self.bloque_base.setPixmap(QPixmap(self.pastos[4]))
                elif num == 8:
                    self.bloque_base.setPixmap(QPixmap(self.pastos[2]))
                elif num == 9:
                    self.bloque_base.setPixmap(QPixmap(self.pastos[3]))
                elif num == 10:
                    self.bloque_base.setPixmap(QPixmap(self.pastos[1]))
                self.bloque_base.setScaledContents(True)

                bloque = QLabel("",self)
                bloque.setGeometry(QRect(pos_x, pos_y, N, N))
                bloque.setScaledContents(True)
                self.lista_bloques.append(bloque)
                bloque = QLabel("",self)
                bloque.setGeometry(QRect(pos_x, pos_y, N, N))
                bloque.setScaledContents(True)
                self.lista_over.append(bloque)
                pos_x += N
            pos_x = 40
            pos_y += N

        self.inventario = QLabel(self)
        self.inventario.setEnabled(True)
        self.inventario.setGeometry(QRect(20, 60, 771, 221))
        self.inventario.setPixmap(QPixmap("sprites/otros/invetary_template.jpg"))
        self.inventario.setScaledContents(True)

        self.fondo_titulo_inv = QLabel(self)
        self.fondo_titulo_inv.setGeometry(QRect(20, 10, 311, 41))
        self.fondo_titulo_inv.setPixmap(QPixmap("sprites/otros/window_template.jpg"))
        self.fondo_titulo_inv.setScaledContents(True)

        self.titulo_inventario = QLabel(self)
        self.titulo_inventario.setGeometry(QRect(110, 10, 141, 41))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.titulo_inventario.setText("INVENTARIO")
        self.titulo_inventario.setFont(font)

        self.fondo_stats = QLabel(self)
        self.fondo_stats.setGeometry(QRect(906, 22, 221, 671))
        self.fondo_stats.setPixmap(QPixmap("sprites/otros/window_template.jpg"))
        self.fondo_stats.setScaledContents(True)

        self.l_stats = QLabel(self)
        self.l_stats.setGeometry(QRect(980, 70, 101, 41))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.l_stats.setText("STATS")
        self.l_stats.setFont(font)

        self.l_dia = QLabel(self)
        self.l_dia.setGeometry(QRect(920, 170, 71, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.dia = 0
        self.l_dia.setText("Dia: 0")
        self.l_dia.setFont(font)

        self.l_hora = QLabel(self)
        self.l_hora.setGeometry(QRect(920, 240, 150, 58))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.tiempo = [00,00]
        self.l_hora.setText("Hora: 00:00")
        self.l_hora.setFont(font)

        self.l_dinero = QLabel(self)
        self.l_dinero.setGeometry(QRect(920, 310, 250, 31))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_dinero.setText("Dinero:$0")
        self.l_dinero.setFont(font)

        self.barra_energia = QProgressBar(self)
        self.barra_energia.setGeometry(QRect(920, 440, 131, 31))
        self.barra_energia.setProperty("value", ENERGIA_JUGADOR)
        self.barra_energia.setTextVisible(True)
        self.barra_energia.setOrientation(Qt.Horizontal)

        self.l_energia = QLabel(self)
        self.l_energia.setGeometry(QRect(920, 390, 111, 41))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_energia.setText("Energia:")
        self.l_energia.setFont(font)

        self.boton_pausa = QPushButton(self)
        self.boton_pausa.setGeometry(QRect(970, 520, 81, 41))
        font = QFont()
        font.setPointSize(10)
        self.boton_pausa.setText("Pausar")
        self.boton_pausa.setFont(font)
        self.pausa = False
        self.boton_pausa.clicked.connect(self.pausar)

        self.boton_salir = QPushButton(self)
        self.boton_salir.setGeometry(QRect(970, 590, 81, 41))
        font = QFont()
        font.setPointSize(10)
        self.boton_salir.setText("Salir")
        self.boton_salir.setFont(font)
        self.boton_salir.clicked.connect(self.salir)

        self.fondo_stats.raise_()
        self.inventario.raise_()
        self.fondo_titulo_inv.raise_()
        self.titulo_inventario.raise_()
        self.l_stats.raise_()
        self.l_dia.raise_()
        self.l_hora.raise_()
        self.l_dinero.raise_()
        self.barra_energia.raise_()
        self.l_energia.raise_()
        self.boton_pausa.raise_()
        self.boton_salir.raise_()

        self.front_character = QLabel(self)
        self.current_sprite = QPixmap(sprites_paths[('walk', 'D', 1)])
        self.front_character.setPixmap(self.current_sprite)
        self.front_character.move(420, 470)

        self.init_signals()

        self.removido_temporal = []
        self.bloques_roca = []
        self.cultivo_box = []
        self.tienda = []
        self.grilla_inventario = []
        self.box_inv = []
        self.pasto_box = []
        self.recolectables = []
        self.casa = []
        pos_x = 60
        pos_y = 100
        for fila in range(1,4):
            for columna in range(1,13):
                slot_inv = QLabel("",self)
                slot_inv.setGeometry(QRect(pos_x, pos_y, 46, 42))
                self.box_inv.append(QRect(pos_x, pos_y, 46, 42))
                self.grilla_inventario.append(slot_inv)
                pos_x += 58
            pos_x = 60
            pos_y += 54
        self.plantas = []

    def crear_mapa(self, mapa):
        self.backend_character.definir_espacio([len(mapa[0]), len(mapa)])
        contador_b = 0
        c_H = 0
        c_T = 0
        for linea in mapa:
            for bloque in linea:
                if bloque == "O":
                    self.pasto_box.append(QRect(self.lista_bloques[contador_b].x(),
                        self.lista_bloques[contador_b].y(), N, N))
                elif bloque == "C" :
                    self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/tile003.png"))
                    self.cultivo_box.append(QRect(self.lista_bloques[contador_b].x(),
                        self.lista_bloques[contador_b].y(), N, N))
                elif bloque == "R":
                    self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/tile000.png"))
                    self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/tile087.png"))
                    self.lista_bloques[contador_b].raise_()
                    self.bloques_roca.append(self.lista_bloques[contador_b])
                    self.lista_over[contador_b] = self.lista_bloques[contador_b]
                elif bloque == "H" and c_H == 0:
                    self.lista_bloques[contador_b].resize(2*N, 2*N)
                    self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/house.png"))
                    self.lista_bloques[contador_b].raise_()
                    self.casa.append(self.lista_bloques[contador_b])
                    c_H += 1
                elif bloque == "T" and c_T == 0:
                    self.lista_bloques[contador_b].resize(2*N, 2*N)
                    self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/store.png"))
                    self.lista_bloques[contador_b].raise_()
                    self.tienda.append(self.lista_bloques[contador_b])
                    c_T += 1
                contador_b += 1
            if (len(mapa[0])) < 29:
                self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/tile087.png"))
                self.lista_bloques[contador_b].raise_()
            contador_b += 30-len(linea)
        #lleno de rocas lo del mapa que no es parte del mapeado eje X
        if len(mapa) < 15:
            for ultima in range(len(mapa[0])+1):
                self.lista_bloques[contador_b].setPixmap(QPixmap("sprites/mapa/tile087.png"))
                self.lista_bloques[contador_b].raise_()
                contador_b += 1
        self.front_character.raise_()
        self.backend_character.lista_bloques_roca(self.bloques_roca)
        self.backend_character.ubic_tienda(self.tienda)
        self.backend_character.ubic_casa(self.casa)
    def act_inventario(self, lista_inventario):
        self.lista_inventario = lista_inventario
        for i in range(0,36):
            self.grilla_inventario[i].setPixmap(QPixmap(objetos_paths[lista_inventario[i]]))
            self.grilla_inventario[i].raise_()
        self.check_ganar()
    def check_ganar(self):
        for i in self.lista_inventario:
            if i == "ticket":
                self.ganar_signal.emit()
                self.salir()
                break
#personaje
    def init_signals(self):
        # Se conecta la señal de actualización con un método
        self.update_window_signal.connect(self.update_window)
        # Define la señal que actualizará el personaje en back-end
        self.update_character_signal = self.backend_character.update_character_signal
        # Se le asigna al back-end la señal para actualizar esta ventana
        self.backend_character.update_window_signal = self.update_window_signal
        self.backend_character.tienda_signal = self.tienda_signal
        self.backend_character.casa_signal = self.casa_signal
        self.backend_character.recoger_signal = self.recoger_signal
        self.backend_character.borrar_recoger = self.borrar_recoger
        self.borrar_recoger.connect(self.borrar)
        self.casa_signal.connect(self.dormir)
    @property
    def frame(self):
        return self._frame
    @frame.setter
    def frame(self, value):
        self._frame = value if value <= 4 else 1
    key_event_dict = {
        Qt.Key_D: 'R',
        Qt.Key_A: 'L',
        Qt.Key_W: 'U',
        Qt.Key_S: 'D'
    }
    def keyPressEvent(self, event):
        if event.key() in self.key_event_dict and not self.pausa:
            action = self.key_event_dict[event.key()]
            self.update_character_signal.emit(action)
        if event.key() == Qt.Key_O and not self.pausa:
            self.agregar_dinero.emit(100)
    def mousePressEvent(self, event):
        if not self.pausa:
            rect_inv = QRect(60, 100, 691, 141)
            rect_juego= QRect(20, 290, 841, 451)
            self.x_original = 60
            self.y_original  = 100
            self.c = 0
            self.move = False
            self.dragstart = event.pos()
            if event.buttons() & Qt.LeftButton and rect_inv.contains(event.pos()):
                for slot in self.box_inv:
                    if slot.contains(event.pos()):
                        self.x_original = slot.x()
                        self.y_original  = slot.y()
                        self.move = True

                        break
                    self.c += 1
            elif "azada" in self.lista_inventario and rect_juego.contains(event.pos()) :
                self.arar_signal.emit([self.cultivo_box, self.lista_over, event, self.pasto_box,
                self.lista_bloques, self.barra_energia])

            elif "hacha" in self.lista_inventario and rect_juego.contains(event.pos()) :
                self.chop_signal.emit([self.lista_over, event, self.removido_temporal,
                    self.barra_energia, self.pasto_box, self.bloques_roca])
            for cultivo in self.cultivo_box:
                if cultivo.contains(event.pos()):
                    self.cosechar_signal.emit([self.plantas, self.lista_over, self.barra_energia,
                    cultivo])
                    break
    def mouseReleaseEvent(self, event):
        if not self.pausa:
            rect_juego = QRect(20, 290, 841, 451)
            if QRect(self.x_original, self.y_original, 46, 42).contains(self.dragstart):
                if (self.lista_inventario[self.c] == "seed_alcachofa"
                and rect_juego.contains(event.x(), event.y())):
                    self.listas_signal.emit([self.cultivo_box, self.lista_over,
                        self.grilla_inventario[self.c], event, self.grilla_inventario, "alca",
                        self.barra_energia])
                if (self.lista_inventario[self.c] == "seed_choclo"
                and rect_juego.contains(event.x(), event.y())):
                    self.listas_signal.emit([self.cultivo_box, self.lista_over,
                        self.grilla_inventario[self.c], event, self.grilla_inventario, "choclo"
                        ,self.barra_energia])
            self.grilla_inventario[self.c].move(self.x_original, self.y_original)
            self.dragstart = None
            self.move = False
    def mouseMoveEvent(self, event):
        if not self.pausa:
            if self.dragstart is not None and event.buttons() & Qt.LeftButton and self.move:
                self.mouse_pos = event.pos()
                self.grilla_inventario[self.c].move(self.mouse_pos.x(), self.mouse_pos.y())
    def cambio_dinero(self,dinero):
        self.l_dinero.setText("Dinero:$"+str(dinero))
    def update_window(self, event):
        direction = event['direction']
        position = event['position']
        if position == 'walk':
            self.frame += 1
            self.current_sprite = QPixmap(sprites_paths[(position, direction, self.frame)])
        else:
            self.current_sprite = QPixmap(sprites_paths[(position, direction)])
        self.front_character.setPixmap(self.current_sprite)
        self.front_character.move(event['x'], event['y'])
    def receptor_ventana(self):
        self.f_timer()
        return self.show()
    def plantado_correcto(self, seed_tipo):
        self.plantado_correcto = seed_tipo[2]
        if seed_tipo[1] == "alca":
            self.plantas.append([60,"alca",self.lista_over[seed_tipo[0]].x(),
                                                                self.lista_over[seed_tipo[0]].y()])
            self.lista_over[seed_tipo[0]].setPixmap(QPixmap(stages_alca["1"]))
            self.lista_over[seed_tipo[0]].raise_()
        else:
            self.plantas.append([180,"choclo",self.lista_over[seed_tipo[0]].x(),
                                                                self.lista_over[seed_tipo[0]].y()])
            self.lista_over[seed_tipo[0]].setPixmap(QPixmap(stages_choclo["1"]))
            self.lista_over[seed_tipo[0]].raise_()
    def arar_handler(self, listas):
        self.cultivo_box = listas[0]
        self.pasto_box = listas[1]
        self.barra_energia = listas[2]
        self.lista_bloques[listas[3]].setPixmap(QPixmap("sprites/mapa/tile003.png"))
    def actualizar_plantas(self):
        pos = 0
        for planta in self.plantas:
            if planta[1] == "alca" and planta[0] < 6 * TIEMPO_ALCACHOFAS:
                for fase in range(1,7):
                    if planta[0] + 1 == TIEMPO_ALCACHOFAS * fase:
                        for bloque in self.lista_over:
                            if bloque.x() == planta[2] and bloque.y() == planta[3]:
                                self.lista_over[pos].setPixmap(QPixmap(stages_alca[str(fase)]))
                            pos += 1
                planta[0] += 1
            if planta[1] == "choclo" and planta[0] < 7 * TIEMPO_CHOCLOS:
                for fase in range(1,8):
                    if planta[0] + 1 == TIEMPO_CHOCLOS * fase:
                        for bloque in self.lista_over:
                            if bloque.x() == planta[2] and bloque.y() == planta[3]:
                                self.lista_over[pos].setPixmap(QPixmap(stages_choclo[str(fase)]))
                            pos += 1
                planta[0] += 1
    def actualizar_tiempo(self):
        if not self.pausa:
            self.actualizar_plantas()
            if self.tiempo[1] + 30 >= 60:
                self.tiempo[1] = 0
                self.tiempo[0] += 1
                if self.tiempo[0] + 1 >=24:
                    self.tiempo[0]=0
                    self.dia +=1
                    self.l_dia.setText("Dia: "+str(self.dia))
                    num = random.randint(1,10)
                    if num >= PROB_ARBOL*10:
                        self.aparecer_signal.emit([self.lista_bloques,self.pasto_box,"arbol"])
                    elif num <= PROB_ORO*10:
                        self.aparecer_signal.emit([self.lista_bloques,self.pasto_box,"oro"])
            else:
                self.tiempo[1] += 30
            if len(str(self.tiempo[0])) == 1 and len(str(self.tiempo[1])) == 1 :
                self.l_hora.setText("Hora: 0"+str(self.tiempo[0])+":0"+str(self.tiempo[1]))
            elif  len(str(self.tiempo[0])) == 1 and len(str(self.tiempo[1]))== 2:
                self.l_hora.setText("Hora: 0"+str(self.tiempo[0])+":"+str(self.tiempo[1]))
            elif  len(str(self.tiempo[0])) == 2 and len(str(self.tiempo[1]))== 1:
                self.l_hora.setText("Hora: "+str(self.tiempo[0])+":0"+str(self.tiempo[1]))
            else:
                self.l_hora.setText("Hora: "+str(self.tiempo[0])+":"+str(self.tiempo[1]))

    def generar_handler(self, lista):
        if not self.pausa:
            if lista[2] == "arbol":
                self.lista_over[lista[0]].setPixmap(QPixmap("sprites/otros/tree.png"))
                self.removido_temporal.append(self.pasto_box.pop(lista[1]))
                self.bloques_roca.append(self.removido_temporal[-1])
                self.backend_character.lista_bloques_roca(self.bloques_roca)
            if lista[2] == "oro":
                self.lista_over[lista[0]].setPixmap(QPixmap(objetos_paths["oro"]))
                self.removido_temporal.append(self.pasto_box.pop(lista[1]))
                self.recolectables.append([self.lista_over[lista[0]].x(),
                                                            self.lista_over[lista[0]].y(),"oro"])
                self.backend_character.ubic_recoger(self.recolectables)


    def cortar_handler(self, listas):
        self.lista_over[listas[0]].setPixmap(QPixmap(objetos_paths["madera"]))
        self.recolectables.append([self.lista_over[listas[0]].x(),
                                                        self.lista_over[listas[0]].y(),"madera"])
        self.backend_character.ubic_recoger(self.recolectables)
        self.removido_temporal = listas[1]
        self.barra_energia = listas[2]
        self.pasto_box = listas[3]
        self.bloques_roca = listas[4]
        self.backend_character.lista_bloques_roca(self.bloques_roca)

    def cosechar_handler(self, listas):
        self.plantas = listas[0]
        self.barra_energia = listas[1]
        if listas[3] == "choclo":
            self.lista_over[listas[2]].setPixmap(QPixmap(objetos_paths["choclo"]))
            self.recolectables.append([self.lista_over[listas[2]].x(),
                                                        self.lista_over[listas[2]].y(),"choclo"])
            self.backend_character.ubic_recoger(self.recolectables)
        if listas[3] == "alca":
            self.lista_over[listas[2]].setPixmap(QPixmap(objetos_paths["alca"]))
            self.recolectables.append([self.lista_over[listas[2]].x(),
                                                            self.lista_over[listas[2]].y(),"alca"])
            self.backend_character.ubic_recoger(self.recolectables)

    def borrar(self, pos):
        c = 0
        for over in self.lista_over:
            if self.recolectables[pos][0] == over.x() and self.recolectables[pos][1] == over.y():
                self.lista_over[c].setPixmap(QPixmap(""))
                break
            c+=1

        self.recolectables.pop(pos)
    def dormir(self):
        self.barra_energia.setValue(ENERGIA_JUGADOR)
        self.dia += 1
        self.l_dia.setText("Dia: "+ str(self.dia))
        tick_restante = 48 - 2 * self.tiempo[0]
        if self.tiempo[1] == 30:
            tick_restante -= 1
        self.tiempo[0] = 0
        self.tiempo[1] = 0
        if len(str(self.tiempo[0])) == 1 and len(str(self.tiempo[1])) == 1 :
            self.l_hora.setText("Hora: 0"+str(self.tiempo[0])+":0"+str(self.tiempo[1]))
        for i in range(0, tick_restante):
            self.actualizar_plantas()
        num = random.randint(1,10)
        if num >= PROB_ARBOL*10:
            self.aparecer_signal.emit([self.lista_bloques,self.pasto_box,"arbol"])
        elif num <= PROB_ORO*10:
            self.aparecer_signal.emit([self.lista_bloques,self.pasto_box,"oro"])

    def salir(self):
        self.close()
    def pausar(self):
        if self.pausa == False:
            self.pausa = True
        else:
            self.pausa = False

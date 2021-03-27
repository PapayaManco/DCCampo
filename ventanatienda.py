from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QProgressBar)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QMetaObject)
from PyQt5.QtGui import (QPixmap, QFont, QMovie, QBrush, QColor, QPalette, QIcon)
from character import Character
import os
import sys
from parametros_precios import (PRECIO_ALACACHOFAS, PRECIO_CHOCLOS, PRECIO_LEÑA, PRECIO_ORO,
    PRECIO_SEMILLA_ALCACHOFAS, PRECIO_SEMILLA_CHOCLOS, PRECIO_HACHA, PRECIO_AZADA, PRECIO_TICKET)
class VentanaTienda(QWidget):

    mapa_signal = pyqtSignal(str)
    venta_signal = pyqtSignal(list)
    compra_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def cerrar(self):
        self.close()

    def init_gui(self):
        self.setGeometry(320, 450, 800, 500)
        self.setWindowTitle('La tiendita')
        icon = QIcon()
        icon.addPixmap(QPixmap("sprites/otros/fish.png"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.fondo_tienda = QLabel(self)
        self.fondo_tienda.setGeometry(QRect(0, 0, 800, 500))
        self.fondo_tienda.setPixmap(QPixmap("sprites/otros/window_template.jpg"))
        self.fondo_tienda.setScaledContents(True)

        self.titulo_tienda = QLabel(self)
        self.titulo_tienda.setGeometry(QRect(40, 30, 731, 51))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.titulo_tienda.setFont(font)
        self.titulo_tienda.setText("ITEM      PRECIO      ACCION  |  ITEM      PRECIO      ACCION")

        self.l_precio_az = QLabel(self)
        self.l_precio_az.setGeometry(QRect(170, 110, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_az.setFont(font)
        self.l_precio_az.setText("$"+str(PRECIO_AZADA))

        self.btn_comprar_azada = QPushButton(self)
        self.btn_comprar_azada.setGeometry(QRect(280, 90, 71, 21))
        self.btn_comprar_azada.setText("Comprar")
        self.btn_comprar_azada.clicked.connect(self.comprar_a)

        self.btn_vender_azada = QPushButton(self)
        self.btn_vender_azada.setGeometry(QRect(280, 120, 71, 21))
        self.btn_vender_azada.setText("Vender")
        self.btn_vender_azada.clicked.connect(self.vender_a)

        self.img_azada = QLabel(self)
        self.img_azada.setGeometry(QRect(50, 90, 51, 61))
        self.img_azada.setPixmap(QPixmap("sprites/otros/hoe.png"))

        self.foto_hacha = QLabel(self)
        self.foto_hacha.setGeometry(QRect(40, 180, 51, 61))
        self.foto_hacha.setPixmap(QPixmap("sprites/otros/axe.png"))

        self.l_precio_h = QLabel(self)
        self.l_precio_h.setGeometry(QRect(170, 200, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_h.setFont(font)
        self.l_precio_h.setText("$"+str(PRECIO_HACHA))

        self.btn_comprar_hacha = QPushButton(self)
        self.btn_comprar_hacha.setGeometry(QRect(280, 180, 71, 21))
        self.btn_comprar_hacha.setText("Comprar")
        self.btn_comprar_hacha.clicked.connect(self.comprar_h)

        self.btn_vender_hacha = QPushButton(self)
        self.btn_vender_hacha.setGeometry(QRect(280, 210, 71, 21))
        self.btn_vender_hacha.setText("Vender")
        self.btn_vender_hacha.clicked.connect(self.vender_h)

        self.semillas_a_f = QLabel(self)
        self.semillas_a_f.setGeometry(QRect(40, 270, 51, 61))
        self.semillas_a_f.setPixmap(QPixmap("sprites/cultivos/alcachofa/seeds.png"))

        self.l_precio_seed_al = QLabel(self)
        self.l_precio_seed_al.setGeometry(QRect(170, 290, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_seed_al.setFont(font)
        self.l_precio_seed_al.setText("$"+str(PRECIO_SEMILLA_ALCACHOFAS))

        self.btn_comprar_seed_a = QPushButton(self)
        self.btn_comprar_seed_a.setGeometry(QRect(280, 280, 71, 21))
        self.btn_comprar_seed_a.setText("Comprar")
        self.btn_comprar_seed_a.clicked.connect(self.comprar_seed_a)

        self.btn_vender_seed_a = QPushButton(self)
        self.btn_vender_seed_a.setGeometry(QRect(280, 310, 71, 21))
        self.btn_vender_seed_a.setText("Vender")
        self.btn_vender_seed_a.clicked.connect(self.vender_seed_a)


        self.semillas_c_f = QLabel(self)
        self.semillas_c_f.setGeometry(QRect(40, 380, 51, 61))
        self.semillas_c_f.setPixmap(QPixmap("sprites/cultivos/choclo/seeds.png"))

        self.l_precio_seed_ch = QLabel(self)
        self.l_precio_seed_ch.setGeometry(QRect(170, 400, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_seed_ch.setFont(font)
        self.l_precio_seed_ch.setText("$"+str(PRECIO_SEMILLA_CHOCLOS))

        self.btn_comprar_seed_ch = QPushButton(self)
        self.btn_comprar_seed_ch.setGeometry(QRect(280, 390, 71, 21))
        self.btn_comprar_seed_ch.setText("Comprar")
        self.btn_comprar_seed_ch.clicked.connect(self.comprar_seed_ch)

        self.btn_vender_seed_ch = QPushButton(self)
        self.btn_vender_seed_ch.setGeometry(QRect(280, 420, 71, 21))
        self.btn_vender_seed_ch.setText("Vender")
        self.btn_vender_seed_ch.clicked.connect(self.vender_seed_ch)

        self.imng_alca = QLabel(self)
        self.imng_alca.setGeometry(QRect(400, 90, 41, 51))
        self.imng_alca.setPixmap(QPixmap("sprites/recursos/artichoke.png"))

        self.l_precio_al = QLabel(self)
        self.l_precio_al.setGeometry(QRect(530, 110, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_al.setFont(font)
        self.l_precio_al.setText("$"+str(PRECIO_ALACACHOFAS))

        self.btn_vender_al = QPushButton(self)
        self.btn_vender_al.setGeometry(QRect(640, 100, 71, 31))
        self.btn_vender_al.setText("Vender")
        self.btn_vender_al.clicked.connect(self.vender_alcachofa)

        self.img_choclo = QLabel(self)
        self.img_choclo.setGeometry(QRect(400, 170, 41, 51))
        self.img_choclo.setPixmap(QPixmap("sprites/recursos/corn.png"))

        self.l_precio_ch = QLabel(self)
        self.l_precio_ch.setGeometry(QRect(530, 190, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_ch.setFont(font)
        self.l_precio_ch.setText("$"+str(PRECIO_CHOCLOS))


        self.btn_vender_choclo = QPushButton(self)
        self.btn_vender_choclo.setGeometry(QRect(640, 180, 71, 31))
        self.btn_vender_choclo.setText("Vender")
        self.btn_vender_choclo.clicked.connect(self.vender_choclo)

        self.img_madera = QLabel(self)
        self.img_madera.setGeometry(QRect(400, 270, 41, 51))
        self.img_madera.setPixmap(QPixmap("sprites/recursos/wood.png"))

        self.l_precio_madera = QLabel(self)
        self.l_precio_madera.setGeometry(QRect(530, 280, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_madera.setFont(font)
        self.l_precio_madera.setText("$"+str(PRECIO_LEÑA))

        self.btn_vender_mad = QPushButton(self)
        self.btn_vender_mad.setGeometry(QRect(640, 280, 71, 31))
        self.btn_vender_mad.setText("Vender")
        self.btn_vender_mad.clicked.connect(self.vender_madera)

        self.img_oro = QLabel(self)
        self.img_oro.setGeometry(QRect(400, 340, 41, 51))
        self.img_oro.setPixmap(QPixmap("sprites/recursos/gold.png"))

        self.l_precio_oro = QLabel(self)
        self.l_precio_oro.setGeometry(QRect(530, 350, 31, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_precio_oro.setFont(font)
        self.l_precio_oro.setText("$"+str(PRECIO_ORO))

        self.btn_vender_oro = QPushButton(self)
        self.btn_vender_oro.setGeometry(QRect(640, 350, 71, 31))
        self.btn_vender_oro.setText("Vender")
        self.btn_vender_oro.clicked.connect(self.vender_oro)

        self.img_ticket = QLabel(self)
        self.img_ticket.setGeometry(QRect(400, 400, 41, 51))
        self.img_ticket.setPixmap(QPixmap("sprites/otros/ticket.png"))

        self.l_ticket = QLabel(self)
        self.l_ticket.setGeometry(QRect(530, 410, 310, 21))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_ticket.setFont(font)
        self.l_ticket.setText("$"+str(PRECIO_TICKET))

        self.l_ticket_btn = QPushButton(self)
        self.l_ticket_btn.setGeometry(QRect(640, 410, 71, 31))
        self.l_ticket_btn.setText("Comprar")
        self.l_ticket_btn.clicked.connect(self.comprar_ticket)


        self.l_resp = QLabel(self)
        self.l_resp.setGeometry(QRect(220, 450, 340, 31))
        font = QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        self.l_resp.setFont(font)
        self.l_resp.setText("")

    def abrir(self):
        self.l_resp.setText("")
        self.show()

    def respuesta_tienda_handler(self, resp):
        if resp == 0:
            self.l_resp.setText("Venta realizada con exito!")
        elif resp == 1:
            self.l_resp.setText("Lo sentimos,no tienes el objeto")
        elif resp == 2:
            self.l_resp.setText("Compra exitosa!")
        elif resp == 3:
            self.l_resp.setText("Lo sentimos, inventario lleno")
        elif resp == 4:
            self.l_resp.setText("Lo sentimos,dinero insuficiente")

    def vender_a(self):
        self.venta_signal.emit([PRECIO_AZADA,"azada"])
    def vender_h(self):
        self.venta_signal.emit([PRECIO_HACHA,"hacha"])
    def vender_seed_a(self):
        self.venta_signal.emit([PRECIO_SEMILLA_ALCACHOFAS,"seed_alcachofa"])
    def vender_seed_ch(self):
        self.venta_signal.emit([PRECIO_SEMILLA_CHOCLOS,"seed_choclo"])
    def vender_alcachofa(self):
        self.venta_signal.emit([PRECIO_ALACACHOFAS,"alca"])
    def vender_choclo(self):
        self.venta_signal.emit([PRECIO_CHOCLOS,"choclo"])
    def vender_madera(self):
        self.venta_signal.emit([PRECIO_LEÑA,"madera"])
    def vender_oro(self):
        self.venta_signal.emit([PRECIO_ORO,"oro"])


    def comprar_ticket(self):
        self.compra_signal.emit([PRECIO_ORO,"ticket"])

    def comprar_a(self):
        self.compra_signal.emit([PRECIO_AZADA,"azada"])
    def comprar_h(self):
        self.compra_signal.emit([PRECIO_HACHA,"hacha"])
    def comprar_seed_a(self):
        self.compra_signal.emit([PRECIO_SEMILLA_ALCACHOFAS,"seed_alcachofa"])
    def comprar_seed_ch(self):
        self.compra_signal.emit([PRECIO_SEMILLA_CHOCLOS,"seed_choclo"])
    def salir(self):
        self.close()

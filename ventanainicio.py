from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QProgressBar)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QMetaObject)
from PyQt5.QtGui import (QPixmap, QFont, QMovie, QBrush, QColor, QPalette, QIcon)
from character import Character
import os
import sys
from parametros_generales import N
import random


class VentanaInicio(QWidget):

    mapa_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def ingreso_mapa(self):
        self.mapa_signal.emit(self.i_text.text())

    def incorrecto(self):
        self.error_text.setText("Por favor ingresa una mapa válido")

    def cerrar(self):
        self.close()

    def init_gui(self):
        self.setGeometry(400, 200, 581, 303)
        self.setWindowTitle('Bienvenido al DCCampo!')

        palette = QPalette()
        brush = QBrush(QColor(195, 190, 168))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        self.setPalette(palette)

        icon = QIcon()
        icon.addPixmap(QPixmap("sprites/otros/fish.png"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        icon1 = QIcon("sprites/otros/fish.png")

        self.logo_img = QLabel("", self)
        self.logo_img.setPixmap(QPixmap("sprites/otros/logo.png"))
        self.logo_img.setGeometry(QRect(110,20,390,122))

        self.texto_ingresar = QLabel("Ingresa el nombre del mapa a cargar:",self)
        self.texto_ingresar.setGeometry(QRect(190, 150, 201, 20))

        self.i_text = QLineEdit('', self)
        self.i_text.setGeometry(QRect(190, 180, 200, 20))

        self.boton_jugar = QPushButton("Jugar",self)
        self.boton_jugar.setGeometry(QRect(240, 210, 81, 31))
        self.boton_jugar.clicked.connect(self.ingreso_mapa)

        self.error_text = QLabel("",self)
        self.error_text.setGeometry(QRect(190, 245, 200, 20))

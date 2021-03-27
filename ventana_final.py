from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QApplication, QHBoxLayout, QVBoxLayout, QSystemTrayIcon, QProgressBar)
from PyQt5.QtCore import (pyqtSignal, Qt, QRect, QSize, QMetaObject)
from PyQt5.QtGui import (QPixmap, QFont, QMovie, QBrush, QColor, QPalette, QIcon)



class VentanaGanar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.setGeometry(500, 250, 450, 303)
        self.setWindowTitle('GANASTE!!!!!!!')

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

        self.texto_ganador = QLabel(self)
        self.texto_ganador.setGeometry(QRect(125, 120, 211, 81))
        font = QFont()
        font.setFamily("qtquickcontrols")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.texto_ganador.setText("GANASTE")
        self.texto_ganador.setFont(font)

    def mostrar(self):
        self.show()

class VentanaPerder(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        self.setGeometry(500, 250, 450, 303)
        self.setWindowTitle('Perdedor :(')

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

        self.texto_perdedor = QLabel(self)
        self.texto_perdedor.setGeometry(QRect(125, 120, 211, 81))
        font = QFont()
        font.setFamily("qtquickcontrols")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.texto_perdedor.setText("PERDISTE")
        self.texto_perdedor.setFont(font)

    def mostrar(self):
        self.show()

from PyQt5.QtCore import QObject, pyqtSignal
import os
from parametros_generales import (MONEDAS_INICIALES, ENERGIA_PLANTAR)
from parametros_acciones import ENERGIA_COSECHAR , ENERGIA_HERRAMIENTA
from character import Character
from random import randint

class DCCampo(QObject):

    cerrar_signal = pyqtSignal()
    respuesta_mapa = pyqtSignal(list)
    mapa_incorrecto = pyqtSignal()
    dinero_signal = pyqtSignal(int)
    resp_tienda_signal = pyqtSignal(int)
    inventario_signal = pyqtSignal(list)
    plant_signal = pyqtSignal(list)
    perder_juego_signal = pyqtSignal()
    arar_retorno_signal = pyqtSignal(list)
    cerrar = pyqtSignal()
    generar_resp_signal = pyqtSignal(list)
    chop_signal_return =  pyqtSignal(list)
    cosechar_resp_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._dinero = MONEDAS_INICIALES
        self.inventario_max = 36
        self.inventario = []
        for i in range(0,self.inventario_max):
            self.inventario.append("")
        self.inventario[0] = "azada"

    @property
    def Billetera(self):
        return self._dinero

    @Billetera.setter
    def Billetera(self, value):
        self._dinero = value

    def mapa_handler(self,data):
        if  os.path.exists("mapas/"+data+".txt"):
            self.cerrar_signal.emit()
            with open("mapas/"+data+".txt", "r", encoding="utf-8") as file:
                lineas = [line.strip().split(" ") for line in file.readlines()]
                self.respuesta_mapa.emit(lineas)

        else:
            self.mapa_incorrecto.emit()

    def venta(self, lista):
        if lista[1] in self.inventario:
            self._dinero +=  lista[0]
            self.dinero_signal.emit(self._dinero)
            pos = self.inventario.index(lista[1])
            self.inventario[pos] = ""
            self.resp_tienda_signal.emit(0)
            self.inventario_signal.emit(self.inventario)
        else:
            self.resp_tienda_signal.emit(1)
    def truco(self, int):
        self._dinero += int
        self.dinero_signal.emit(self._dinero)

    def compra(self, lista):
        c = 0
        for i in range(len(self.inventario)):
            if self.inventario[i] != "":
                c+=1
        if c == 36:
            self.resp_tienda_signal.emit(3)
        else:
            #aqui no funciona el setter por estar dentro del mismo objeto
            anterior = self._dinero
            self._dinero -= lista[0]
            if self._dinero < 0:
                self._dinero = anterior
            if anterior == self._dinero:
                self.resp_tienda_signal.emit(4)
            else:
                self.dinero_signal.emit(self._dinero)
                for i in range(len(self.inventario)):
                    if self.inventario[i] == "":
                        self.inventario[i] = lista[1]
                        self.resp_tienda_signal.emit(2)
                        self.inventario_signal.emit(self.inventario)
                        break

    def plantado(self, listas):
        for espa_culti in listas[0]:
            if espa_culti.contains(listas[3].x(), listas[3].y()):
                seed = self.buscar(espa_culti.x(), espa_culti.y(), listas[1])
                pos  = self.buscar(listas[2].x(), listas[2].y(), listas[4])
                if listas[1][seed].pixmap() == None:
                    if (listas[6].value() - ENERGIA_PLANTAR) > 0:
                        listas[6].setValue(listas[6].value() - ENERGIA_PLANTAR)
                        self.plant_signal.emit([seed, listas[5], listas[6]])
                        self.inventario[pos] = ""
                        self.inventario_signal.emit(self.inventario)
                    else:
                        listas[6].setValue(0)
                        self.perder_juego_signal.emit()
                        self.cerrar.emit()
                break

    def arar(self, listas):
        p = 0
        for pasto in listas[3]:
            if pasto.contains(listas[2].pos()):
                for over in listas[1]:
                    if over.x() == pasto.x() and over.y() == pasto.y() and over.pixmap() == None:
                        if (listas[5].value() - ENERGIA_COSECHAR) > 0:
                            listas[5].setValue(listas[5].value() - ENERGIA_COSECHAR)
                            listas[0].append(pasto)
                            listas[3].remove(pasto)
                            self.arar_retorno_signal.emit([listas[0],listas[3],listas[5],p])
                        else:
                            listas[5].setValue(0)
                            self.perder_juego_signal.emit()
                            self.cerrar.emit()
                        break
                    p += 1
                break


    def buscar(self,pos_x , pos_y, lista):
        v = 0
        for tile in lista:
            if pos_x == tile.x() and pos_y == tile.y():
                return v
            v+=1
    def generar(self, lista):
        pos_bloque = 0
        if lista[2] == "arbol":
            num = randint(0, len(lista[1]))
            for bloque in lista[0]:
                if lista[1][num].x() == bloque.x() and lista[1][num].y() == bloque.y() :
                    self.generar_resp_signal.emit([pos_bloque,num,"arbol"])
                    break
                pos_bloque+=1

        if lista[2] == "oro":
            num = randint(0, len(lista[1]))
            for bloque in lista[0]:
                if lista[1][num].x() == bloque.x() and lista[1][num].y() == bloque.y() :
                    self.generar_resp_signal.emit([pos_bloque,num,"oro"])
                    break
                pos_bloque+=1
    def cortar(self, lista):
        pos_removido = 0
        for removido in lista[2]:
            if removido.contains(lista[1].pos()):
                if (lista[3].value() - ENERGIA_HERRAMIENTA) > 0:
                    b = self.buscar(lista[2][pos_removido].x(),lista[2][pos_removido].y(),lista[5])
                    lista[5].pop(b)
                    a = lista[2].pop(pos_removido)
                    lista[4].append(a)
                    pos = self.buscar(lista[4][-1].x(),lista[4][-1].y(), lista[0])
                    lista[3].setValue(lista[3].value() - ENERGIA_HERRAMIENTA)
                    self.chop_signal_return.emit([pos, lista[2], lista[3], lista[4], lista[5]])
                else:
                    listas[3].setValue(0)
                    self.perder_juego_signal.emit()
                    self.cerrar.emit()

                break
            pos_removido += 1
    def cosechar(self, lista):
        c_planta = 0
        pos = 0
        for planta in lista[0]:
            for a in range (len(lista[1])) :
                if ((lista[3].x() == lista[1][a].x() and lista[3].y() == lista[1][a].y()) and
                    lista[1][a].pixmap() != None):
                    if lista[2].value() - ENERGIA_COSECHAR > 0:
                        lista[2].setValue(lista[2].value() - ENERGIA_COSECHAR)
                        pos = a
                        lista[0].pop(c_planta)
                        self.cosechar_resp_signal.emit([lista[0],lista[2], pos, planta[1]])
                    else:
                        listas[2].setValue(0)
                        self.perder_juego_signal.emit()
                        self.cerrar.emit()
                    break
            c_planta += 1
    def recoger(self, str):
        c=0
        for i in range(len(self.inventario)):
            if self.inventario[i] != "":
                c+=1
        if c == 36 :
            pass
        else:
            for i in range(len(self.inventario)):
                if self.inventario[i] == "":
                    self.inventario[i] = str
                    self.inventario_signal.emit(self.inventario)
                    break

from PyQt5.QtWidgets import QApplication
from ventanainicio import (VentanaInicio)
from ventanajuego import (VentanaJuego)
from ventanatienda import (VentanaTienda)
import sys
from DCCampo import DCCampo
from ventana_final import(VentanaGanar, VentanaPerder)

def hook(type, value, traceback):
    print(type)
    print(traceback)
sys.__excepthook__ = hook


app = QApplication(sys.argv)
ventana = VentanaInicio()
ventana.show()
campo = DCCampo()
tienda= VentanaTienda()
ventanaganador = VentanaGanar()
ventanaperder = VentanaPerder()

ventana.mapa_signal.connect(campo.mapa_handler)

#signals de antes de iniciar el juego
campo.mapa_incorrecto.connect(ventana.incorrecto)
campo.cerrar_signal.connect(ventana.cerrar)

ventana1 = VentanaJuego()
campo.respuesta_mapa.connect(ventana1.crear_mapa)
#por si jugador parte con dinero
ventana1.cambio_dinero(campo._dinero)
#por si el jugador parte con objetos en el inventario
campo.inventario_signal.connect(ventana1.act_inventario)
campo.inventario_signal.emit(campo.inventario)
campo.dinero_signal.connect(ventana1.cambio_dinero)

campo.cerrar_signal.connect(ventana1.receptor_ventana)
ventana1.tienda_signal.connect(tienda.abrir)
ventana1.listas_signal.connect(campo.plantado)
ventana1.arar_signal.connect(campo.arar)
campo.arar_retorno_signal.connect(ventana1.arar_handler)
ventana1.chop_signal.connect(campo.cortar)
campo.chop_signal_return.connect(ventana1.cortar_handler)
ventana1.cosechar_signal.connect(campo.cosechar)
ventana1.recoger_signal.connect(campo.recoger)
campo.cosechar_resp_signal.connect(ventana1.cosechar_handler)
ventana1.aparecer_signal.connect(campo.generar)
campo.generar_resp_signal.connect(ventana1.generar_handler)
campo.perder_juego_signal.connect(ventanaperder.mostrar)
campo.cerrar.connect(ventana1.salir)
ventana1.ganar_signal.connect(ventanaganador.mostrar)
ventana1.ganar_signal.connect(tienda.salir)

campo.plant_signal.connect(ventana1.plantado_correcto)
tienda.compra_signal.connect(campo.compra)
tienda.venta_signal.connect(campo.venta)
ventana1.agregar_dinero.connect(campo.truco)
campo.resp_tienda_signal.connect(tienda.respuesta_tienda_handler)


sys.exit(app.exec_())

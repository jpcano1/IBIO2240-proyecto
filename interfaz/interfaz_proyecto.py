from tkinter import *
from interfaz.panel_parametros import PanelParametros
from interfaz.panel_metodos import PanelMetodos
from interfaz.panel_opciones import PanelOpciones
from interfaz.panel_senales import PanelSenales
from interfaz.panel_puntos import PanelPuntos

class InterfazProyecto(Tk):

    def __init__(self, name="Interfaz"):
        super(InterfazProyecto, self).__init__(className=name)

        self.panel_parametros = PanelParametros(self)
        self.panel_parametros.grid(row=0, column=1)

        self.panel_metodos = PanelMetodos(self)
        self.panel_metodos.grid(row=1, column=1)

        self.panel_opciones = PanelOpciones(self)
        self.panel_opciones.grid(row=0, column=0)

        self.panel_senales = PanelSenales(self)
        self.panel_senales.grid(row=1, column=0)

        self.panel_puntos = PanelPuntos(self)
        self.panel_puntos.grid(row=2, column=0)

if __name__ == '__main__':
    interfaz = InterfazProyecto(" ECG Monitor")
    interfaz.mainloop()

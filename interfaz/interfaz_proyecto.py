from tkinter import *
from interfaz.panel_parametros import PanelParametros
from interfaz.panel_metodos import PanelMetodos
from interfaz.panel_opciones import PanelOpciones
from interfaz.panel_senales import PanelSenales
from interfaz.panel_puntos import PanelPuntos
from mundo.ecg_generator import ECGGenerator

class InterfazProyecto(Tk):

    def __init__(self, name="Interfaz"):
        super(InterfazProyecto, self).__init__(className=name)

        self.configure(background='#212946')
        self.ecg=ECGGenerator()

        self.panel_parametros = PanelParametros(self)
        self.panel_parametros.grid(row=0, column=1)
        self.panel_parametros.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_metodos = PanelMetodos(self)
        self.panel_metodos.grid(row=1, column=1)
        self.panel_metodos.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_opciones = PanelOpciones(self)
        self.panel_opciones.grid(row=0, column=0)
        self.panel_opciones.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_senales = PanelSenales(self)
        self.panel_senales.grid(row=1, column=0)
        self.panel_senales.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_puntos = PanelPuntos(self)
        self.panel_puntos.grid(row=2, column=0)
        self.panel_puntos.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

    def updatePoints(self):
        return self.ecg.a_i,self.ecg.b_i

    def plot(self):
        self.panel_senales.plot_canvas(self.ecg.interval,self.ecg.points)
    def getXY(self):
        return self.ecg.interval,self.ecg.points
if __name__ == '__main__':
    interfaz = InterfazProyecto(" ECG Monitor")
    interfaz.mainloop()

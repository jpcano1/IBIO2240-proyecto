from tkinter import *

class PanelParametros(Frame):

    def __init__(self, pInterfaz):
        super(PanelParametros, self).__init__(master=pInterfaz, highlightbackground="black",
                                              highlightcolor="black", highlightthickness=3)
        self.interfaz = pInterfaz

        # Titulo
        Label(master=self, text="Parámetros").grid(row=0, column=0)

        # Labels Parametros
        Label(master=self, text="Frecuencia Cardíaca").grid(row=1, column=0)

        Label(master=self, text="# de latidos").grid(row=2, column=0)

        Label(master=self, text="Frecuencia Muestreo").grid(row=3, column=0)

        Label(master=self, text="Factor de Ruido").grid(row=4, column=0)

        # Input Parametros
        self.frecuencia_input = Entry(master=self)
        self.frecuencia_input.grid(row=1, column=1)

        self.latidos_input = Entry(master=self)
        self.latidos_input.grid(row=2, column=1)

        self.frecuencia_muestreo_input = Entry(master=self)
        self.frecuencia_muestreo_input.grid(row=3, column=1)

        self.factor_ruido_input = Entry(master=self)
        self.factor_ruido_input.grid(row=4, column=1)
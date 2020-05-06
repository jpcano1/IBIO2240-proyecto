from tkinter import *

class PanelParametros(Frame):

    def __init__(self, pInterfaz):
        super(PanelParametros, self).__init__(master=pInterfaz, highlightbackground="black", highlightcolor="black",
                         highlightthickness=3)
        self.principial = pInterfaz

        # Titulo
        self.title = Label(master=self, text="Parámetros")
        self.title.grid(row=0, column=0)

        # Labels Parametros
        self.frecuencia_label = Label(master=self, text="Frecuencia Cardíaca")
        self.frecuencia_label.grid(row=1, column=0)

        self.latidos = Label(master=self, text="# de latidos")
        self.latidos.grid(row=2, column=0)

        self.frecuencia_muestreo = Label(master=self, text="Frecuencia Muestreo")
        self.frecuencia_muestreo.grid(row=3, column=0)

        self.factor_ruido = Label(master=self, text="Factor de Ruido")
        self.factor_ruido.grid(row=4, column=0)

        # Input Parametros
        self.frecuencia_input = Entry(master=self)
        self.frecuencia_input.grid(row=1, column=1)

        self.latidos_input = Entry(master=self)
        self.latidos_input.grid(row=2, column=1)

        self.frecuencia_muestreo_input = Entry(master=self)
        self.frecuencia_muestreo_input.grid(row=3, column=1)

        self.factor_ruido_input = Entry(master=self)
        self.factor_ruido_input.grid(row=4, column=1)
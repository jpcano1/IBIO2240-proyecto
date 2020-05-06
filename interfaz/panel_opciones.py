from tkinter import *

class PanelOpciones(Frame):

    GUARDAR = "Guardar"
    CARGAR = "Cargar"

    def __init__(self, pInterfaz):
        super(PanelOpciones, self).__init__(master=pInterfaz, highlightbackground="black", highlightcolor="black",
                         highlightthickness=3)

        # Botones
        self.guardar_boton = Button(master=self, text=self.GUARDAR)
        self.guardar_boton.pack(side=LEFT)

        self.cargar_boton = Button(master=self, text=self.CARGAR)
        self.cargar_boton.pack(side=RIGHT)
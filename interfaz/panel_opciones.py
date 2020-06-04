from tkinter import *
class PanelOpciones(Frame):

    GUARDAR = "Guardar"
    CARGAR = "Cargar"

    def __init__(self, pInterfaz):
        super(PanelOpciones, self).__init__(master=pInterfaz, highlightbackground="#F5D300", highlightcolor="#F5D300",
                         highlightthickness=3)

        self.interfaz = pInterfaz

        # Botones
        self.guardar_boton = Button(master=self,command=self.save, text=self.GUARDAR,background='#FE53BB',
                                    foreground="#212946", font=('calibri', 15, 'bold'),borderwidth='4')
        self.guardar_boton.pack(side=LEFT)

        self.cargar_boton = Button(master=self,command=self.load, text=self.CARGAR,background='#FE53BB',
                                   foreground="#212946", font=('calibri', 15, 'bold'),borderwidth='4')
        self.cargar_boton.pack(side=RIGHT)

    def save(self):
        self.interfaz.save()

    def load(self):
        self.interfaz.load()
from tkinter import *

class PanelMetodos(Frame):

    def __init__(self, pInterfaz):
        super(PanelMetodos, self).__init__(master=pInterfaz,
                                           highlightbackground="black", highlightcolor="black", highlightthickness=3)

        # Titulo
        self.title = Label(master=self, text="Metodo de solucion de ED")
        self.title.pack(side=TOP)

        # Radio Buttons
        self.radio_euler_adelante = Radiobutton(master=self, text="Euler Adelante", value="EA")
        self.radio_euler_adelante.pack()

        self.radio_euler_atras = Radiobutton(master=self, text="Euler Atrás", value="EAT")
        self.radio_euler_atras.pack()

        self.radio_euler_modificado = Radiobutton(master=self, text="Euler Modificado", value="EM")
        self.radio_euler_modificado.pack()

        self.radio_runge_kutta2 = Radiobutton(master=self, text="Runge Kutta 2", value="RK2")
        self.radio_runge_kutta2.pack()

        self.radio_runge_kutta4 = Radiobutton(master=self, text="Runge Kutta 4", value="RK4")
        self.radio_runge_kutta4.pack()
from tkinter import *
import tkinter.ttk as ttk
class PanelMetodos(Frame):

    def __init__(self, pInterfaz):
        super(PanelMetodos, self).__init__(master=pInterfaz,
                                           highlightbackground="black", highlightcolor="black", highlightthickness=3)

        self.interfaz = pInterfaz
        self.configure(background='#212946')

        # Titulo
        Label(master=self, text="Metodo de solucion de ED",background='#212946',foreground='#08F7FE').pack(side=TOP)

        self.var_metodo = StringVar()

        # Radio Buttons
        self.radio_euler_adelante = Radiobutton(master=self, text="Euler Adelante",background='#212946',
                                                foreground='#00ff41', activebackground='#212946',
                                                activeforeground='#00ff41', selectcolor='#212946',
                                                value="EA", variable=self.var_metodo)
        self.radio_euler_adelante.pack(expand=True, fill='both')

        self.radio_euler_atras = Radiobutton(master=self, text="Euler Atrás",background='#212946',
                                             foreground='#00ff41', activebackground='#212946',
                                             activeforeground='#00ff41', selectcolor='#212946',
                                             value="EAT", variable=self.var_metodo)
        self.radio_euler_atras.pack(expand=True, fill='both')

        self.radio_euler_modificado = Radiobutton(master=self, text="Euler Modificado",background='#212946',
                                                  foreground='#00ff41', activebackground='#212946',
                                                  activeforeground='#00ff41', selectcolor='#212946',
                                                  value="EM", variable=self.var_metodo)
        self.radio_euler_modificado.pack(expand=True, fill='both')

        self.radio_runge_kutta2 = Radiobutton(master=self, text="Runge Kutta 2", background='#212946',
                                              foreground='#00ff41', activebackground='#212946',
                                              activeforeground='#00ff41', selectcolor='#212946',
                                              value="RK2", variable=self.var_metodo)
        self.radio_runge_kutta2.pack(expand=True, fill='both')

        self.radio_runge_kutta4 = Radiobutton(master=self, text="Runge Kutta 4", background='#212946',
                                              foreground='#00ff41', activebackground='#212946',
                                              activeforeground='#00ff41', selectcolor='#212946',
                                              value="RK4", variable=self.var_metodo)
        self.radio_runge_kutta4.pack(expand=True, fill='both')
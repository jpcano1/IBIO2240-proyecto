from tkinter import *
import numpy as np

class PanelPuntos(Frame):

    def __init__(self, pInterfaz):
        super(PanelPuntos, self).__init__(master=pInterfaz)
        self.interfaz = pInterfaz
        self.configure(background='#212946')

        # labels
        label_list = ["P", "Q", "R", "S", "T"]

        self.variables_a = np.array([BooleanVar(self) for i in range(len(label_list))])
        self.variables_b = np.array([BooleanVar(self) for i in range(len(label_list))])

        for i in range(len(label_list)):
            Label(self, text=label_list[i],background='#212946',foreground='#08F7FE').grid(row=0, column=(i+1))
            Checkbutton(self, variable=self.variables_a[i],background='#212946',
                                              foreground='#00ff41', activebackground='#212946',
                                              activeforeground='#00ff41', selectcolor='#212946',).grid(row=1, column=(i+1))
            Checkbutton(self, variable=self.variables_b[i],background='#212946',
                                              foreground='#00ff41', activebackground='#212946',
                                              activeforeground='#00ff41', selectcolor='#212946',).grid(row=2, column=(i+1))
        Label(self, text="a_i",background='#212946', foreground='#FE53BB').grid(row=1, column=0)
        Label(self, text="b_i",background='#212946', foreground='#FE53BB').grid(row=2, column=0)
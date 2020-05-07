from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PanelSenales(Frame):

    def __init__(self, pInterfaz):
        super(PanelSenales, self).__init__(master=pInterfaz, highlightbackground="black", highlightcolor="black",
                         highlightthickness=3)
        self.interfaz = pInterfaz

        # Título
        self.title = Label(master=self, text="Señal de ECG")
        self.title.pack()

        # Canvas Plot
        self.plot_canvas()

        # HR
        self.button_hr = Button(master=self, text="Hallar HR")
        self.button_hr.pack(side=LEFT)

        self.text_hr = Entry(master=self)
        self.text_hr.pack(side=RIGHT)

    def plot_canvas(self):
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        x = np.linspace(0, 2*np.pi, 1000)
        ax.plot(x, np.cos(x))
        canvas = FigureCanvasTkAgg(figure=fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

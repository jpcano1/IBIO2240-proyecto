from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PanelSenales(Frame):

    def __init__(self, pInterfaz):
        super(PanelSenales, self).__init__(master=pInterfaz, highlightbackground="black", highlightcolor="black",
                         highlightthickness=3)
        self.plot_canvas()

    def plot_canvas(self):
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        x = np.linspace(0, 2*np.pi, 1000)
        ax.plot(x, np.cos(x))
        canvas = FigureCanvasTkAgg(figure=fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

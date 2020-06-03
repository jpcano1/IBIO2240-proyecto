from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

class PanelSenales(Frame):

    def __init__(self, pInterfaz):
        super(PanelSenales, self).__init__(master=pInterfaz, highlightbackground="black", highlightcolor="black",
                         highlightthickness=3)
        self.interfaz = pInterfaz
        self.configure(background='#212946')
        self.ax=None
        self.canvas=None
        # Título
        self.title = Label(master=self, text="Señal de ECG",background='#212946',foreground='#08F7FE',font=("Helvetica", 16))
        self.title.pack()
        # Canvas Plot
        x,y=self.interfaz.getXY()

        self.plot_canvas(x,y,True)

        # HR
        self.text_hr = Entry(master=self,background='#212946',foreground='#dad0c0',insertbackground='#dad0c0')
        self.text_hr.pack()

        self.button_hr = Button(master=self, text="Hallar HR",background='#F5D300', foreground="#212946", font=('calibri', 12, 'bold'),borderwidth='4')
        self.button_hr.pack()

    def plot_canvas(self,x,y,create=False):
        if(not create):
            self.ax.clear()
            self.canvas.get_tk_widget().destroy()
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey
        colors = [
            '#08F7FE',  # teal/cyan
            '#00ff41',  # matrix green
        ]

        df = pd.DataFrame({'y':y})
        fig, self.ax = plt.subplots()
        self.ax.plot(x, y, color=colors[0], linewidth=1.4)

        # Redraw the data with low alpha and slighty increased linewidth:
        n_shades = 10
        diff_linewidth = 0.5
        alpha_value = 0.3 / n_shades
        for n in range(1, n_shades + 1):
            self.ax.plot(x, y, linewidth=2 + (diff_linewidth * n),
                    alpha=alpha_value,
                    color=colors[0])

        # Color the areas below the lines:
        for column, color in zip(df, colors):
            self.ax.fill_between(x=x,
                    y1=df[column].values,
                    y2=[0] * len(df),
                    color=color,
                    alpha=0.1)

        self.ax.grid(color='#2A3459',linewidth=1.5, linestyle="--")

        self.ax.set_xlim(min(x), max(x))  # to not have the markers cut off
        plt.close()
        self.canvas = FigureCanvasTkAgg(figure=fig, master=self)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()


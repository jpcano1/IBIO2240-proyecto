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

        # Título
        self.title = Label(master=self, text="Señal de ECG",background='#212946',foreground='#08F7FE',font=("Helvetica", 16))
        self.title.pack()
        # Canvas Plot
        x,y=self.interfaz.getXY()

        self.plot_canvas(x,y)

        # HR
        self.text_hr = Entry(master=self,background='#212946',foreground='#dad0c0',insertbackground='#dad0c0')
        self.text_hr.pack()

        self.button_hr = Button(master=self, text="Hallar HR",background='#F5D300', foreground="#212946", font=('calibri', 12, 'bold'),borderwidth='4')
        self.button_hr.pack()

    def plot_canvas(self,x,y):
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey
        colors = [
            '#FE53BB',  # pink
            '#08F7FE',  # teal/cyan
            '#F5D300',  # yellow
            '#00ff41',  # matrix green
        ]

        df = pd.DataFrame({'y':y})
        fig, ax = plt.subplots()
        df.plot( color=colors, ax=ax,linewidth=3)

        # Redraw the data with low alpha and slighty increased linewidth:
        n_shades = 10
        diff_linewidth = 1.05
        alpha_value = 0.3 / n_shades
        for n in range(1, n_shades + 1):
            df.plot(
                    linewidth=2 + (diff_linewidth * n),
                    alpha=alpha_value,
                    legend=False,
                    ax=ax,
                    color=colors)

        # Color the areas below the lines:
        for column, color in zip(df, colors):
            ax.fill_between(x=x,
                    y1=df[column].values,
                    y2=[0] * len(df),
                    color=color,
                    alpha=0.1)

        ax.grid(color='#2A3459',linewidth=1.5)

        ax.set_xlim(0,1000)  # to not have the markers cut off
        ax.set_ylim(min(y),max(y))
        canvas = FigureCanvasTkAgg(figure=fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

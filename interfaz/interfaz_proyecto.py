from tkinter import *
from interfaz.panel_parametros import PanelParametros
from interfaz.panel_metodos import PanelMetodos
from interfaz.panel_opciones import PanelOpciones
from interfaz.panel_senales import PanelSenales
from interfaz.panel_puntos import PanelPuntos
from mundo.ecg_generator import ECGGenerator
from PIL import ImageTk ,Image
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd

class InterfazProyecto(Tk):

    def __init__(self, name="Interfaz"):
        super(InterfazProyecto, self).__init__(className=name)
        self.geometry("1100x760")

        Style = ttk.Style()  # Objeto para crear estilos  # https://kite.com/python/docs/ttk.Style
        Style.configure('2.TButton', font=('Times', 15, 'bold', 'underline',), background="#212946",foreground='red',height=5, width=3)

        Style.map("2.TButton",
                  foreground=[('pressed', 'red'), ('active', 'red')],
                  background=[('pressed', '!disabled', '#212946'), ('active', '#212946')])

        self.configure(background='#212946')
        self.ecg=ECGGenerator()

        self.panel_parametros = PanelParametros(self) #Bien
        self.panel_parametros.place(x=700, y=200)
        self.panel_parametros.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_metodos = PanelMetodos(self) #Bien
        self.panel_metodos.place(x=700, y=410)
        self.panel_metodos.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_opciones = PanelOpciones(self)
        self.panel_opciones.place(x=250, y=10)
        self.panel_opciones.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_senales = PanelSenales(self)
        self.panel_senales.place(x=30, y=70)
        self.panel_senales.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_puntos = PanelPuntos(self)
        self.panel_puntos.place(x=250, y=675)
        self.panel_puntos.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        #Imágenes
        self.img=Image.open("../data/img/images.jpg")
        self.img=self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        self.lab = Label(image=self.img,borderwidth=0)
        self.lab.place(x=800, y=40)

        self.img2=Image.open("../data/img/lapiz.png")
        self.img2=self.img2.resize((50, 50))
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.lab2 = Label(image=self.img2,borderwidth=0)
        self.lab2.place(x=150, y=680)

        self.img3=Image.open("../data/img/heart.jpg")
        self.img3=self.img3.resize((100, 90))
        self.img3 = ImageTk.PhotoImage(self.img3)
        self.lab3 = Label(image=self.img3,borderwidth=0)
        self.lab3.place(x=130, y=100)

        Boton2 = ttk.Button(master=self, text="X", style="2.TButton", command=self.CerrarAplicacion).place(x=0, y=0)

    '''Se definen todas las funciones requeridas'''

    def CerrarAplicacion(self):
        self.MsgBox = tk.messagebox.askquestion('Cerrar Aplicación', '¿Está seguro que desea cerrar la aplicación?',icon='warning')
        if self.MsgBox == 'yes':
            self.destroy()
        else:
            tk.messagebox.showinfo('Retornar', 'Será retornado a la aplicación')

    def CerrarAplicacion2(self):
        self.destroy()

    def updatePoints(self):
        return self.ecg.a_i,self.ecg.b_i

    def save(self):
        self.ecg.save_points()

    def load(self):
        self.ecg.load_points()
        self.panel_puntos.updateMe()
        self.panel_parametros.updateMe(self.ecg.hr_mean,self.ecg.fs,self.ecg.noise,self.ecg.num_latidos)

    def darHR(self):
        x,y=self.ecg.heart_rate()
        #self.panel_senales.pintar_aparte(x,self.ecg.points[y])
        window=tk.Toplevel(self)
        window.configure(background='#212946')
        title = Label(master=window, text="HR", background='#212946', foreground='#08F7FE',
                      font=('calibri', 16, 'bold'))
        title.pack()
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey
        colors = [
            '#00ff41',  # matrix green
            '#08F7FE',  # teal/cyan
        ]
        df = pd.DataFrame({'y': self.ecg.points[y]})
        fig, ax = plt.subplots()
        ax.plot(x, self.ecg.points[y], color=colors[0], linewidth=1.4,marker='s')

        # Redraw the data with low alpha and slighty increased linewidth:
        n_shades = 10
        diff_linewidth = 0.5
        alpha_value = 0.3 / n_shades
        for n in range(1, n_shades + 1):
            ax.plot(x, self.ecg.points[y], linewidth=2 + (diff_linewidth * n),
                         alpha=alpha_value,
                         color=colors[0])

        # Color the areas below the lines:
        for column, color in zip(df, colors):
            ax.fill_between(x=x,
                                 y1=df[column].values,
                                 y2=[0] * len(df),
                                 color=color,
                                 alpha=0.1)

        ax.grid(color='#2A3459', linewidth=1.5, linestyle="--")
        ax.set_xlim(min(x), max(x))  # to not have the markers cut off
        canvas = FigureCanvasTkAgg(figure=fig, master=window)
        canvas.get_tk_widget().pack()
        canvas.draw()
        return len(y)

    def plot(self):
        fcardiaca=self.panel_parametros.frecuencia_input.get()
        fmuestreo=self.panel_parametros.frecuencia_muestreo_input.get()
        fruido=self.panel_parametros.factor_ruido_input.get()
        latidos=self.panel_parametros.latidos_input.get()
        newa = []
        newa.append(float(self.panel_puntos.p_a.get()))
        newa.append(float(self.panel_puntos.q_a.get()))
        newa.append(float(self.panel_puntos.r_a.get()))
        newa.append(float(self.panel_puntos.s_a.get()))
        newa.append(float(self.panel_puntos.t_a.get()))

        newb=[]
        newb.append(float(self.panel_puntos.p_b.get()))
        newb.append(float(self.panel_puntos.q_b.get()))
        newb.append(float(self.panel_puntos.r_b.get()))
        newb.append(float(self.panel_puntos.s_b.get()))
        newb.append(float(self.panel_puntos.t_b.get()))

        self.ecg.a_i = newa
        self.ecg.b_i = newb

        if fcardiaca != "":
            self.ecg.hr_mean = float(fcardiaca)
        if fmuestreo != "":
            self.ecg.fs = float(fmuestreo)
        if fruido != "":
            self.ecg.noise = float(fruido)
        if latidos != "":
            self.ecg.num_latidos = float(latidos)

        if self.panel_metodos.getSelected() == "EA":
            self.ecg.euler_forward(t_f=self.ecg.num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval,self.ecg.points)
        elif self.panel_metodos.getSelected()== "EAT":
            self.ecg.euler_backward(t_f=self.ecg.num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval,self.ecg.points)
        elif self.panel_metodos.getSelected() == "EM":
            self.ecg.euler_modificado(t_f=self.ecg.num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval, self.ecg.points)
        elif self.panel_metodos.getSelected() == "RK2":
            self.ecg.rk2(t_f=self.ecg.num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval, self.ecg.points)
        else:
            self.ecg.rk4(t_f=self.ecg.num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval, self.ecg.points)

    def getXY(self):
        return self.ecg.interval,self.ecg.points

if __name__ == '__main__':
    interfaz = InterfazProyecto(" ECG Monitor")
    interfaz.mainloop()

from tkinter import *
import tkinter.ttk as ttk
class PanelParametros(Frame):

    def __init__(self, pInterfaz):
        super(PanelParametros, self).__init__(master=pInterfaz, highlightbackground="black",
                                              highlightcolor="black", highlightthickness=3)
        self.interfaz = pInterfaz
        self.configure(background='#212946')

        style_titles=ttk.Style()
        style_titles.configure('titulos.Label',background='#212946', foreground='#08F7FE')

        style_subtitles = ttk.Style()
        style_subtitles.configure('subtitulos.Label', background='#212946', foreground='#FE53BB')

        # Titulo
        ttk.Label(master=self, text="Parámetros",style='titulos.Label').grid(row=0, column=0)

        # Labels Parametros
        ttk.Label(master=self, text="Frecuencia Cardíaca",style='subtitulos.Label').grid(row=1, column=0)

        ttk.Label(master=self, text="# de latidos",style='subtitulos.Label').grid(row=2, column=0)

        ttk.Label(master=self, text="Frecuencia Muestreo",style='subtitulos.Label').grid(row=3, column=0)

        ttk.Label(master=self, text="Factor de Ruido",style='subtitulos.Label').grid(row=4, column=0)

        # Input Parametros
        self.frecuencia_input = Entry(master=self, background='#212946',foreground='#dad0c0',insertbackground='#dad0c0')
        self.frecuencia_input.grid(row=1, column=1)

        self.latidos_input = Entry(master=self, background='#212946',foreground='#dad0c0',insertbackground='#dad0c0')
        self.latidos_input.grid(row=2, column=1)

        self.frecuencia_muestreo_input = Entry(master=self, background='#212946',foreground='#dad0c0',insertbackground='#dad0c0')
        self.frecuencia_muestreo_input.grid(row=3, column=1)

        self.factor_ruido_input = Entry(master=self, background='#212946',foreground='#dad0c0',insertbackground='#dad0c0')
        self.factor_ruido_input.grid(row=4, column=1)
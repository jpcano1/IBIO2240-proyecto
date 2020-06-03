from tkinter import *
from interfaz.panel_parametros import PanelParametros
from interfaz.panel_metodos import PanelMetodos
from interfaz.panel_opciones import PanelOpciones
from interfaz.panel_senales import PanelSenales
from interfaz.panel_puntos import PanelPuntos
from mundo.ecg_generator import ECGGenerator
from PIL import ImageTk ,Image

class InterfazProyecto(Tk):

    def __init__(self, name="Interfaz"):
        super(InterfazProyecto, self).__init__(className=name)

        self.configure(background='#212946')
        self.ecg=ECGGenerator()

        self.panel_parametros = PanelParametros(self)
        self.panel_parametros.grid(row=0, column=1)
        self.panel_parametros.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_metodos = PanelMetodos(self)
        self.panel_metodos.grid(row=1, column=1)
        self.panel_metodos.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_opciones = PanelOpciones(self)
        self.panel_opciones.grid(row=0, column=0)
        self.panel_opciones.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_senales = PanelSenales(self)
        self.panel_senales.grid(row=1, column=0)
        self.panel_senales.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.panel_puntos = PanelPuntos(self)
        self.panel_puntos.grid(row=2, column=0)
        self.panel_puntos.config(highlightbackground = "#F5D300",highlightcolor="#F5D300")

        self.img=Image.open("../images.jpg")
        self.img=self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        self.lab = Label(image=self.img)
        self.lab.place(x=710, y=480)

    def updatePoints(self):
        return self.ecg.a_i,self.ecg.b_i

    def plot(self):
        fcardiaca=self.panel_parametros.frecuencia_input.get()
        fmuestreo=self.panel_parametros.frecuencia_muestreo_input.get()
        fruido=self.panel_parametros.factor_ruido_input.get()
        latidos=self.panel_parametros.latidos_input.get()

        num_latidos = 10

        if fcardiaca!= "":
            self.ecg.hr_mean = float(fcardiaca)
        if fmuestreo != "":
            self.ecg.fs = float(fmuestreo)
        if fruido != "":
            self.ecg.noise = float(fruido)
        if latidos != "":
            num_latidos = float(latidos)

        if self.panel_metodos.getSelected() == "EA":
            self.ecg.euler_forward(t_f=num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval,self.ecg.points)
        elif self.panel_metodos.getSelected()== "EAT":
            self.ecg.euler_backward(t_f=num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval,self.ecg.points)
        elif self.panel_metodos.getSelected() == "EM":
            #self.ecg.euler_modificado()
            self.panel_senales.plot_canvas(self.ecg.interval, self.ecg.points)
        elif self.panel_metodos.getSelected() == "RK2":
            self.ecg.rk2(t_f=num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval, self.ecg.points)
        else:
            self.ecg.rk4(t_f=num_latidos)
            self.panel_senales.plot_canvas(self.ecg.interval, self.ecg.points)

    def getXY(self):
        return self.ecg.interval,self.ecg.points

if __name__ == '__main__':
    interfaz = InterfazProyecto(" ECG Monitor")
    interfaz.mainloop()

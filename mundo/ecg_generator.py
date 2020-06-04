import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import find_peaks

import struct as st

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

class ECGGenerator:

    def __init__(self, fs=1., hr_mean=60., hr_std=1., noise=0.):
        """
        Inicializa el electrocardiograma con valores predeterminados
        :param fs: Frecuencia de muestreo
        :param hr_mean: Promedio de frecuencia cardíaca
        :param hr_std: Desviación estándar de la frecuencia
        cardíaca
        :param noise: Factor de ruido
        """
        # Parámetros de a_i y b_i
        self.a_i = np.array([1.2, -5, 30, -7.5, 0.75])
        self.b_i = np.array([0.25, 0.1, 0.1, 0.1, 0.4])
        self.theta_i = np.array([-1/3, -1/12, 0, 1/12, 0.5]) * np.pi
        self.points = list()
        self.interval = list()
        # Parámetros
        self.fs = fs
        self.hr_mean = hr_mean
        self.hr_std = hr_std
        self.noise = noise
        self.num_latidos = 10

        # Inicializa con Euler Forward
        self.euler_forward()

    def w_t(self, t):
        """
        Calcula el período basado en la media
        y las desviación de la frecuencia cardíaca
        :param t: El vector con los tiempos
        :return: El vector de períodos
        """
        rr_mean = 60 / self.hr_mean
        rr_std = 60 * self.hr_std / self.hr_mean**2
        return rr_mean + np.random.randn(len(t)) * rr_std

    @staticmethod
    def x_dot(x, y, trr):
        """
        Ecuación diferencial de x
        :param x: Parámetro x
        :param y: Parámetro y
        :param trr: período
        """
        alpha = 1 - np.sqrt(x ** 2 + y ** 2)
        return alpha * x - (2. * np.pi / trr) * y

    @staticmethod
    def y_dot(x, y, trr):
        """
        Ecuación diferencial de y
        :param x: Parámetroo x
        :param y: Parámetro y
        :param trr: Período
        """
        alpha = 1 - np.sqrt(x ** 2 + y ** 2)
        return alpha * y + (2 * np.pi / trr) * x

    def z_dot(self, x, y, z, t):
        """
        Ecuación diferencial de z
        :param x: Parámetro x
        :param y: Parámetro y
        :param z: Parámetro z
        :param t: Vector con los tiempos
        """
        theta = np.arctan2(y, x)
        A = 1.5 * 10 ** (-4)
        delta_i = np.fmod(theta - self.theta_i, 2 * np.pi)
        zbase = A * np.sin(2 * np.pi * 0.25 * t)
        result = -sum(self.a_i * delta_i * np.exp(-0.5 * (delta_i / self.b_i) ** 2)) - (z - zbase)
        return result

    def euler_forward(self, h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
        """
        Algoritmo que soluciona ecuaciones diferenciales
        por el método de euler hacia adelante
        :param h: el avance
        :param x_0: Parámetro x inicial
        :param y_0: Parámetro y inicial
        :param z_0: Parámetro z inicial
        :param t_0: Tiempo inicial
        :param t_f: Tiempo final
        :return: Un vector con los puntos de la solución
        """
        T = np.arange(t_0, t_f + h, h)
        x_euler = np.zeros(len(T))
        Ws = self.w_t(T)
        y_euler = np.zeros(len(T))
        z_euler = np.zeros(len(T))
        x_euler[0] = x_0; y_euler[0] = y_0; z_euler[0] = z_0
        for i in range(1, len(T)):
            x_euler[i] = x_euler[i - 1] + h * self.x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
            y_euler[i] = y_euler[i - 1] + h * self.y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
            z_euler[i] = z_euler[i - 1] + h * self.z_dot(x_euler[i - 1], y_euler[i - 1], z_euler[i - 1], T[i - 1])

        rango = np.arange(len(T)) / self.fs
        self.interval = rango; self.points = self.noise_factor(z_euler)
        return

    def euler_modificado(self,h=0.01, x_0=1., y_0=0., z_0=0.04, t_0=0., t_f=10.):
        T = np.arange(t_0, t_f + h, h)
        x_euler = np.zeros(len(T))
        Ws = self.w_t(T)
        y_euler = np.zeros(len(T))
        z_euler = np.zeros(len(T))
        x_euler[0] = x_0
        y_euler[0] = y_0
        z_euler[0] = z_0
        for i in range(1, len(T)):
            x_euler[i] = x_euler[i - 1] + (h / 2.0) * (
                        self.x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1]) + self.x_dot(x_euler[i - 1], y_euler[i - 1],
                                                                                 Ws[i - 1]))
            y_euler[i] = y_euler[i - 1] + (h / 2.0) * (
                        self.y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1]) + self.y_dot(x_euler[i - 1], y_euler[i - 1],
                                                                                 Ws[i - 1]))
            z_euler[i] = z_euler[i - 1] + (h / 2.0) * (self.z_dot(x_euler[i], y_euler[i], z_euler[i], T[i]) + self.z_dot(
                x_euler[i - 1], y_euler[i - 1], z_euler[i - 1], T[i - 1]))
        rango = np.arange(len(T)) / self.fs
        self.interval = rango; self.points = self.noise_factor(z_euler)
        return

    def euler_backward(self, h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
        """
        Algoritmo que soluciona ecuaciones diferenciales
        por el método de euler hacia atrás
        :param h: el avance
        :param x_0: Parámetro x inicial
        :param y_0: Parámetro y inicial
        :param z_0: Parámetro z inicial
        :param t_0: Tiempo inicial
        :param t_f: Tiempo final
        :return: Un vector con los puntos de la solución
        """
        T = np.arange(t_0, t_f + h, h)
        x_euler = np.zeros(len(T))
        Ws = self.w_t(T)
        y_euler = np.zeros(len(T))
        z_euler = np.zeros(len(T))
        x_euler[0] = x_0;
        y_euler[0] = y_0;
        z_euler[0] = z_0
        for i in range(1, len(T)):
            x_euler[i] = x_euler[i - 1] + h * self.x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
            y_euler[i] = y_euler[i - 1] + h * self.y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
            z_euler[i] = z_euler[i - 1] + h * self.z_dot(x_euler[i], y_euler[i], z_euler[i], T[i])

        rango = np.arange(len(T)) / self.fs
        self.interval = rango; self.points = self.noise_factor(z_euler)
        return

    def rk2(self, h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
        """
        Algoritmo que soluciona ecuaciones diferenciales
        por el método de Runge-Kutta de segundo orden
        :param h: el avance
        :param x_0: Parámetro x inicial
        :param y_0: Parámetro y inicial
        :param z_0: Parámetro z inicial
        :param t_0: Tiempo inicial
        :param t_f: Tiempo final
        :return: Un vector con los puntos de la solución
        """
        T = np.arange(t_0, t_f + h, h)
        x_rk2 = np.zeros(len(T))
        y_rk2 = np.zeros(len(T))
        z_rk2 = np.zeros(len(T))
        Ws = self.w_t(T)
        x_rk2[0] = x_0
        y_rk2[0] = y_0
        z_rk2[0] = z_0
        for i in range(1, len(T)):
            x_k1 = self.x_dot(x_rk2[i - 1], y_rk2[i - 1], Ws[i - 1])
            y_k1 = self.y_dot(x_rk2[i - 1], y_rk2[i - 1], Ws[i - 1])
            z_k1 = self.z_dot(x_rk2[i - 1], y_rk2[i - 1], z_rk2[i - 1], Ws[i - 1])

            x_k2 = self.x_dot(x_rk2[i - 1] + x_k1 * h, y_rk2[i - 1] + y_k1 * h,
                         Ws[i - 1] + h)
            y_k2 = self.y_dot(x_rk2[i - 1] + x_k1 * h, y_rk2[i - 1] + y_k1 * h,
                         Ws[i - 1] + h)
            z_k2 = self.z_dot(x_rk2[i - 1] + x_k1 * h, y_rk2[i - 1] + y_k1 * h,
                         z_rk2[i - 1] + z_k1 * h, Ws[i - 1] + h)

            x_rk2[i] = x_rk2[i - 1] + (h / 2.) * (x_k1 + x_k2)
            y_rk2[i] = y_rk2[i - 1] + (h / 2.) * (y_k1 + y_k2)
            z_rk2[i] = z_rk2[i - 1] + (h / 2.) * (z_k1 + z_k2)
        rango = np.arange(len(T)) / self.fs
        self.interval = rango; self.points = self.noise_factor(z_rk2)
        return

    def rk4(self, h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
        """
        Algoritmo que soluciona ecuaciones diferenciales
        por el método de Runge-Kutta de cuarto orden
        :param h: el avance
        :param x_0: Parámetro x inicial
        :param y_0: Parámetro y inicial
        :param z_0: Parámetro z inicial
        :param t_0: Tiempo inicial
        :param t_f: Tiempo final
        :return: Un vector con los puntos de la solución
        """
        T = np.arange(t_0, t_f + h, h)
        x_rk4 = np.zeros(len(T))
        y_rk4 = np.zeros(len(T))
        z_rk4 = np.zeros(len(T))
        Ws = self.w_t(T)
        x_rk4[0] = x_0
        y_rk4[0] = y_0
        z_rk4[0] = z_0
        for i in range(1, len(T)):
            x_k1 = self.x_dot(x_rk4[i - 1], y_rk4[i - 1], Ws[i - 1])
            y_k1 = self.y_dot(x_rk4[i - 1], y_rk4[i - 1], Ws[i - 1])
            z_k1 = self.z_dot(x_rk4[i - 1], y_rk4[i - 1], z_rk4[i - 1], Ws[i - 1])

            x_k2 = self.x_dot(x_rk4[i - 1] + 0.5 * x_k1 * h,
                              y_rk4[i - 1] + 0.5 * y_k1 * h,
                              Ws[i - 1] + 0.5 * h)
            y_k2 = self.y_dot(x_rk4[i - 1] + 0.5 * x_k1 * h,
                              y_rk4[i - 1] + 0.5 * y_k1 * h,
                              Ws[i - 1] + 0.5 * h)
            z_k2 = self.z_dot(x_rk4[i - 1] + 0.5 * x_k1 * h,
                              y_rk4[i - 1] + 0.5 * y_k1 * h,
                              z_rk4[i - 1] + 0.5 * z_k1 * h,
                              Ws[i - 1] + 0.5 * h)

            x_k3 = self.x_dot(x_rk4[i - 1] + 0.5 * x_k2 * h,
                              y_rk4[i - 1] + 0.5 * y_k2 * h,
                              Ws[i - 1] + 0.5 * h)
            y_k3 = self.y_dot(x_rk4[i - 1] + 0.5 * x_k2 * h,
                              y_rk4[i - 1] + 0.5 * y_k2 * h,
                              Ws[i - 1] + 0.5 * h)
            z_k3 = self.z_dot(x_rk4[i - 1] + 0.5 * x_k2 * h,
                              y_rk4[i - 1] + 0.5 * y_k2 * h,
                              z_rk4[i - 1] + 0.5 * z_k2 * h,
                              Ws[i - 1] + 0.5 * h)

            x_k4 = self.x_dot(x_rk4[i - 1] + 0.5 * x_k3 * h,
                              y_rk4[i - 1] + 0.5 * y_k3 * h,
                              Ws[i - 1] + 0.5 * h)
            y_k4 = self.y_dot(x_rk4[i - 1] + 0.5 * x_k3 * h,
                              y_rk4[i - 1] + 0.5 * y_k3 * h,
                              Ws[i - 1] + 0.5 * h)
            z_k4 = self.z_dot(x_rk4[i - 1] + 0.5 * x_k3 * h,
                              y_rk4[i - 1] + 0.5 * y_k3 * h,
                              z_rk4[i - 1] + 0.5 * z_k3 * h,
                              Ws[i - 1] + 0.5 * h)

            x_rk4[i] = x_rk4[i - 1] + (h / 6.0) * (x_k1 + 2.0 * x_k2 + 2.0 * x_k3 + x_k4)
            y_rk4[i] = y_rk4[i - 1] + (h / 6.0) * (y_k1 + 2.0 * y_k2 + 2.0 * y_k3 + y_k4)
            z_rk4[i] = z_rk4[i - 1] + (h / 6.0) * (z_k1 + 2.0 * z_k2 + 2.0 * z_k3 + z_k4)

        rango = np.arange(len(T)) / self.fs
        self.interval = rango; self.points = z_rk4
        return

    def save_points(self, points_path="../data/points.bin", interval_path="../data/interval.bin", params_path="../data/params.txt"):
        """
        Salva los puntos de la gráfica al igual que el
        rango donde se evalúa
        :param points_path: Ruta del archivo de puntos
        :param interval_path: Ruta del archivo del intervalo
        :param params_path: Ruta del archivo del parámetros
        """
        file = open(points_path, "wb")
        var1 = st.pack("d"*int(len(self.points)), *self.points)
        file.write(var1)
        file.close()
        file = open(interval_path, "wb")
        var1 = st.pack("d"*int(len(self.interval)), *self.interval)
        file.write(var1)
        file.close()
        file = open(params_path,"w")

        file.write("Frecuencia de muestreo:"+str(self.fs)+"\n")
        file.write("Frecuencia cardiaca media:"+str(self.hr_mean)+"\n")
        file.write("Desv est frecuencia cardiaca:"+str(self.hr_std)+"\n")#Validar
        file.write("Factor de ruido:"+str(self.noise)+"\n")#Validad
        file.write("# de latidos:"+str(self.num_latidos)+"\n")
        file.write("a_i:")
        for i in self.a_i:
            file.write(str(i)+",")
        file.write("\n")

        file.write("b_i:")
        for i in self.b_i:
            file.write(str(i) + ",")
        file.write("\n")

        file.write("theta_i:")
        for i in self.theta_i:
            file.write(str(i) + ",")
        file.write("\n")
        file.close()
        return

    def load_points(self, points_path="../data/points.bin", interval_path="../data/interval.bin", params_path="../data/params.txt"):
        """
        Carga los puntos de la gráfica, al igual que
        su rango de evaluación
        :param points_path: Ruta del archivo de puntos
        :param interval_path: Ruta del archivo del intervalo
        :except FileNotFoundError: Excepción generada si el archivo
        no existe
        """
        try:
            file = open(points_path, "rb")
            var1 = file.read()
            self.points = st.unpack("d"*int(len(var1)/8), var1)
            file.close()
            file = open(interval_path, "rb")
            var1 = file.read()
            self.interval = st.unpack("d" * int(len(var1) / 8), var1)
            file.close()

            file = open(params_path, "r")
            self.fs = float(file.readline().split(":")[1].replace("\n",""))
            self.hr_mean = float(file.readline().split(":")[1].replace("\n",""))
            self.hr_std = float(file.readline().split(":")[1].replace("\n",""))
            self.noise = float(file.readline().split(":")[1].replace("\n",""))
            self.num_latidos = float(file.readline().split(":")[1].replace("\n",""))
            self.a_i=[float(x) for x in file.readline().split(":")[1].replace(",\n","").split(",")]
            self.b_i=[float(x) for x in file.readline().split(":")[1].replace(",\n","").split(",")]
            self.theta_i=[float(x) for x in file.readline().split(":")[1].replace(",\n","").split(",")]
            file.close()
        except FileNotFoundError as e:
            raise e

    def heart_rate(self):
        peaks, _ = find_peaks(self.points, height=0.75)
        interval = peaks / self.fs
        return interval, peaks

    def noise_factor(self, points):
        z = np.array(points)
        z_min = np.min(z)
        z_max = np.max(z)
        z_range = z_max - z_min
        z = (z - z_min) * 1.6 / z_range - 0.4

        eta = 2 * np.random.rand(len(z)) - 1
        s = z + self.noise * eta
        return s

# ecg = ECGGenerator(fs=1, noise=0)
# plt.plot(ecg.interval, ecg.points, label="Euler Forward")
# plt.legend(loc="best")
# plt.grid(linestyle="--")
# plt.show()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import struct as st

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

class ECGGenerator:

    def __init__(self):
        self.a_i = np.array([1.2, -5, 30, -7.5, 0.75])
        self.b_i = np.array([0.25, 0.1, 0.1, 0.1, 0.4])
        self.theta_i = np.array([-1/3, -1/12, 0, 1/12, 0.5]) * np.pi
        self.points = list()
        self.interval = list()
        self.euler_forward()

    @staticmethod
    def w_t(t):
        return np.random.uniform(0.98, 1.1, len(t))

    @staticmethod
    def x_dot(x, y, trr):
        alpha = 1 - np.sqrt(x ** 2 + y ** 2)
        return alpha * x - (2. * np.pi / trr) * y

    @staticmethod
    def y_dot(x, y, trr):
        alpha = 1 - np.sqrt(x ** 2 + y ** 2)
        return alpha * y + (2 * np.pi / trr) * x

    def z_dot(self, x, y, z, t):
        theta = np.arctan2(y, x)

        delta_i = np.fmod(theta - self.theta_i, 2 * np.pi)
        zbase = 0.005 * np.sin(2 * np.pi * 0.25 * t)
        result = -sum(self.a_i * delta_i * np.exp(-0.5 * (delta_i / self.b_i) ** 2)) - (z - zbase)
        return result

    def euler_forward(self, h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
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
        self.interval = T; self.points = z_euler
        return

    def save_points(self, points_path="points.bin", interval_path="interval.bin"):
        file = open(points_path, "wb")
        var1 = st.pack("d"*int(len(self.points)), *self.points)
        file.write(var1)
        file.close()
        file = open(interval_path, "wb")
        var1 = st.pack("d"*int(len(self.interval)), *self.interval)
        file.write(var1)
        file.close()
        return

    def load_points(self, points_path="points.bin", interval_path="interval.bin"):
        try:
            file = open(points_path, "rb")
            var1 = file.read()
            self.points = st.unpack("d"*int(len(var1)/8), var1)
            file.close()
            file = open(interval_path, "rb")
            var1 = file.read()
            self.interval = st.unpack("d" * int(len(var1) / 8), var1)
            file.close()
        except FileNotFoundError as e:
            raise e
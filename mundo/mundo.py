import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

def w_t(t):
    return 1 / np.random.uniform(58, 62, len(t))

def x_dot(x, y, trr):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha * x - (2. * np.pi / trr) * y

def y_dot(x, y, trr):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha * y + (2 * np.pi / trr) * x

def z_dot(x, y, z, t):
    theta = np.arctan2(y, x)
    result = 0
    args = ["P", "Q", "R", "S", "T"]
    for arg in args:
        a_i = parametros.loc["a_i", arg]; b_i = parametros.loc["b_i", arg]
        theta_i = parametros.loc["Theta_i", arg]
        delta_theta_i = math.fmod(theta - theta_i, 2 * np.pi)
        result += a_i * delta_theta_i * np.exp(-(delta_theta_i**2 / (2 * b_i**2)))
    return  - result - (z - z0(t))

def z0(t):
    A = 0.15
    return A * np.sin(2 * np.pi* 0.25 * t)

def euler_for(h=0.01, x_0=1, y_0=0, z_0=0, t_0=0, t_f=1):
    T = np.arange(t_0, t_f + h, h)
    x_euler = np.zeros(len(T))
    Ws = w_t(T)
    y_euler = np.zeros(len(T))
    z_euler = np.zeros(len(T))
    x_euler[0] = x_0; y_euler[0] = y_0; z_euler[0] = z_0
    for i in range(1, len(T)):
        x_euler[i] = x_euler[i - 1] + h * x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        y_euler[i] = y_euler[i - 1] + h * y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        z_euler[i] = z_euler[i - 1] + h * z_dot(x_euler[i - 1], y_euler[i - 1], z_euler[i - 1], T[i - 1])
    return T, z_euler

# h = 0.001
# t_0 = 0
# t_f = 1
# T = np.arange(t_0, t_f + h, h)
# x1 = 0; y1 = 1; z1 = 0
# x_euler = np.zeros(len(T))
# Ws = w_t(T)
# y_euler = np.zeros(len(T))
# z_euler = np.zeros(len(T))
# x_euler[0] = x1
# y_euler[0] = y1
# z_euler[0] = z1
#
# for i in range(1, len(T)):
#     x_euler[i] = x_euler[i - 1] + h * x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i-1])
#     y_euler[i] = y_euler[i-1] + h * y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i-1])
#     z_euler[i] = z_euler[i-1] + h * z_dot(x_euler[i - 1], y_euler[i - 1], z_euler[i - 1], T[i - 1])

T, z_euler = euler_for()

plt.plot(T, z_euler)
plt.grid(linestyle="--")
plt.show()

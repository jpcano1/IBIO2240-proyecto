import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

def w_t(t):
    return np.random.uniform(0.98, 1.1, len(t))

def x_dot(x, y, trr):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha * x - (2. * np.pi / trr) * y

def y_dot(x, y, trr):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha * y + (2 * np.pi / trr) * x

def z_dot(x, y, z, t, a_i = parametros.loc["a_i"], b_i = parametros.loc["b_i"], theta_i = parametros.loc["Theta_i"]):
    theta = np.arctan2(y, x)
    A = 1.5 * 10 ** (-4)
    delta_i = np.fmod(theta - theta_i, 2 * np.pi)
    zbase = A * np.sin(2 * np.pi * 0.25 * t)
    result = -sum(a_i * delta_i * np.exp(-0.5 * (delta_i / b_i) ** 2)) - (z - zbase)
    return result

def euler_for(h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
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

T, z_euler = euler_for()

plt.plot(T, z_euler)
plt.grid(linestyle="--")
plt.show()

def euler_back(h=0.01, x_0=1, y_0=0, z_0=0, t_0=0, t_f=0.1):
    T = np.arange(t_0, t_f + h, h)
    x_euler = np.zeros(len(T))
    Ws = w_t(T)
    y_euler = np.zeros(len(T))
    z_euler = np.zeros(len(T))
    x_euler[0] = x_0; y_euler[0] = y_0; z_euler[0] = z_0
    for i in range(1, len(T)):
        x_euler[i] = x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        y_euler[i] = y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        z_euler[i] = z_dot(x_euler[i - 1], y_euler[i - 1], z_euler[i - 1], T[i - 1])
    return T, z_euler

# T, z_euler = euler_back()
#
# plt.plot(T, z_euler, "-")
# plt.grid(linestyle="--")
# plt.show()

def euler_mod(h=0.001, x_0=1, y_0=0, z_0=0, t_0=0, t_f=0.1):
    T = np.arange(t_0, t_f + h, h)
    x_euler = np.zeros(len(T))
    Ws = w_t(T)
    y_euler = np.zeros(len(T))
    z_euler = np.zeros(len(T))
    x_euler[0] = x_0
    y_euler[0] = y_0
    z_euler[0] = z_0
    for i in range(1, len(T)):
        x_euler[i] = (x_euler[i - 1] + (h/2.0) * x_dot(x_euler[i - 1], y_euler[i - 1])) / x_dot(x_euler[i], h)
        y_euler[i] = (y_euler[i - 1] + (h/2.0) * y_dot(x_euler[i - 1], y_euler[i - 1])) / y_dot(x_euler[i], h)
        z_euler[i] = (z_euler[i - 1] + (h/2.0) * z_dot(x_euler[i - 1], y_euler[i - 1])) / z_dot(x_euler[i], h)
    return T, z_euler

# T, z_euler = euler_mod()

# plt.plot(T, z_euler)
# plt.grid(linestyle="--")
# plt.show()

def rk2(func, h=0.01, y_0=0.01, t_0=0., t_f=30.):
    T = np.arange(t_0, t_f + h, h)
    y_rk2=np.zeros(len(T))
    y_rk2[0]=y_0
    for i in range(1,len(T)):
        k1=func(T[i - 1], y_rk2[i - 1])
        k2=func(T[i - 1] + h, y_rk2[i - 1] + k1 * h)
        y_rk2=y_rk2[i-1]+(h/2.0)*(k1+k2)

    return T, y_rk2
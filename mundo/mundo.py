import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

def w_t(t):
    return np.random.uniform(0.98, 1.1, len(t))

def x_dot(x, y, trr):
    alpha = 1. - np.sqrt(x**2. + y**2.)
    return alpha * x - (2. * np.pi / trr) * y

def y_dot(x, y, trr):
    alpha = 1. - np.sqrt(x**2. + y**2.)
    return alpha * y + (2. * np.pi / trr) * x

def z_dot(x, y, z, t, a_i = parametros.loc["a_i"], b_i = parametros.loc["b_i"], theta_i = parametros.loc["Theta_i"]):
    theta = np.arctan2(y, x)
    A = 1.5 * 10 ** (-4)
    delta_i = np.fmod(theta - theta_i, 2 * np.pi)
    zbase = A * np.sin(2 * np.pi * 0.25 * t)
    result = -sum(a_i * delta_i * np.exp(-0.5 * (delta_i / b_i) ** 2)) - (z - zbase)
    return result

def euler_back(h=0.01, x_0=1., y_0=0., z_0=0.04, t_0=0., t_f=10.):
    T = np.arange(t_0, t_f + h, h)
    x_euler = np.zeros(len(T))
    Ws = w_t(T)
    y_euler = np.zeros(len(T))
    z_euler = np.zeros(len(T))
    x_euler[0] = x_0; y_euler[0] = y_0; z_euler[0] = z_0
    """y_n=y_n-1+h*f(y_n,t_n)"""
    for i in range(1, len(T)):
        x_euler[i] = x_euler[i - 1] + h * x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])#O WS[i-1]?
        y_euler[i] = y_euler[i - 1] + h * y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        z_euler[i] = z_euler[i - 1] + h * z_dot(x_euler[i], y_euler[i], z_euler[i], T[i])
    return T, z_euler

def euler_for(h=0.01, x_0=1., y_0=0., z_0=0.04, t_0=0., t_f=10.):
    T = np.arange(t_0, t_f + h, h)
    x_euler = np.zeros(len(T))
    Ws = w_t(T)
    y_euler = np.zeros(len(T))
    z_euler = np.zeros(len(T))
    x_euler[0] = x_0; y_euler[0] = y_0; z_euler[0] = z_0
    for i in range(1, len(T)):
        """y_n=y_n-1+h*f(y_n-1,t_n-1)""" #MELO
        x_euler[i] = x_euler[i - 1] + h * x_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        y_euler[i] = y_euler[i - 1] + h * y_dot(x_euler[i - 1], y_euler[i - 1], Ws[i - 1])
        z_euler[i] = z_euler[i - 1] + h * z_dot(x_euler[i - 1], y_euler[i - 1], z_euler[i - 1], T[i - 1])
    return T, z_euler

# T, z_euler = euler_back()
# plt.plot(T, z_euler, "-", label="Backward")
# plt.grid(linestyle="--")
# plt.title("BACKWARD")
# plt.show()

# T2, z_euler2 = euler_for()
# print(T-T2,z_euler-z_euler2)

# plt.title("FORWARD")
# plt.plot(T, z_euler, "-", label="Forward")
# plt.grid(linestyle="--")
# plt.legend(loc="best")
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

def rk2(h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
    T = np.arange(t_0, t_f + h, h)
    x_rk2 = np.zeros(len(T))
    y_rk2 = np.zeros(len(T))
    z_rk2 = np.zeros(len(T))
    Ws = w_t(T)
    x_rk2[0] = x_0
    y_rk2[0] = y_0
    z_rk2[0] = z_0
    for i in range(1, len(T)):
        x_k1 = x_dot(x_rk2[i-1], y_rk2[i-1], Ws[i-1])
        y_k1 = y_dot(x_rk2[i-1], y_rk2[i-1], Ws[i-1])
        z_k1 = z_dot(x_rk2[i-1], y_rk2[i-1], z_rk2[i-1], Ws[i-1])

        x_k2 = x_dot(x_rk2[i-1] + x_k1 * h, y_rk2[i-1] + y_k1 * h,
                     Ws[i-1] + h)
        y_k2 = y_dot(x_rk2[i-1] + x_k1 * h, y_rk2[i-1] + y_k1 * h,
                     Ws[i-1] + h)
        z_k2 = z_dot(x_rk2[i-1] + x_k1 * h, y_rk2[i-1] + y_k1 * h,
                     z_rk2[i-1] + z_k1 * h, Ws[i-1] + h)

        x_rk2[i] = x_rk2[i-1] + (h / 2.) * (x_k1 + x_k2)
        y_rk2[i] = y_rk2[i-1] + (h / 2.) * (y_k1 + y_k2)
        z_rk2[i] = z_rk2[i-1] + (h / 2.) * (z_k1 + z_k2)

    return T, z_rk2

# T, z_rk2 = rk2()
#
# plt.plot(T, z_rk2)
# plt.grid(linestyle="--")
# plt.show()

def rk4(h=0.01, x_0=1, y_0=0, z_0=0.04, t_0=0, t_f=10):
    T = np.arange(t_0, t_f + h, h)
    x_rk4 = np.zeros(len(T))
    y_rk4 = np.zeros(len(T))
    z_rk4 = np.zeros(len(T))
    Ws = w_t(T)
    x_rk4[0] = x_0
    y_rk4[0] = y_0
    z_rk4[0] = z_0
    for i in range(1, len(T)):
        x_k1 = x_dot(x_rk4[i-1], y_rk4[i-1], Ws[i-1])
        y_k1 = x_dot(x_rk4[i-1], y_rk4[i-1], Ws[i-1])
        z_k1 = z_dot(x_rk4[i-1], y_rk4[i-1], z_rk4[i-1], Ws[i-1])

        x_k2 = x_dot(x_rk4[i-1] + 0.5 * h, y_rk4[i-1] + 0.5 * y_k1 * h,
                     Ws[i-1] + h)
        y_k2 = y_dot(x_rk4[i-1] + 0.5 * h, y_rk4[i-1] + 0.5 * y_k1 * h,
                     Ws[i-1] + h)
        z_k2 = z_dot(x_rk4[i-1] + 0.5 * h, y_rk4[i-1] + 0.5 * y_k1 * h,
                     z_rk4[i-1] + z_k1 * h, Ws[i-1] + h)

        x_k3 = x_dot(x_rk4[i - 1] + 0.5 * h, y_rk4[i - 1] + 0.5 * y_k2 * h,
                     Ws[i - 1] + h)
        y_k3 = y_dot(x_rk4[i - 1] + 0.5 * h, y_rk4[i - 1] + 0.5 * y_k2 * h,
                     Ws[i - 1] + h)
        z_k3 = z_dot(x_rk4[i - 1] + 0.5 * h, y_rk4[i - 1] + 0.5 * y_k2 * h,
                     z_rk4[i - 1] + z_k2 * h, Ws[i - 1] + h)

        x_k4 = x_dot(x_rk4[i - 1] + h, y_rk4[i - 1] + y_k3 * h,
                     Ws[i - 1] + h)
        y_k4 = y_dot(x_rk4[i - 1] + h, y_rk4[i - 1] + y_k3 * h,
                     Ws[i - 1] + h)
        z_k4 = z_dot(x_rk4[i - 1] + h, y_rk4[i - 1] + y_k3 * h,
                     z_rk4[i - 1] + z_k3 * h, Ws[i - 1] + h)

        x_rk4[i] = x_rk4[i-1] + (h / 6.0) * (x_k1 + 2.0 * x_k2 + 2.0 * x_k3 + x_k4)
        y_rk4[i] = y_rk4[i-1] + (h / 6.0) * (y_k1 + 2.0 * y_k2 + 2.0 * y_k3 + y_k4)
        z_rk4[i] = z_rk4[i-1] + (h / 6.0) * (z_k1 + 2.0 * z_k2 + 2.0 * z_k3 + z_k4)

    return T, z_rk4

# T, z_rk4 = rk4()
#
# plt.plot(T, z_rk4)
# plt.grid(linestyle="--")
# plt.show()
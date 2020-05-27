import numpy as np
import pandas as pd

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

def x_dot(x, y, w):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha*x - w*y

def y_dot(x, y, w):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha*y + w*x

def z_dot(x, y, z, *args):
    theta = np.arctan2(y, x)
    result = 0
    for arg in args:
        a_i = parametros.loc["a_i", arg]; b_i = parametros.loc["b_i", arg]
        theta_i = parametros.loc["Theta_i", arg]; t = parametros.loc["Time", arg]
        delta_theta_i = (theta - theta_i) % 2 * np.pi
        result += a_i * delta_theta_i * np.exp(-(delta_theta_i**2 / (2 * b_i**2))) \
                  - (z - z_0(t))
    return result

def z_0(t):
    """Falta meter la frecuencia"""
    A = 0.15
    return A * np.sin(2 * np.pi * t)
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

def z_dot(x, y):
    theta = np.arctan2(x, y)
    return
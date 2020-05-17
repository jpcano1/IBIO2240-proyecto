import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    return (0.49 - ((0.00245 * np.exp(0.49 * t)) / (0.49 + 0.005 * (np.exp(0.49 * t) - 1)))) * y

def f1_euler_back(t, y, h):
    return y / (1 - h * (0.49 - ((0.00245 * np.exp(0.49 * t)) / (0.49 + 0.005 * (np.exp(0.49 * t) - 1)))))

def f1_euler_mod(t, y):
    return (1 - (h / 2.0) * (0.49 - ((0.00245 * np.exp(0.49 * t)) / (0.49 + 0.005 * (np.exp(0.49 * t) - 1)))))

def euler_forward(func, h=0.01, y_0=0.01, t_0=0., t_f=30.):
    """
    Calcula la solución de una ecuación diferencial a través
    del método de euler hacia adelante
    :param func: La función a la que se hará el cálculo
    :param h: el valor de h
    :param y_0: y inicial
    :param t_0: tiempo inicial
    :param t_f: tiempo final
    :return: valores de euler
    """
    T = np.arange(t_0, t_f + h, h)
    y_euler = np.zeros(len(T))
    y_euler[0] = y_0
    for i in range(1, len(T)):
        # Vamos estimando el valor de Y_i
        y_euler[i] = y_euler[i - 1] + h * func(T[i - 1], y_euler[i - 1])
    return T, y_euler

def euler_backward(func, h=0.01, y_0=0.01, t_0=0., t_f=30.):
    T = np.arange(t_0, t_f + h, h)
    y_euler = np.zeros(len(T))
    y_euler[0] = y_0

    for i in range(1, len(T)):
        y_euler[i] = f1_euler_back(T[i], y_euler[i-1], h)
    return T, y_euler

def euler_modified(func, h=0.01, y_0=0.01, t_0=0., t_f=30.)
    T = np.arange(t_0, t_f + h, h)
    y_euler = np.zeros(len(T))
    y_euler[0] = y_0

    for i in range(1, len(T)):
        y_euler[i] = (y_euler[i - 1] + (h / 2.0) * f1(T[i - 1], y_euler[i - 1])) / \ f1_euler_mod(T[i], h)
        return T, y_euler

def y_analitc(t):
    # Tasa de infeccion
    a = 0.5
    # Tasa de recuperación
    b = 0.01
    # Porcentaje inicial de personas suceptibles
    s_0 = 0.99
    # Porcentaje inicial de pesonas infectadas
    i_0 = 1 - s_0
    # Total de personas
    N = s_0 + i_0

    expr1 = ((a * N-b) * i_0 * np.exp((a*N - b)*t))
    expr2 = ((a * N-b) + a * i_0 * (np.exp((a*N - b)*t)-1))
    return expr1 / expr2

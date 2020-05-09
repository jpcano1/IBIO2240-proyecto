import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    return (0.49 - ((0.00245 * np.exp(0.49 * t)) / (0.49 + 0.005 * (np.exp(0.49 * t))))) * y

def euler_forward(func, h = 0.01, y_0 = 0.01, t_0 = 0., t_f = 30.):
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

h_values = np.array([5., 1., 0.5, 0.1, 0.05])
T_euler = np.arange(0, 30, 0.1)

fig = plt.figure()
ax = fig.add_subplot(111)

for index in h_values:
    T, y = euler_forward(f, h=index)
    ax.plot(T, y, linestyle="--", label=f"Euler h: {index}")
ax.plot(T_euler, y_analitc(T_euler), linestyle="--", label="Analitica")
ax.set_xlabel("t", fontsize=15)
ax.set_ylabel("Y(t)", fontsize=15)
ax.grid(linestyle="--")
ax.legend(loc="best")
plt.show()
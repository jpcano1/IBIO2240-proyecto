##
# Importamos las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.integrate as inte

# Estimación de la solución de la ecuación diferencial
# (y''-2y'+4y=8t-12sin(2t)) con y(0)=-2 y y'(0)=8
# Por los métodos de Euler y RK

# Definimos la función F1
def F1(y2):
    return y2

# Definimos la función F2
def F2(t, y1, y2):
    return 2.0 * y2 - 4.0 * y1 + 8.0 * t - 12.0 * np.sin(2.0 * t)

# Por facilidad definimos una función
# para la estimación del método de
# Euler hacia atrás
def F2EulerBack(t, y1, y2, h):
    return (y2 + h * (-4.0 * y1 + 8.0 * t - 12.0 * np.sin(2.0 * t))) / \
           (1 - 2 * h + 4 * (h**2))

# Por facilidad definimos una función
# para la estimación del método de
# Euler modificado
def F2EulerMod(t1, t2, y1, y2, h):
    return (y2 + (h / 2.0) * (F2(t1, y1, y2) - 4.0 * (y1 + (h/2.0) * y2) +
                              8.0 * t2 - 12.0 * np.sin(2.0 * t2))) / \
           (1 - h + (h**2))

# Creamos una función para encontrar
# simultáneamente las raíces de las
# ecuaciones resultantes del método
# de Euler modificado para Y1 y Y2
# Es de notar que esta función corresponde
# en realidad a un arreglo de 2 funciones:
# la primera correspondiente a Y1(i)
# la segunda correspondiente a Y2(i)
# En esta función:
# yt2 -->  Vector de dos posiciones
# donde yt2[0] corresponde al valor de Y1(i)
# y yt2[1] corresponde al valor de Y2(i)
# t1 --> Tiempo en la iteración i-1
# t2 --> Tiempo en la iteración i
# y1t1 --> Estimación de Y1 en la iteración i-1
# y2t1 --> Estimación de Y2 en la iteración i-1
# h --> Intervalo entre un tiempo y el
# siguiente (p.ej. t2-t1)
def FEulerModRoot(yt2, t1, t2, y1t1, y2t1, h):
    return [y1t1 + (h / 2.0) * \
           (F1(y2t1) + F1(yt2[1])) - yt2[0],
            y2t1 + (h / 2.0) * \
           (F2(t1, y1t1, y2t1) + F2(t2, yt2[0], yt2[1])) - yt2[1]]

# Solución Y1 analítica
def Y1Analitic(t):
    return 2 * (3**(1/2)) * np.exp(t) * np.sin((3**(1/2)) * t) + \
           2 * t + 1 - 3 * np.cos(2 * t)

# Definimos un valor para h
h = 0.01
# Definimos la condición inicial para Y1 y Y2
Y10 = -2
Y20 = 8
# Definimos el tiempo inicial
To = 0.0
# Definimos el tiempo final
Tf = 10.0
# Creamos un arreglo de tiempo que vaya
# desde To hasta Tf con pasos de h
T = np.arange(To, Tf + h, h)
# Definimos un arreglo para ir almacenando
# los valores estimados de Y1(t) en cada iteración
Y1EulerFor = np.zeros(len(T))
Y1EulerBack = np.zeros(len(T))
Y1EulerMod = np.zeros(len(T))
Y1EulerModRoot = np.zeros(len(T))
Y1RK2 = np.zeros(len(T))
Y1RK4 = np.zeros(len(T))
# Definimos un arreglo para ir almacenando
# los valores estimados de Y2(t) en cada iteración
Y2EulerFor = np.zeros(len(T))
Y2EulerBack = np.zeros(len(T))
Y2EulerMod = np.zeros(len(T))
Y2EulerModRoot = np.zeros(len(T))
Y2RK2 = np.zeros(len(T))
Y2RK4 = np.zeros(len(T))
# Asignamos el valor de la condición
# inicial al primer valor de Y1(t)
Y1EulerFor[0] = Y10
Y1EulerBack[0] = Y10
Y1EulerMod[0] = Y10
Y1EulerModRoot[0] = Y10
Y1RK2[0] = Y10
Y1RK4[0] = Y10
# Asignamos el valor de la condición
# inicial al primer valor de Y2(t)
Y2EulerFor[0] = Y20
Y2EulerBack[0] = Y20
Y2EulerMod[0] = Y20
Y2EulerModRoot[0] = Y20
Y2RK2[0] = Y20
Y2RK4[0] = Y20
# Creamos un procedimiento iterativo que
# recorra completo el arrego de tiempo desde
# la segunda posición hasta la última
for iter in range(1, len(T)):
    # Vamos estimando el valor de Yi
    # correspondiente a la iteración i

    # Euler hacia adelante
    Y1EulerFor[iter] = Y1EulerFor[iter - 1] + \
                      h * F1(Y2EulerFor[iter - 1])
    Y2EulerFor[iter] = Y2EulerFor[iter - 1] + \
                      h * F2(T[iter - 1], Y1EulerFor[iter - 1],
                             Y2EulerFor[iter - 1])
    # Euler hacia atrás

    Y2EulerBack[iter] = F2EulerBack(T[iter], Y1EulerBack[iter - 1],
                                    Y2EulerBack[iter - 1], h)
    Y1EulerBack[iter] = Y1EulerBack[iter - 1] + h * F1(Y2EulerBack[iter])


    # Euler modificado
    Y2EulerMod[iter] = F2EulerMod(T[iter - 1], T[iter],
                                  Y1EulerMod[iter - 1],
                                  Y2EulerMod[iter - 1], h)
    Y1EulerMod[iter] = Y1EulerMod[iter - 1] + (h / 2.0) * \
                       (F1(Y2EulerMod[iter - 1]) + F1(Y2EulerMod[iter]))

    # Euler modificado resolviendo el sistema de ecuaciones no-lineales
    SolMod = opt.fsolve(FEulerModRoot,
                      np.array([Y1EulerModRoot[iter - 1],
                                Y2EulerModRoot[iter - 1]]),
                      (T[iter - 1], T[iter], Y1EulerModRoot[iter - 1],
                       Y2EulerModRoot[iter - 1], h), xtol=10**-15)
    Y1EulerModRoot[iter] = SolMod[0]
    Y2EulerModRoot[iter] = SolMod[1]

    # RK2
    k11 = F1(Y2RK2[iter - 1])
    k21 = F2(T[iter - 1], Y1RK2[iter - 1], Y2RK2[iter - 1])
    k12 = F1(Y2RK2[iter - 1] + k21 * h)
    k22 = F2(T[iter - 1] + h, Y1RK2[iter - 1] + k11 * h,
             Y2RK2[iter - 1] + k21 * h)
    Y1RK2[iter] = Y1RK2[iter - 1] + (h / 2.0) * (k11 + k12)
    Y2RK2[iter] = Y2RK2[iter - 1] + (h / 2.0) * (k21 + k22)

    # RK4
    k11 = F1(Y2RK4[iter - 1])
    k21 = F2(T[iter - 1], Y1RK4[iter - 1], Y2RK4[iter - 1])
    k12 = F1(Y2RK4[iter - 1] + 0.5 * k21 * h)
    k22 = F2(T[iter - 1] + 0.5 * h, Y1RK4[iter - 1] + 0.5 * k11 * h,
             Y2RK4[iter - 1] + 0.5 * k21 * h)
    k13 = F1(Y2RK4[iter - 1] + 0.5 * k22 * h)
    k23 = F2(T[iter - 1] + 0.5 * h, Y1RK4[iter - 1] + 0.5 * k12 * h,
             Y2RK4[iter - 1] + 0.5 * k22 * h)
    k14 = F1(Y2RK4[iter - 1] + k23 * h)
    k24 = F2(T[iter - 1] + h, Y1RK4[iter - 1] + k13 * h,
             Y2RK4[iter - 1] + k23 * h)
    Y1RK4[iter] = Y1RK4[iter - 1] + (h / 6.0) * \
                  (k11 + 2.0 * k12 + 2.0 * k13 + k14)
    Y2RK4[iter] = Y2RK4[iter - 1] + (h / 6.0) * \
                  (k21 + 2.0 * k22 + 2.0 * k23 + k24)

# Creamos una función con el sistema
# de ecuaciones F1 y F2
def FSystem(t, y):
    return [F1(y[1]),F2(t,y[0],y[1])]

    # Llamamos la función solve_ivp del
    # paquete integrate de la librería scipy
SolRK45 = inte.solve_ivp(FSystem, [To,Tf], [Y10,Y20], t_eval=T, method='RK45')

# Graficamos la estimación de Y1(t)=Y(t) obtenida
plt.figure()
plt.plot(T, Y1Analitic(T), "--b")
plt.plot(T, Y1EulerFor, "r")
plt.plot(T, Y1EulerBack, "g")
plt.plot(T, Y1EulerMod, "m")
plt.plot(T, Y1EulerModRoot, "--c")
plt.plot(T, Y1RK2, "orange")
plt.plot(T, Y1RK4, "maroon")
plt.plot(T, SolRK45.y[0], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de Y1(t)=Y(t)")
plt.legend(["Analítica","EulerFor","EulerBack","EulerMod","EulerModRoot",
            "RK2","RK4","SolRK45"], fontsize=12)
plt.grid(1)

# Graficamos la estimación de Y2(t)=Y'(t) obtenida
plt.figure()
plt.plot(T, Y2EulerFor, "r")
plt.plot(T, Y2EulerBack, "g")
plt.plot(T, Y2EulerMod, "m")
plt.plot(T, Y2EulerModRoot, "--c")
plt.plot(T, Y2RK2, "orange")
plt.plot(T, Y2RK4, "maroon")
plt.plot(T, SolRK45.y[1], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de Y2(t)=Y'(t)")
plt.legend(["EulerFor","EulerBack","EulerMod","EulerModRoot",
            "RK2","RK4","SolRK45"], fontsize=12)
plt.grid(1)

# Estimación del error local
Y1EulerForErr = np.abs(Y1EulerFor - Y1Analitic(T))
Y1EulerBackErr = np.abs(Y1EulerBack - Y1Analitic(T))
Y1EulerModErr = np.abs(Y1EulerMod - Y1Analitic(T))
Y1RK2Err = np.abs(Y1RK2 - Y1Analitic(T))
Y1RK4Err = np.abs(Y1RK4 - Y1Analitic(T))

# Estimación del error acumulado con todos los métodos
Y1EulerForErrCum = np.cumsum(Y1EulerForErr)
Y1EulerBackErrCum = np.cumsum(Y1EulerBackErr)
Y1EulerModErrCum = np.cumsum(Y1EulerModErr)
Y1RK2ErrCum = np.cumsum(Y1RK2Err)
Y1RK4ErrCum = np.cumsum(Y1RK4Err)

print("{:.02f}\t{:.06f}\t{:.06f}\t{:.06f}\t{:.06f}\t{:.10f}".format(
    h, Y1EulerForErrCum[-1], Y1EulerBackErrCum[-1], Y1EulerModErrCum[-1],
    Y1RK2ErrCum[-1], Y1RK4ErrCum[-1]))

print("{:.02f}\t{:.06f}\t{:.06f}\t{:.06f}\t{:.06f}\t{:.010f}".format(
    h, Y1EulerForErrCum[-1] / np.size(Y1EulerForErrCum),
    Y1EulerBackErrCum[-1] / np.size(Y1EulerBackErrCum),
    Y1EulerModErrCum[-1] / np.size(Y1EulerModErrCum),
    Y1RK2ErrCum[-1] / np.size(Y1RK2ErrCum),
    Y1RK4ErrCum[-1] / np.size(Y1RK4ErrCum)))

##
# Importamos las librerías numpy y matplotlib
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.integrate as inte

# Estimación de la solución del sistema
# de ecuaciones del modelo SIS
# (Susceptibles-Infectados-Susceptibles)
# dS(t)/dt=bI(t)-aS(t)I(t);dI(t)/dt=aS(t)I(t)-bI(t)
# con:
# a -> Tasa de infección
# b -> Tasa de recuperación
# So -> % inicial de susceptibles
# Io -> % inicial de infectados
# Usaremos Y1 = S(t) y Y2 = I(t)
# Por los métodos de Euler y RK

# Definimos la función F1
def F1(y1, y2, a, b):
    return b * y2 - a * y1 * y2

# Definimos la función F2
def F2(y1, y2, a, b):
    return a * y1 * y2 - b * y2

# Creamos una función para encontrar
# simultáneamente las raíces de las
# ecuaciones resultantes del método
# de Euler hacia atrás para Y1 y Y2
def FEulerBackRoot(yt2, y1t1, y2t1, h, a, b):
    return [y1t1 + h * F1(yt2[0], yt2[1], a, b) - yt2[0],
            y2t1 + h * F2(yt2[0], yt2[1], a, b) - yt2[1]]

# Creamos una función para encontrar
# simultáneamente las raíces de las
# ecuaciones resultantes del método
# de Euler modificado para Y1 y Y2
def FEulerModRoot(yt2, y1t1, y2t1, h, a, b):
    return [y1t1 + (h / 2.0) * \
           (F1(y1t1, y2t1, a, b) + F1(yt2[0], yt2[1], a, b)) - yt2[0],
            y2t1 + (h / 2.0) * \
           (F2(y1t1, y2t1, a, b) + F2(yt2[0], yt2[1], a, b)) - yt2[1]]

# Para efectos de comparación,
# definimos la solución analítica para Y2
def Y2Analitic(t, a, b, So, Io, N):
    return ((a*N-b)*Io*np.exp((a*N-b)*t))/\
           ((a*N-b)+a*Io*(np.exp((a*N-b)*t)-1))

# Para efectos de comparación,
# definimos la solución analítica para Y1
def Y1Analitic(t, a, b, So, Io, N):
    return N - Y2Analitic(t, a, b, So, Io, N)

# Definimos los parámetros para resolver
# el modelo
# Tasa de infection
a = 0.5
# Tasa de recuperación
b = 0.01
# Porcentaje inicial de personas susceptibles
So = 0.99
# Porcentaje inicial de personas infectadas
Io = 1 - So
# Total de personas
N = So + Io

# Definimos un valor para h
h = 0.01
# Definimos la condición inicial para Y1 y Y2
Y10 = So
Y20 = Io
# Definimos el tiempo inicial
To = 0.0
# Definimos el tiempo final
Tf = 30.0
# Creamos un arreglo de tiempo que vaya
# desde To hasta Tf con pasos de h
T = np.arange(To, Tf + h, h)
# Definimos un arreglo para ir almacenando
# los valores estimados de Y1(t) en cada iteración
Y1EulerFor = np.zeros(len(T))
Y1EulerBackRoot = np.zeros(len(T))
Y1EulerModRoot = np.zeros(len(T))
Y1RK2 = np.zeros(len(T))
Y1RK4 = np.zeros(len(T))
# Definimos un arreglo para ir almacenando
# los valores estimados de Y2(t) en cada iteración
Y2EulerFor = np.zeros(len(T))
Y2EulerBackRoot = np.zeros(len(T))
Y2EulerModRoot = np.zeros(len(T))
Y2RK2 = np.zeros(len(T))
Y2RK4 = np.zeros(len(T))
# Asignamos el valor de la condición
# inicial al primer valor de Y1(t)
Y1EulerFor[0] = Y10
Y1EulerBackRoot[0] = Y10
Y1EulerModRoot[0] = Y10
Y1RK2[0] = Y10
Y1RK4[0] = Y10
# Asignamos el valor de la condición
# inicial al primer valor de Y2(t)
Y2EulerFor[0] = Y20
Y2EulerBackRoot[0] = Y20
Y2EulerModRoot[0] = Y20
Y2RK2[0] = Y20
Y2RK4[0] = Y20
# Creamos un procedimiento iterativo que
# recorra completo el arrego de tiempo desde
# la segunda posición hasta la última
for iter in range(1, len(T)):
    # Vamos estimando el valor de Yi
    # correspondiente a la iteración i

    # Euler hacia adelante
    Y1EulerFor[iter] = Y1EulerFor[iter - 1] + \
                      h * F1(Y1EulerFor[iter - 1], Y2EulerFor[iter - 1], a, b)
    Y2EulerFor[iter] = Y2EulerFor[iter - 1] + \
                      h * F2(Y1EulerFor[iter - 1], Y2EulerFor[iter - 1], a, b)
    # Euler hacia atrás resolviendo el sistema de ecuaciones no-lineales
    SolBack = opt.fsolve(FEulerBackRoot,
                      np.array([Y1EulerBackRoot[iter - 1],
                                Y2EulerBackRoot[iter - 1]]),
                      (Y1EulerBackRoot[iter - 1],
                       Y2EulerBackRoot[iter - 1], h, a, b), xtol=10**-15)
    Y1EulerBackRoot[iter] = SolBack[0]
    Y2EulerBackRoot[iter] = SolBack[1]

    # Euler modificado resolviendo el sistema de ecuaciones no-lineales
    SolMod = opt.fsolve(FEulerModRoot,
                      np.array([Y1EulerModRoot[iter - 1],
                                Y2EulerModRoot[iter - 1]]),
                      (Y1EulerModRoot[iter - 1],
                       Y2EulerModRoot[iter - 1], h, a, b), xtol=10**-15)
    Y1EulerModRoot[iter] = SolMod[0]
    Y2EulerModRoot[iter] = SolMod[1]

    # RK2
    k11 = F1(Y1RK2[iter - 1], Y2RK2[iter - 1], a, b)
    k21 = F2(Y1RK2[iter - 1], Y2RK2[iter - 1], a, b)
    k12 = F1(Y1RK2[iter - 1] + k11 * h, Y2RK2[iter - 1] + k21 * h, a, b)
    k22 = F2(Y1RK2[iter - 1] + k11 * h, Y2RK2[iter - 1] + k21 * h, a, b)
    Y1RK2[iter] = Y1RK2[iter - 1] + (h / 2.0) * (k11 + k12)
    Y2RK2[iter] = Y2RK2[iter - 1] + (h / 2.0) * (k21 + k22)

    # RK4
    k11 = F1(Y1RK4[iter - 1], Y2RK4[iter - 1], a, b)
    k21 = F2(Y1RK4[iter - 1], Y2RK4[iter - 1], a, b)
    k12 = F1(Y1RK4[iter - 1] + 0.5 * k11 * h,
             Y2RK4[iter - 1] + 0.5 * k21 * h, a, b)
    k22 = F2(Y1RK4[iter - 1] + 0.5 * k11 * h,
             Y2RK4[iter - 1] + 0.5 * k21 * h, a, b)
    k13 = F1(Y1RK4[iter - 1] + 0.5 * k12 * h,
             Y2RK4[iter - 1] + 0.5 * k22 * h, a, b)
    k23 = F2(Y1RK4[iter - 1] + 0.5 * k12 * h,
             Y2RK4[iter - 1] + 0.5 * k22 * h, a, b)
    k14 = F1(Y1RK4[iter - 1] + k13 * h,
             Y2RK4[iter - 1] + k23 * h, a, b)
    k24 = F2(Y1RK4[iter - 1] + k13 * h,
             Y2RK4[iter - 1] + k23 * h, a, b)
    Y1RK4[iter] = Y1RK4[iter - 1] + (h / 6.0) * \
                  (k11 + 2.0 * k12 + 2.0 * k13 + k14)
    Y2RK4[iter] = Y2RK4[iter - 1] + (h / 6.0) * \
                  (k21 + 2.0 * k22 + 2.0 * k23 + k24)

# Creamos una función con el sistema
# de ecuaciones F1 y F2
def FSystem(t, y, a, b):
    return [F1(y[0], y[1], a, b),F2(y[0],y[1], a, b)]

# Llamamos la función solve_ivp del
# paquete integrate de la librería scipy
SolRK45 = inte.solve_ivp(FSystem, [To,Tf], [Y10,Y20], args=(a, b),
                         t_eval=T, method='RK45')

# Graficamos la estimación de Y1(t)=Y(t) obtenida
plt.figure()
plt.plot(T, Y1Analitic(T, a, b, So, Io, N), "--b")
plt.plot(T, Y1EulerFor, "r")
plt.plot(T, Y1EulerBackRoot, "g")
plt.plot(T, Y1EulerModRoot, "m")
plt.plot(T, Y1RK2, "orange")
plt.plot(T, Y1RK4, "maroon")
plt.plot(T, SolRK45.y[0], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de Y1(t)=Y(t)")
plt.legend(["Analítica","EulerFor","EulerBackRoot","EulerModRoot",
            "RK2","RK4","SolRK45"], fontsize=12)
plt.grid(1)

# Graficamos la estimación de Y2(t)=Y'(t) obtenida
plt.figure()
plt.plot(T, Y2Analitic(T, a, b, So, Io, N), "--b")
plt.plot(T, Y2EulerFor, "r")
plt.plot(T, Y2EulerBackRoot, "g")
plt.plot(T, Y2EulerModRoot, "m")
plt.plot(T, Y2RK2, "orange")
plt.plot(T, Y2RK4, "maroon")
plt.plot(T, SolRK45.y[1], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de Y2(t)=Y'(t)")
plt.legend(["Analítica","EulerFor","EulerBackRoot","EulerModRoot",
            "RK2","RK4","SolRK45"], fontsize=12)
plt.grid(1)

##
# Estimación del error local
Y1EulerForErr = np.abs(Y1EulerFor - Y1Analitic(T, a, b, So, Io, N))
Y1EulerBackRootErr = np.abs(Y1EulerBackRoot - Y1Analitic(T, a, b, So, Io, N))
Y1EulerModRootErr = np.abs(Y1EulerModRoot - Y1Analitic(T, a, b, So, Io, N))
Y1RK2Err = np.abs(Y1RK2 - Y1Analitic(T, a, b, So, Io, N))
Y1RK4Err = np.abs(Y1RK4 - Y1Analitic(T, a, b, So, Io, N))

# Estimación del error acumulado con todos los métodos
Y1EulerForErrCum = np.cumsum(Y1EulerForErr)
Y1EulerBackRootErrCum = np.cumsum(Y1EulerBackRootErr)
Y1EulerModRootErrCum = np.cumsum(Y1EulerModRootErr)
Y1RK2ErrCum = np.cumsum(Y1RK2Err)
Y1RK4ErrCum = np.cumsum(Y1RK4Err)

print("{:.02f}\t{:.04f}\t{:.04f}\t{:.04f}\t{:.04f}\t{:.04f}".format(
    h, Y1EulerForErrCum[-1], Y1EulerBackRootErrCum[-1], Y1EulerModRootErrCum[-1],
    Y1RK2ErrCum[-1], Y1RK4ErrCum[-1]))

print("{:.04f}\t{:.04f}\t{:.04f}\t{:.04f}\t{:.04f}\t{:.010f}".format(
    h, Y1EulerForErrCum[-1] / np.size(Y1EulerForErrCum),
    Y1EulerBackRootErrCum[-1] / np.size(Y1EulerBackRootErrCum),
    Y1EulerModRootErrCum[-1] / np.size(Y1EulerModRootErrCum),
    Y1RK2ErrCum[-1] / np.size(Y1RK2ErrCum),
    Y1RK4ErrCum[-1] / np.size(Y1RK4ErrCum)))


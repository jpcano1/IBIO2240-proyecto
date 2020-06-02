import numpy as np
import pandas as pd

parametros = pd.read_excel("../data/parametros.xlsx", index_col=0)
parametros.loc["Theta_i"] = parametros.loc["Theta_i"] * np.pi

class ECGGenerator:

    def __init__(self):
        self.a_i = parametros.loc["a_i"]
        self.b_i = parametros.loc["b_i"]
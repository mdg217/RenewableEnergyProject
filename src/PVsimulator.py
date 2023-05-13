from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
from PVstring import *
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
import random
from scipy.optimize import minimize_scalar
from PVutils import *
from PVparallel import *

class PVsimulator:

    def __init__(self, system, parameters):
        self.system = system
        self.parameters = parameters
        
        self.Gconditions = {}
        self.Tconditions = {}

        
    def simulate(self, num_panels, num_series):
        for k in range(num_series):
            G, T = [], []
            for _ in range(24):
                lunghezza_lista = 10  # Lunghezza casuale della lista
                g = [random.randint(0, 2000) for _ in range(lunghezza_lista)]
                G.append(g)
                
                t = [random.randint(25, 55) for _ in range(lunghezza_lista)]
                T.append(t)
            
            for i, lista in enumerate(G, start=1+num_panels*k):
                self.Gconditions[i] = lista

            for i, lista in enumerate(T, start=1+num_panels*k):
                self.Tconditions[i] = lista
            
        print(self.Gconditions)
        
    
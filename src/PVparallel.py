from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
from PVstring import *
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
import random
from scipy.optimize import minimize_scalar
from PVutils import *

class PVparallel():

    def __init__(self):
        self.PVstrings = []
    
    def add(self, string):
        self.PVstrings.append(string)
    
    def get(self):
        return self.PVstrings
    
    def computeMaxPower(self, Voc):

        #Compute max, v, i result for each string
        max = []
        v = []
        i = []

        for k in range(len(self.PVstrings)):
            m, vt, it = self.PVstrings[k].getFullIVCurve()
            max.append(m)
            v.append(vt)
            i.append(it)
        
        #Define the vector function of all the strings in the parallels
        f = []

        for k in range(len(self.PVstrings)):
            f.append(interpolation1D(v[k], i[k], round(v[k][-1])))
                

        # Set the bounds for V values (the common range)
        V_min = 0
        V_max = 0

        for k in range(len(self.PVstrings)-1):
            V_max = min(v[k][-1], v[k+1][-1])

        # Define the objective function to maximize (negative total power)
        def objective_function(V):
            total_power = 0
            for k in range(len(self.PVstrings)):
                funct = f[k]
                total_power += funct(V)*V

            return -total_power

        # Find the V value that maximizes the total power
        result = minimize_scalar(objective_function, bounds=(V_min, V_max), method='bounded')

        # Extract the optimal V value and total power
        optimal_V = result.x
        max_total_power = -result.fun

        # Print the results
        print("Optimal V value:", optimal_V)
        print("Maximum total power:", max_total_power)
        print("Quanti pannelli sono accesi? " + str(optimal_V/Voc))
        
        return (max_total_power, optimal_V, optimal_V/Voc)
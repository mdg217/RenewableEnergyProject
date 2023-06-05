from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
from PVstring import *
from scipy.interpolate import interp1d
import random
from scipy.optimize import minimize_scalar
from PVutils import *
import time

class PVparallel():

    __slots__ = 'PVstrings'

    def __init__(self):
        self.PVstrings = []
    
    def add(self, string):
        self.PVstrings.append(string)
    
    def getParallel(self):
        return self.PVstrings
    
    def clear(self):
        self.PVstrings = []
    
    def computeMaxPower(self, Voc):

        start = time.time()

        #Compute max, v, i result for each string
        max = []
        v = []
        i = []

        for k in range(len(self.PVstrings)):
            m, vt, it = self.PVstrings[k].getFullIVCurve()
            max.append(m)
            v.append(vt)
            i.append(it)
        
        f = []

        #Define the vector function of all the strings in the parallels
        for k in range(len(self.PVstrings)):
            f.append(interpolation1D(v[k], i[k]))

        # Set the bounds for V values (the common range)
        V_min = 0
        V_max = 0

        for k in range(len(self.PVstrings)-1):
            V_max = min(v[k][-1], v[k+1][-1])

        # Define the objective function to maximize (negative total power)
        def objective_function(V):
            total_power = 0
            for k in range(len(self.PVstrings)):
                try: 
                    funct = f[k]
                    total_power += funct(V)*V
                except ValueError as e:
                    #print("last value missing")
                    pass

            return -total_power

        # Find the V value that maximizes the total power
        result = minimize_scalar(objective_function, bounds=(V_min, V_max), method='bounded')

        # Extract the optimal V value and total power
        optimal_V = result.x
        max_total_power = -result.fun

        end = time.time()
        print("Necessary time for the optimization is: " + str(end - start))

        self.plot_PV_curve(f)
        
        #Print the results
        #print("Optimal V value:", optimal_V)
        #print("Maximum total power:", max_total_power)
        #print("Quanti pannelli sono accesi? " + str(round(optimal_V/Voc)))
        #print("---------------------------------------------------")
        
        return (max_total_power, optimal_V, optimal_V/Voc)
    
    def plot_PV_curve(self, f):
        #Compute the max value of voltage of the series

        maxV = 0 
        for x in range(len(self.PVstrings)):
            maxV = max(maxV, f[x].x.max())

        #Creazione dei dati per il plot
        v_plotter = list(range(round(maxV)))
        #print(type(v_plotter))

        total_current_plotter = []

        
        for x in range(len(v_plotter)):
            current = 0
            for i in range(len(self.PVstrings)):
                try: 
                    funct = f[i]
                    current += funct(x)
                except ValueError as e:
                    #print("last value missing")
                    pass
            total_current_plotter.append(current*x)

        if len(total_current_plotter)>0:
           # print(total_current_plotter)

            plt.plot(v_plotter, total_current_plotter)
            plt.xlabel('Tensione (V)')
            plt.ylabel('Potenza (W)')
            plt.title('Plot della curva P-V in una precisa ora del giorno.')
            plt.show()
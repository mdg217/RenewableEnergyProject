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

    __slots__ = 'parameters', 'system', 'Gconditions', 'Tconditions'

    def __init__(self, parameters):
        self.system = PVparallel()
        self.parameters = parameters
        
        self.Gconditions = {}
        self.Tconditions = {}

        
    def simulate(self, num_panels, num_series):
        filename = 'RenewableEnergyProject\\test\\report.csv'
        column_name_g = 'G(i)'
        column_name_t = 'T2m'
        
        #Create a list with #num_series of list of irradiation conidtions
        for k in range(num_series):
            self.Gconditions[k] = read_csv_and_extract_column(filename, column_name_g, num_panels)
            #print(self.Gconditions[k][0][0])
            self.Tconditions[k] = read_csv_and_extract_column(filename, column_name_t, num_panels)
            #print(self.Tconditions[k][0][0])

        self.createShadowZone(type=2)    #max power without shadow = 2220 approx
            
        p_result = []
        
        for hour in range(24):
            
            for d in range(num_series):
                
                s = PVstring()
                
                for i in range(num_panels):
                    s.add(self.Gconditions[d][hour][i], self.Tconditions[d][hour][i], self.parameters, 30)
                    #s.get(i)
                
                self.system.add(s)
            
            p_result.append(self.system.computeMaxPower(59.4)[0])
            #print(p_result)
            
            self.system.clear()
            
        keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        
        #print(keys)
        
        values = p_result
        
        #print(values)
        
        plt.plot(keys, values)
        plt.xlabel('Tempo (t)')
        plt.ylabel('Potenza (W)')
        plt.title('Plot della potenza misurata durante il giorno')
        plt.show()
        
    def createShadowZone(self, type):
        if type == 1: # multiple string shadowing
            pass

        elif type == 2: # single string shadowing
            for x in range(len(self.Gconditions[0])):
                for i in range(len(self.Gconditions[0][x])):
                    if self.Gconditions[0][x][i]>200:
                        self.Gconditions[0][x][i] = 200
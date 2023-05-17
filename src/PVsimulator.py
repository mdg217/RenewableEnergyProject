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

    def __init__(self, parameters):
        self.system = PVparallel()
        self.parameters = parameters
        
        self.Gconditions = {}
        self.Tconditions = {}

        
    def simulate(self, num_panels, num_series):
        for k in range(num_series):
            G, T = [], []
            for _ in range(24):
                lunghezza_lista = num_panels  # Lunghezza casuale della lista
                g = [random.randint(1000, 2000) for _ in range(lunghezza_lista)]
                print(g)
                g.sort()
                print(g)
                G.append(g)
                
                t = [random.randint(25, 55) for _ in range(lunghezza_lista)]
                t.sort()
                T.append(t)
            
            self.Gconditions[k] = G
            self.Tconditions[k] = T
            
        #print(self.Gconditions)

        p_result = []
        
        for hour in range(24):
            
            for d in range(num_series):
                
                s = PVstring()
                
                for i in range(num_panels):
                    s.add(self.Gconditions[d][hour][i], self.Tconditions[d][hour][i], self.parameters, 30)
                    #s.get(i)
                
                self.system.add(s)
            
            p_result.append(self.system.computeMaxPower(59.4)[0])
            print(p_result)
            
            self.system.clear()
            
        keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        for x in keys:
            x = x-1
        
        print(keys)
        
        values = p_result
        
        print(values)
        
        plt.plot(keys, values)
        plt.xlabel('Chiavi')
        plt.ylabel('Valori')
        plt.title('Plot del dizionario')
        plt.show()
        
        
        
    
    
    
    
    
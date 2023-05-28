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
import numpy as np

class PVsimulator:

    __slots__ = 'parameters', 'system', 'Gconditions', 'Tconditions'

    def __init__(self, parameters):
        self.system = PVparallel()
        self.parameters = parameters
        
        self.Gconditions = {}
        self.Tconditions = {}

        
    def simulate(self, num_panels, num_series, mode):
        filename = 'test\\report.csv'
        column_name_g = 'G(i)'
        column_name_t = 'T2m'
        
        #Create a list with #num_series of list of irradiation conidtions
        for k in range(num_series):
            self.Gconditions[k] = read_csv_and_extract_column(filename, column_name_g, num_panels)
            #print(self.Gconditions[k][0][0])
            self.Tconditions[k] = read_csv_and_extract_column(filename, column_name_t, num_panels)
            #print(self.Tconditions[k][0][0])

        #Senza intoppi = 940V e 100V circa
        self.createShadowZone(type=mode)    #max power without shadow = 500 approx
        #self.createShadowZone(type=1)    

        p_result = []
        v_result = []
        
        for hour in range(24):
            
            for d in range(num_series):
                
                s = PVstring()
                
                for i in range(num_panels):
                    s.add(self.Gconditions[d][hour][i], self.Tconditions[d][hour][i], self.parameters)
                    #s.get(i)
                
                self.system.add(s)
            
            iteration = self.system.computeMaxPower(59.4)
            p_result.append(iteration[0])
            v_result.append(iteration[1])
            #print(p_result)
            
            self.system.clear()
            
        keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        
        values = p_result
        
        plt.plot(keys, values)
        plt.xlabel('Tempo (t)')
        plt.ylabel('Potenza (W)')
        plt.title('Plot della potenza misurata durante il giorno')
        plt.show()

        plt.plot(keys, v_result)
        plt.xlabel('Tempo (t)')
        plt.ylabel('Tensione Ottimale (V)')
        plt.title('Plot della Tensione ottimizzata durante il giorno')
        plt.show()
        
    def createShadowZone(self, type):
        print(len(self.Gconditions))
        print(len(self.Gconditions[0]))
        print(len(self.Gconditions[0][0]))

        if type == 1: # multiple string shadowing but at the same level
            for x in range(len(self.Gconditions)): # for all the strings in the parallel
                for i in range(len(self.Gconditions[x])): # for all the 24 conditions in a day
                    if self.Gconditions[x][i][0]>100:
                        self.Gconditions[x][i][0] = 100
                    print(self.Gconditions[x][i][0])

            for x in range(len(self.Gconditions)):
                print(self.Gconditions[x])

        elif type == 2: # single string shadowing
            for x in range(len(self.Gconditions[0])):
                for i in range(len(self.Gconditions[0][x])):
                    if self.Gconditions[0][x][i]>100:
                        self.Gconditions[0][x][i] = 100
        
        elif type == 3: # central panel shadowing
            for x in range(len(self.Gconditions[0])):
                    if self.Gconditions[1][x][0]>100:
                        self.Gconditions[1][x][0] = 100

        elif type == 4: # Time-Varying simulation shadowing
            for x in range(5, 6):
                if self.Gconditions[0][x][0]>0:
                        self.Gconditions[0][x][0] = 10
            for x in range(7, 8):
                if self.Gconditions[0][x][0]>100:
                        self.Gconditions[0][x][0] = 100
                if self.Gconditions[1][x][0]>100:
                        self.Gconditions[1][x][0] = 100
            for x in range(9, 10):
                if self.Gconditions[1][x][0]>100:
                        self.Gconditions[1][x][0] = 100
                if self.Gconditions[2][x][0]>100:
                        self.Gconditions[2][x][0] = 100
            for x in range(13, 18):
                if self.Gconditions[1][x][0]>100:
                        self.Gconditions[1][x][0] = 100
                if self.Gconditions[2][x][0]>100:
                        self.Gconditions[2][x][0] = 100
                if self.Gconditions[1][x][1]>100:
                        self.Gconditions[1][x][1] = 100
                if self.Gconditions[2][x][1]>100:
                        self.Gconditions[2][x][1] = 100


            print(self.Gconditions)

        else:
            print("")
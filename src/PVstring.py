from PVpanel import *
import matplotlib.pyplot as plt
import numpy as np
import itertools


class PVstring:

    __slots__ = "N", "pvs", "battery_voltage"

    def __init__(self):
        self.N = 0
        self.pvs = []

    def add(self, G, T, parameters, battery_voltage):
        newPanel = PVpanel(parameters, G, T)
        self.pvs.append(newPanel)
        self.battery_voltage = battery_voltage
        self.N +=1

    def get(self, index):
        print("Il pannello in posizione " + str(index))
        print(self.pvs[index])
        print("----------------------------")

    def remove(self, index):
        self.pvs.remove(index)

    def getCurrentVector(self):
        currents = []
        for x in range(self.N):
            currents.append(self.pvs[x].get_PV_current_voltage()[0])
        currents = list(itertools.chain.from_iterable(currents))
        return currents

    def getVoltageVector(self):
        voltages = []
        for x in range(self.N):
            voltages.append(self.pvs[x].get_PV_current_voltage()[1])
        voltages = list(itertools.chain.from_iterable(voltages))
        return voltages
    
    def getMaxPower(self, mode):

        Vmpp = (self.getVoltageVector())#.sort(reverse=True)
        Vmpp.sort(reverse=True)
        print(Vmpp)
        Impp = self.getCurrentVector()#.sort()
        Impp.sort(reverse=False)
        print(Impp)
        N = self.N

        if mode == 1: #matrix

            print()

            p = [[(0,0,0)] * N for _ in range(N)]
            
            for i in range(N):
                for j in range(N):
                    if j == 0:
                        p[i][j] = (Vmpp[i]*Impp[i], Vmpp[i], Impp[i])
                    elif j==i:
                        p[i][j] = p[i][j-1] 
                    else: 
                        imin = min(p[i][j-1][2], Impp[j])
                        vtot = Vmpp[j]+p[i][j-1][1]

                        p1 = imin*vtot
                        p2 = p[i][j-1][0]
                        if p1 > p2:
                            p[i][j] = (p1, vtot, imin)
                        else:
                            p[i][j] = (p2, vtot-p[i][j-1][1], p[i][j-1][2])
                        
            
            for i in range(N):
                for j in range(N):
                    print(str(p[i][j]) + "\t   " , end="")
                print()
            print()

            return 0

        elif mode == 2: 
            pass

    def plotStruct(self):
        N = self.N

        # Disegna la riga
        matrix = ""

        # Disegna la matrice
        for i in range(N//10):
            for j in range(10):
                matrix += '█' + str(j) + '█'
                if j < 9:
                    matrix += '---'
            matrix += '\n'
            if i%2==0:
                matrix += "\t\t\t\t\t\t       |\n"
            else:
                matrix += " |\n"

        # Stampa la matrice
        print(matrix)
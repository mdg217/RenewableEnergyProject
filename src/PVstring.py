from PVpanel import *
import matplotlib.pyplot as plt
import numpy as np


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

    def remove(self, index):
        self.pvs.remove(index)

    def getCurrentVector(self):
        currents = []
        for x in range(self.N):
            currents.append(self.pvs[x].get_PV_current_voltage())
            #print(self.pvs[x].get_PV_current_voltage()[0])
        return currents

    def getVoltageVector(self):
        voltages = []
        for x in range(self.N):
            voltages.append(self.pvs[x].get_PV_current_voltage()[1])
            #print(self.pvs[x].get_PV_current_voltage()[1])
        return voltages
    
    def getMaxPower(self, mode):

        Vmpp = self.getVoltageVector()
        Impp = self.getCurrentVector()

        if mode == 1: #Dynamic
            n = len(Impp)
            dp = [0] * (n + 1)
            for i in range(1, n + 1):
                print(Impp[i - 1] * Vmpp[i - 1])
                dp[i] = max(dp[i - 1], Impp[i - 1] * Vmpp[i - 1])
                for j in range(i - 1, 0, -1):
                    prodotto = Impp[i - 1] * Vmpp[j - 1]
                    dp[i] = max(dp[i], prodotto + dp[j - 1])
            return dp[n]
        elif mode == 2: 
            return 0

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
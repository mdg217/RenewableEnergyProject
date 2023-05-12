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
    
    def getFullIVCurve(self):

        Vmpp = self.getVoltageVector()
        Impp = self.getCurrentVector()
        
        imin = 0
        vtot = 0
            
        v = []
        c = []
            
        v_tmp = []
        c_tmp = []
            
        for i in range(self.N):
            model = self.pvs[i].define_model()
            v.append(model['v'])
            v_tmp.append(model['v'][-1][-1])
            #print(v_tmp)
            c.append(model['i'])
            c_tmp.append(model['i'][0][0])
            #print(c_tmp)
                
        c_ind = [i for i in range(len(c_tmp))] # oppure ind = list(range(len(l)))
        c_new_ind = [i for i, _ in sorted(enumerate(c_ind), key=lambda x: x[1], reverse=True)]  # [3, 1, 2, 0]
        #print([c_tmp[i] for i in c_new_ind]   )
        c = [c[i] for i in c_new_ind]        
            
        v_ind = [i for i in range(len(v_tmp))] # oppure ind = list(range(len(l)))
        v_new_ind = sorted(v_ind, key=lambda i: v_tmp[i])
        #print([v_tmp[i] for i in v_new_ind]   )
        v = [v[i] for i in v_new_ind]        

        # Crea la figura e i due assi (grafici)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        last_max_value = 0

        # Disegna le curve
        for i in range(self.N):
            for j in range(len(v[i])):
                ax1.plot(v[i][j]+last_max_value, c[i][j], label='Curva {}'.format(i+1))
            last_max_value += v[i][-1][-1]
            
            
        #unire le tensioni
        last_max_value = v[0][0][-1]
            
        total_v_plot = v[0][0]
        for i in range(self.N-1):
            #print(v[i+1][0])
            total_v_plot = np.append(total_v_plot, v[i+1][0] + last_max_value)
            last_max_value += v[i][0][-1]
            
        #unire le correnti
        total_c_plot = np.zeros(self.N*len(c[0][0]))
        index_tot = 0
            
        for i in range(self.N):
            for j in range(len(c[0][0])):
                if(i<self.N-1):
                    if c[i][0][j]<c[i+1][0][0]:
                        total_c_plot[index_tot] = c[i+1][0][0]
                    elif c[i][0][j]>=c[i+1][0][0]:
                        total_c_plot[index_tot] = c[i][0][j]
                else:
                    total_c_plot[index_tot] = c[i][0][j]
                index_tot +=1
            
        ax2.plot(total_v_plot, total_c_plot)
          
        plt.tight_layout()                    

        # Mostra il grafico
        plt.show()   
            
        return (max(total_v_plot*total_c_plot), total_v_plot, total_c_plot)
                        

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
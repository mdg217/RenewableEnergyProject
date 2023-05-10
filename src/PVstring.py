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

        Vmpp = self.getVoltageVector()
        #Vmpp.sort(reverse=True)
        #print(Vmpp)
        Impp = self.getCurrentVector()
        #Impp.sort(reverse=False)
        #print(Impp)
        N = self.N

        if mode == 1: #matrix
            
            #implementare un 
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
                            p[i][j] = (p2, p[i][j-1][1], p[i][j-1][2])
                        
            #IPOTESI: misuro in real-time V e I sulla  
            #VINCOLO AGGIUNTIVO: ipotizzare di dover avere un parallelo tra K stringhe 
            #Confrontare con la versione con i diodi di bypass
            
            for i in range(N):
                for j in range(N):
                    print(tuple("{:.1f}".format(valore) for valore in p[i][j]), end="")
                    print("\t   ", end="")
                print()
            print()

            return max([row[-1][0] for row in p])

        elif mode == 2: #Bypass diode
            
            imin = 0
            vtot = 0
            
            v = []
            c = []
            
            v_tmp = []
            c_tmp = []
            
            for i in range(N):
                model = self.pvs[i].define_model()
                v.append(model['v'])
                v_tmp.append(model['v'][-1][-1])
                print(v_tmp)
                c.append(model['i'])
                c_tmp.append(model['i'][0][0])
                print(c_tmp)
                
            c_ind = [i for i in range(len(c_tmp))] # oppure ind = list(range(len(l)))
            c_new_ind = [i for i, _ in sorted(enumerate(c_ind), key=lambda x: x[1], reverse=True)]  # [3, 1, 2, 0]
            print([c_tmp[i] for i in c_new_ind]   )
            c = [c[i] for i in c_new_ind]        
            
            v_ind = [i for i in range(len(v_tmp))] # oppure ind = list(range(len(l)))
            v_new_ind = sorted(v_ind, key=lambda i: v_tmp[i])
            print([v_tmp[i] for i in v_new_ind]   )
            v = [v[i] for i in v_new_ind]        

            # Crea il grafico
            plt.figure()

            last_max_value = 0

            # Disegna le curve
            for i in range(N):
                for j in range(len(v[i])):
                    plt.plot(v[i][j]+last_max_value, c[i][j], label='Curva {}'.format(i+1))
                last_max_value += v[i][-1][-1]
                

            # Mostra il grafico
            plt.show()   
            
                

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
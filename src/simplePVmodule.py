import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


class simplePVmodule:
    
    def __init__(self):
         self.parameters = {
             'Isc' : 5.2,
             'alpha': 0.005,
             'Tref' : 25,
             'Gref' : 1000,
             'q' : 1.602176634e-19,
             'k' : 1.38064852e-23,
             'Eg' : 1.12,
             'I0ref' : 8.196e-10,
             'Vtref' : 1.38064852e-23 *(25 + 273.15) / 1.602176634e-19,
             'Rpref' : 381.68,
             'Rs' : 1.065,
             'a' : 2.6373  
         }
    
    def Iph(self, T, G):
        return (self.parameters['Isc'] + self.parameters['alpha']*(T - self.parameters['Tref']))*(G/self.parameters['Gref'])
    
    def I0(self, T):
        return self.parameters['I0ref']*(T/self.parameters['Tref'])**3*np.exp((self.parameters['q']*self.parameters['Eg'])/(self.parameters['a']*self.parameters['k'])*(1/self.parameters['Tref'] - 1/T))
    
    def Vt(self, T):
        return self.parameters['Vtref']*(T/self.parameters['Tref'])
    
    def Rp(self, G):
        return self.parameters['Rpref']*(self.parameters['Gref']/G)
    
    def I(self, T, G, V):
        I = optimize.fsolve(lambda x: x - self.I0(T)*(np.exp((V + x*self.parameters['Rs'])/(self.Vt(T))) - 1) - (V + x*self.parameters['Rs'])/self.Rp(G) + self.Iph(T,G), 0.01)
        return I
    
def IV_curve(T, G):
    module = simplePVmodule()
    V = np.linspace(0, 0.6, 61) # range di tensioni
    I = np.zeros_like(V)
    for i in range(len(V)):
        I[i] = module.I(T, G, V[i])
    fig, ax = plt.subplots()
    ax.plot(V, I)
    ax.set_xlabel('V [V]')
    ax.set_ylabel('I [A]')
    ax.set_title(f'IV curve at T={T} C and G={G} W/m^2')
    plt.show()
    
IV_curve(T=25, G=2000)




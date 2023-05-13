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
from PVsimulator import *

if __name__ == "__main__":
    # Definizione dei parametri del pannello solare
    parameters = {
        'Name': 'Canadian Solar CS5P-220M',
        'BIPV': 'N',
        'Date': '10/5/2009',
        'T_NOCT': 42.4,
        'A_c': 1.7,
        'N_s': 96,
        'I_sc_ref': 5.1,
        'V_oc_ref': 59.4,
        'I_mp_ref': 4.69,
        'V_mp_ref': 46.9,
        'alpha_sc': 0.004539,
        'beta_oc': -0.22216,
        'a_ref': 2.6373,
        'I_L_ref': 5.114,
        'I_o_ref': 8.196e-10,
        'R_s': 1.065,
        'R_sh_ref': 381.68,
        'Adjust': 8.7,
        'gamma_r': -0.476,
        'Version': 'MM106',
        'PTC': 200.1,
        'Technology': 'Mono-c-Si',
    }

    # Creazione di una stringa di pannelli solari
    string1 = PVstring()

    # Aggiunta di N pannelli alla stringa con differenti condizioni operative
    N = 3

    # radiazione solare effettiva in W/m^2
    G = [[random.randint(0, 2000)] for i in range(N)]
    G.sort()

    # temperatura della cella in °C
    T = [[random.randint(25, 50)] for i in range(N)]
    T.sort()

    for i in range(N):
        string1.add(G[i], T[i], parameters, 30)
        
    string2 = PVstring()

    # radiazione solare effettiva in W/m^2
    G = [[random.randint(0, 2000)] for i in range(N)]
    G.sort()

    # temperatura della cella in °C
    T = [[random.randint(25, 50)] for i in range(N)]
    T.sort()

    for i in range(N):
        string2.add(G[i], T[i], parameters, 30)
        
    string3 = PVstring()

    # radiazione solare effettiva in W/m^2
    G = [[random.randint(0, 2000)] for i in range(N)]
    G.sort()

    # temperatura della cella in °C
    T = [[random.randint(25, 50)] for i in range(N)]
    T.sort()

    for i in range(N):
        string3.add(G[i], T[i], parameters, 30)
        
    Parallel = PVparallel()
    Parallel.add(string1)
    Parallel.add(string2)
    Parallel.add(string3)

    Parallel.computeMaxPower(parameters['V_oc_ref'])
    
    
    #Test simulation
    simulator = PVsimulator(string1, parameters)
    simulator.simulate(10, 4)
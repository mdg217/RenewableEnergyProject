from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
from PVstring import *
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
import random
from scipy.optimize import minimize_scalar
from PVutils import *

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
    N = 2

    # radiazione solare effettiva in W/m^2
    G = [[random.randint(0, 2000)] for i in range(N)]
    G.sort()
    #G = [[3000],[500],[2000],[200]]

    # temperatura della cella in °C
    T = [[random.randint(25, 50)] for i in range(N)]
    T.sort()
    #T = [[50],[30],[40],[25]]

    for i in range(N):
        string1.add(G[i], T[i], parameters, 30)
        
    string2 = PVstring()

    # Aggiunta di N pannelli alla stringa con differenti condizioni operative
    N = 2

    # radiazione solare effettiva in W/m^2
    G = [[random.randint(0, 2000)] for i in range(N)]
    G.sort()
    #G = [[3000],[500],[2000],[200]]

    # temperatura della cella in °C
    T = [[random.randint(25, 50)] for i in range(N)]
    T.sort()
    #T = [[50],[30],[40],[25]]

    for i in range(N):
        string2.add(G[i], T[i], parameters, 30)
        
    max1, v1, i1 = string1.getFullIVCurve()
    print(max1)
    
    max2, v2, i2 = string2.getFullIVCurve()
    print(max2)
    
    f1, interpoled_v1, interpoled_i1 = interpolation1D(v1, i1, round(v1[-1]))
    
    f2, interpoled_v2, interpoled_i2 = interpolation1D(v2, i2, round(v2[-1]))
    
    # Define the objective function to maximize (negative total power)
    def objective_function(V):
        total_power = -(f1(V)*V + f2(V)*V)
        return total_power

    # Set the bounds for V values (the common range)
    V_min = 0
    V_max = min(v2[-1], v1[-1])

    # Find the V value that maximizes the total power
    result = minimize_scalar(objective_function, bounds=(V_min, V_max), method='bounded')

    # Extract the optimal V value and total power
    optimal_V = result.x
    max_total_power = -result.fun

    # Print the results
    print("Optimal V value:", optimal_V)
    print("Maximum total power:", max_total_power)
    
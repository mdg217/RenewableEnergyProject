from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
from PVstring import *
from scipy.interpolate import interp1d
import csv

def interpolation1D(v, c, last_value):
    #print(last_value)
    
    # Creazione della funzione interpolata
    f = interp1d(v, c)
    #print(f)
    # Valori di x per cui calcolare la funzione interpolata
    x_new = np.linspace(0, max(v), num=1000)
    # Calcolo dei valori y corrispondenti
    y_new = f(x_new)
        
    # Plot della versione interpolata
    """plt.plot(x_new, y_new, label='Interpolata')
    plt.scatter(v, c, color='red', label='Punti originali')
    plt.legend()
    plt.xlabel('v')
    plt.ylabel('i')
    plt.title('Interpolazione dei punti')
    plt.show()"""
    return f

def read_csv_and_extract_column(filename, column_name, N):
    data = []
    finalData = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            data.append(float(row[column_name]))
    
    for x in data:
        row = []
        for i in range(N):
            row.append(x)
        finalData.append(row)     
    
    return finalData
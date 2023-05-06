from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
from PVmodule import *

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

cases = [
    (500, 40)
]

pv0_1 = PVmodule(parameters, cases)
pv0_1.plot_curves()

i_mp, i_pv, v_mp, v_pv = pv0_1.get_PV_current_voltage()
print("Current Max: " + str(i_mp) + "\tVoltage Max: " + str(v_mp))

print("Current PV: " + str(i_pv) + "\tVoltage PV: " + str(v_pv))
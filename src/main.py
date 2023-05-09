from PVAnalyzer import *
from PVModule import *

class Main:
    @staticmethod
    def run_test():
        # Parametri del modulo fotovoltaico
        G_ref = 1000  # W/m^2
        T_ref = 25  # °C
        I_sc_ref = 5.2  # A
        V_oc_ref = 45.5  # V
        I_mp_ref = 4.8  # A
        V_mp_ref = 37.0  # V
        alpha_I_sc = 0.005  # A/°C
        beta_V_oc = -0.32  # V/°C
        n_s = 72  # numero di celle in serie
        K_i = 0.01  # A/°C
        K_v = -0.005  # V/°C
        R_s = 1.065

        # Creazione di un'istanza del modulo fotovoltaico
        pv_module = PVModule(G_ref, T_ref, I_sc_ref, V_oc_ref, I_mp_ref, V_mp_ref, alpha_I_sc, beta_V_oc, n_s, K_i, K_v, R_s)

        # Valori di G e T per un singolo pannello
        G = 800  # W/m^2
        T = 35  # °C

        # Generazione della curva I-V per un singolo pannello
        voltages_single, currents_single = PVAnalyzer.iv_curve_single_panel(pv_module, G, T)

        print(voltages_single)
        print(currents_single)


Main.run_test()
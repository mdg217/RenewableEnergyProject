import numpy as np

class PVModule:
    def __init__(self, G_ref, T_ref, I_sc_ref, V_oc_ref, I_mp_ref, V_mp_ref, alpha_I_sc, beta_V_oc, n_s, K_i, K_v, R_s):
        self.G_ref = G_ref  # radiazione solare di riferimento (W/m^2)
        self.T_ref = T_ref  # temperatura di riferimento (°C)
        self.I_sc_ref = I_sc_ref  # corrente di corto circuito di riferimento (A)
        self.V_oc_ref = V_oc_ref  # tensione di circuito aperto di riferimento (V)
        self.I_mp_ref = I_mp_ref  # corrente al punto di massima potenza di riferimento (A)
        self.V_mp_ref = V_mp_ref  # tensione al punto di massima potenza di riferimento (V)
        self.alpha_I_sc = alpha_I_sc  # coeff. temp. per la corrente di corto circuito (%/°C)
        self.beta_V_oc = beta_V_oc  # coeff. temp. per la tensione di circuito aperto (%/°C)
        self.n_s = n_s  # numero di celle in serie nel modulo
        self.K_i = K_i  # coeff. di idealtà del diodo corrente
        self.K_v = K_v  # coeff. di idealtà del diodo tensione
        self.R_s = R_s
        
    def I_sc(self, G, T):
        return self.I_sc_ref * (G / self.G_ref) * (1 + self.alpha_I_sc * (T - self.T_ref))

    def V_oc(self, G, T):
        return self.V_oc_ref * (1 + self.beta_V_oc * (T - self.T_ref))

    def I_ph(self, G, T):
        return self.I_sc(G, T)

    def I_0(self, G, T):
        return self.I_ph(G, T) / (np.exp(self.V_oc(G, T) / (self.K_v * self.n_s)) - 1)

    def V_t(self, T):
        k = 1.38064852e-23  # costante di Boltzmann (J/K)
        q = 1.602176634e-19  # carica elementare (C)
        return k * (T + 273.15) / q

    def I_d(self, V, G, T):
        return self.I_0(G, T) * (np.exp((V + self.I_0(G, T) * self.R_s) / (self.K_i * self.n_s * self.V_t(T))) - 1)

    def output(self, V, G, T):
        return self.I_ph(G, T) - self.I_d(V, G, T)

    def max_power(self, G, T):
        # Questo metodo può essere implementato utilizzando un algoritmo di ricerca numerica, come il metodo di bisezione.
        # Per semplicità, verranno restituiti i valori di riferimento

        return self.I_mp_ref * self.V_mp_ref
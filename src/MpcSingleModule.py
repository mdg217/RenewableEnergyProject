import casadi as cs

# Dichiarazione delle variabili
V, I, I_L, I_0, R_s, R_sh, T, G, V_t = cs.SX.sym('V'), cs.SX.sym('I'), cs.SX.sym('I_L'), cs.SX.sym('I_0'), cs.SX.sym('R_s'), cs.SX.sym('R_sh'), cs.SX.sym('T'), cs.SX.sym('G'), cs.SX.sym('V_t')

# Equazione della corrente del fotodiodo
I_ph = G * I_L
I_diode = I_0 * (cs.exp((V + I * R_s) / (V_t * T)) - 1)
I_rs = (V + I * R_s) / R_sh
I_pv = I_ph - I_diode - I_rs

# Definizione del modello dinamico
x = cs.vertcat(V, I)
u = I_L
f = cs.vertcat(I_pv - V / R_sh, (I_L - I_pv) / R_s)

# Creazione del modello
dae = {'x': x, 'p': u, 'ode': f}
opts = {'tf': 0.1}
model = cs.integrator('model', 'cvodes', dae, opts)

# Definizione dei parametri del modello
p = [3.7, 0.034, 2.2e-9, 1e6, 100, 300, 1000, 0.0259]

# Definizione delle condizioni iniziali
x0 = [0, 0]

# Esecuzione della simulazione
result = model(x0=x0, p=p)
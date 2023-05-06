from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt

class PVmodule:   
    
    __slots__ = 'parameters', 'conditions'
    
    def __init__(self, parameters, cases):
        self.parameters = parameters
        self.conditions = pd.DataFrame(cases, columns=['Geff', 'Tcell'])

    def define_model(self):
        IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
        self.conditions['Geff'],
        self.conditions['Tcell'],
        alpha_sc=self.parameters['alpha_sc'],
        a_ref=self.parameters['a_ref'],
        I_L_ref=self.parameters['I_L_ref'],
        I_o_ref=self.parameters['I_o_ref'],
        R_sh_ref=self.parameters['R_sh_ref'],
        R_s=self.parameters['R_s'],
        EgRef=1.121,
        dEgdT=-0.0002677
        )
        
        # plug the parameters into the SDE and solve for IV curves:
        curve_info = pvsystem.singlediode(
            photocurrent=IL,
            saturation_current=I0,
            resistance_series=Rs,
            resistance_shunt=Rsh,
            nNsVth=nNsVth,
            ivcurve_pnts=100,
            method='lambertw'
        )   

        return curve_info

    def get_PV_current_voltage(self):
        v_mp = []
        v_pv = []
        
        i_mp = []
        i_pv = []
        
        model_curve = self.define_model()
        for i, case in self.conditions.iterrows():
            label = (
                "$G_{eff}$ " + f"{case['Geff']} $W/m^2$\n"
                "$T_{cell}$ " + f"{case['Tcell']} $\\degree C$"
            )
            plt.plot(model_curve['v'][i], model_curve['i'][i], label=label)
            v_mp.append(model_curve['v_mp'][i])
            v_pv.append(model_curve['v_oc'][i])
            i_mp.append(model_curve['i_mp'][i])
            i_pv.append(model_curve['i_sc'][i])
        
        return [i_mp, i_pv, v_mp, v_pv]
    
    def plot_curves(self):
        
        model_curve = self.define_model()
        for i, case in self.conditions.iterrows():
            label = (
                "$G_{eff}$ " + f"{case['Geff']} $W/m^2$\n"
                "$T_{cell}$ " + f"{case['Tcell']} $\\degree C$"
            )
            plt.plot(model_curve['v'][i], model_curve['i'][i], label=label)
            v_mp = (model_curve['v_mp'][i])
            i_mp = (model_curve['i_mp'][i])
            # mark the MPP
            plt.plot([v_mp], [i_mp], ls='', marker='o', c='k')
        
        plt.legend(loc=(1.0, 0))
        plt.xlabel('Module voltage [V]')
        plt.ylabel('Module current [A]')
        plt.title(self.parameters['Name'])
        plt.show()
        plt.gcf().set_tight_layout(True)

    
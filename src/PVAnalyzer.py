import numpy as np
import matplotlib.pyplot as plt
from PVModule import *

class PVAnalyzer:
    @staticmethod
    def iv_curve_single_panel(pv_module, G, T, num_points=100, v_min=0, v_max=None):
        if v_max is None:
            v_max = pv_module.V_oc(G, T)
            print(v_max)

        voltages = np.linspace(v_min, v_max, num_points)
        currents = np.array([pv_module.output(v, G, T) for v in voltages])
        
        fig, ax = plt.subplots()
        ax.plot(voltages, currents)
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Current (A)')
        ax.set_title("I-V Curve")
        plt.show()

        return voltages, currents

    @staticmethod
    def iv_curve_series_panels(pv_modules, G_list, T_list, num_points=100, v_min=0, v_max=None):
        if len(pv_modules) != len(G_list) or len(pv_modules) != len(T_list):
            raise ValueError("The length of pv_modules, G_list, and T_list must be the same.")

        if v_max is None:
            v_max = sum([pv.V_oc(G, T) for pv, G, T in zip(pv_modules, G_list, T_list)])

        voltages = np.linspace(v_min, v_max, num_points)
        currents = []

        for v in voltages:
            i_min = float("inf")
            for pv, G, T in zip(pv_modules, G_list, T_list):
                i = pv.output(v, G, T)
                if i < i_min:
                    i_min = i
            currents.append(i_min)

        return voltages, np.array(currents)

    @staticmethod
    def plot_iv_curve(voltages, currents, title=None, xlabel="Voltage (V)", ylabel="Current (A)"):
        plt.plot(voltages, currents)
        if title is not None:
            plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()
    
    @staticmethod
    def iv_curve_series_panels(pv_modules, G_list, T_list, num_points=100, v_min=0, v_max=None, tol=1e-6, max_iter=100):
        if len(pv_modules) != len(G_list) or len(pv_modules) != len(T_list):
            raise ValueError("The length of pv_modules, G_list, and T_list must be the same.")

        if v_max is None:
            v_max = sum([pv.V_oc(G, T) for pv, G, T in zip(pv_modules, G_list, T_list)])

        voltages = np.linspace(v_min, v_max, num_points)
        currents = []

        for v in voltages:
            i_prev = float("inf")
            i_curr = 0
            iter_count = 0

            while abs(i_curr - i_prev) > tol and iter_count < max_iter:
                i_prev = i_curr
                i_curr = 0

                for pv, G, T in zip(pv_modules, G_list, T_list):
                    i_pv = pv.output(v, G, T)
                    i_curr += (i_pv - i_prev) / len(pv_modules)

                iter_count += 1

            currents.append(i_curr)

        return voltages, np.array(currents)
    
    def max_power_series_panels(pv_modules, G_list, T_list):
        if len(pv_modules) != len(G_list) or len(pv_modules) != len(T_list):
            raise ValueError("The lengths of pv_modules, G_list, and T_list must be the same.")

        v_mpp_total = 0
        i_mpp_min = float("inf")

        for pv_module, G, T in zip(pv_modules, G_list, T_list):
            v_mpp, i_mpp, _ = pv_module.max_power(G, T)
            v_mpp_total += v_mpp
            i_mpp_min = min(i_mpp_min, i_mpp)

        p_mpp_total = v_mpp_total * i_mpp_min
        return v_mpp_total, i_mpp_min, p_mpp_total
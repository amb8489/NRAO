'''
Testing file for calculating A B R X
'''
import time

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line_builder import floquet_line_builder
from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency
from utills.functions import toGHz, unfold


# ---------------------------- unit cell inputs from paper


def simulate(line_model):
    floquet_line = floquet_line_builder(line_model)
    # ---------------------------- calculations -------------------
    alpha_plt, r, x, beta_plt, beta_unfold_plt, RR, LL, GG, CC, gamma, transmission_plt = [], [], [], [], [], [], [], [], [], [], []
    cl_beta = []
    cl_alpha = []
    inputs = line_model.get_inputs()

    resoultion = int(inputs["Frequency Range"][resolution.get_name()])
    start_freq_GHz = toGHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
    end_freq_GHz = toGHz(int(inputs["Frequency Range"][end_frequency.get_name()]))

    # todo
    FRange = np.linspace(start_freq_GHz, end_freq_GHz, resoultion)

    for F in FRange:
        alpha, beta, alphaCl, betaCL, r_, x_ = floquet_line.simulate(F)
        # RR.append(R)
        # LL.append(L)
        # GG.append(G)
        # CC.append(C)
        # transmission_plt.append(thickness)
        cl_beta.append(betaCL)
        cl_alpha.append(alphaCl)
        beta_plt.append(beta)
        alpha_plt.append(alpha)
        r.append(r_)
        x.append(x_)

    # RR, LL, GG, CC, gamma = np.array(RR), np.array(LL), np.array(GG), np.array(CC), np.array(gamma)
    # I = .2
    # I3 = I * I * I
    # w = FRange * PI2
    # WW = w * w
    # CLWWI = CC * LL * WW * I
    # CRwI = CC * RR * w * I
    # GLwI = GG * LL * w * I
    # RGI = RR * GG * I
    # GLIIIwDiv3 = GG * LL * I3 * (w / 3)
    # CLIIIWWDiv3 = CC * LL * I3 * (WW / 3)
    # YYI = gamma * gamma * I  # TODO

    # ---------------------------- plots----------------------------

    # ------- test ------
    # Create some mock data

    fig1, ax1 = plt.subplots()
    ax1.set_ylabel('alpha - alpha0', color='tab:blue')


    ax1.plot(FRange, np.array(alpha_plt) - np.array(cl_alpha) , color='tab:blue')

    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_xlabel('Frequency [GHz]')
    ax2 = ax1.twinx()
    ax2.set_ylabel('beta - beta0', color='tab:orange')
    ax2.plot(FRange, np.array(unfold(beta_plt)) - np.array(unfold(cl_beta)), color='tab:orange')

    ax2.tick_params(axis='y', labelcolor='tab:orange')
    fig1.tight_layout()

    # --------------------------------------------------------------------
    fig2, ax12 = plt.subplots()
    color = 'tab:blue'
    ax12.set_ylabel('r Blue -- x orange', color=color)
    ax12.plot(FRange, r, color=color)
    ax12.tick_params(axis='y', labelcolor=color)
    ax12.set_xlabel('Frequency [GHz]')
    ax12.plot(FRange, x, color='tab:orange')
    fig2.tight_layout()

    return [fig1, fig2]

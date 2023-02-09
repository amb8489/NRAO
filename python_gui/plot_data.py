'''
Testing file for calculating A B R X
'''

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line import unfold
from python_gui.floquet_line_builder import floquet_line_builder
from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency
from utills.functions import toGHz


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
        # transmission_plt.append(t)
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
    color = 'tab:blue'
    ax1.set_ylabel('alpha - alpha0', color=color)
    ax1.plot(FRange, np.array(alpha_plt) - np.array(cl_alpha), color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlabel('Frequency [GHz]')
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('beta - beta0', color=color)
    ax2.plot(FRange, np.array(unfold(beta_plt)) - np.array(unfold(cl_beta)), color=color)
    ax2.tick_params(axis='y', labelcolor=color)
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

    # ---------------------------------

    # fig1 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    # axes1 = fig1.add_subplot(111)
    # fig1.suptitle("ALPHAS")
    # axes1.set_xlabel('Frequency [GHz]')
    # axes1.set_ylabel('Frequency [GHz]')
    # axes1.plot(FRange, alpha_plt)
    #
    # floquet_line.FindPumpZone(3, alpha_plt)
    # axes1.axvspan(FRange[int(floquet_line.target_pump_zone_start)], FRange[int(floquet_line.target_pump_zone_end)],
    #               facecolor='b', alpha=0.3)
    # axes1.axvspan(FRange[int(floquet_line.target_pump_zone_start / 3)],
    #               FRange[int(floquet_line.target_pump_zone_end / 3)],
    #               facecolor='g', alpha=0.5)
    #
    # fig2 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    # axes2 = fig2.add_subplot(111)
    # fig2.suptitle("BETAS")
    # axes2.set_xlabel('Frequency [GHz]')
    # axes2.set_ylabel('Frequency [GHz]')
    # axes2.plot(FRange, beta_plt)
    # axes2.plot(FRange, unfold(beta_plt))
    #
    # fig3 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    # axes3 = fig3.add_subplot(111)
    # fig3.suptitle("R")
    # axes3.set_xlabel('Frequency [GHz]')
    # axes3.set_ylabel('Frequency [GHz]')
    # axes3.plot(FRange, r)
    #
    # fig4 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    # axes4 = fig4.add_subplot(111)
    # fig4.suptitle("X")
    # axes4.set_xlabel('Frequency [GHz]')
    # axes4.set_ylabel('Frequency [GHz]')
    # axes4.plot(FRange, x)
    #
    # fig5 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    # axes5 = fig5.add_subplot(111)
    # fig5.suptitle("TRANSMISSION")
    # axes5.set_xlabel('Frequency [GHz]')
    # axes5.set_ylabel('Frequency [GHz]')
    # axes5.plot(FRange, transmission_plt)
    #
    # # todo
    # fig6 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    # axes6 = fig6.add_subplot(111)
    # fig6.suptitle("CIRCUIT")
    # axes6.set_xlabel('Frequency [GHz]')
    # axes6.set_ylabel('Frequency [GHz]')
    # axes6.plot(FRange, FRange)

    return [fig1, fig2]

    # return [[fig1, fig2], [fig3, fig4]]

    # return [[fig1, fig2], [fig3, fig4], [fig5, fig6]]

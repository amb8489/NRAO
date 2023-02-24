'''
Testing file for calculating A B R X
'''

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line_builder import floquet_line_builder
from hfss.read_hsff_file import hsff_simulate
from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency
from utills.functions import toGHz, unfold


# ---------------------------- unit cell inputs from paper


def mk_plots(frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x):
    plt.close()
    # -------------------ALPHA , BETA PLOTS---------------------------------

    fig1, ax1 = plt.subplots()
    ax1.set_ylabel('alpha - alpha0', color='tab:red')
    ax1.plot(frequency_range, np.array(floquet_alpha) - np.array(central_line_alpha), color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_xlabel('Frequency [GHz]')

    ax2 = ax1.twinx()
    ax2.set_ylabel('beta - beta0', color='tab:green')
    # todo for smat might need to use mk_monotinic_inc() idk
    ax2.plot(frequency_range, np.array(unfold(floquet_beta)) - np.array(unfold(central_line_beta)), color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    fig1.tight_layout()

    # ---------------------R , X PLOTS ----------------------------
    fig2, ax12 = plt.subplots()
    color = 'tab:blue'
    ax12.set_ylabel('r Blue -- x orange', color=color)
    ax12.plot(frequency_range, floquet_r, color=color)
    ax12.tick_params(axis='y', labelcolor=color)
    ax12.set_xlabel('Frequency [GHz]')
    ax12.plot(frequency_range, floquet_x, color='tab:orange')
    fig2.tight_layout()

    return [fig1, fig2]


def simulate(line_model):
    if line_model.type == "SMAT":

        frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x = __simulate_hfss(
            line_model)
    else:

        frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x = __siulate_transmission_line(
            line_model)

    return mk_plots(frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r,
                    floquet_x)


def __simulate_hfss(line_model):
    return hsff_simulate(line_model.file_path, int(line_model.n_interp_points.get_value()))


def __siulate_transmission_line(line_model):
    # ----------------------- mking  floquet_line -----------------

    floquet_line = floquet_line_builder(line_model)
    inputs = line_model.get_inputs()

    # ---------------------------- storage -------------------
    floquet_alpha, floquet_beta, floquet_r, floquet_x = [], [], [], []
    floquet_transmission_plt = []

    central_line_beta = []
    central_line_alpha = []

    # ---------------------------- simulation -------------------
    resoultion = int(inputs["Frequency Range"][resolution.get_name()])
    start_freq_GHz = toGHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
    end_freq_GHz = toGHz(int(inputs["Frequency Range"][end_frequency.get_name()]))
    frequency_range = np.linspace(start_freq_GHz, end_freq_GHz, resoultion)

    for frequency in frequency_range:
        alpha, beta, alphaCl, betaCL, r_, x_ = floquet_line.simulate(frequency)
        central_line_beta.append(betaCL)
        central_line_alpha.append(alphaCl)
        floquet_beta.append(beta)
        floquet_alpha.append(alpha)
        floquet_r.append(r_)
        floquet_x.append(x_)

    return frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x

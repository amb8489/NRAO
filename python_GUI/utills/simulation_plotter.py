'''
Testing file for calculating A B R X
'''

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line_builder import floquet_line_builder
from hfss.read_hsff_file import hsff_simulate
from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency
from utills.functions import toGHz, beta_unfold


# ---------------------------- unit cell inputs from paper


def mk_plots(frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x,
             floquet_transmission):
    plt.close()

    # scaling down so plots look nice on x axis (this does not afect any calculation , purly for looks)
    frequency_range /= 10e8
    # -------------------delta ALPHA , delta BETA PLOTS---------------------------------

    fig1, ax1 = plt.subplots()
    fig1.suptitle('αd - α0d  |  βd - β0d')
    ax1.set_ylabel('δ αd', color='tab:red')
    ax1.plot(frequency_range, np.array(floquet_alpha) - np.array(central_line_alpha), color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_xlabel('Frequency [GHz]')

    ax2 = ax1.twinx()
    ax2.set_ylabel('δ βd', color='tab:green')
    ax2.plot(frequency_range, beta_unfold(floquet_beta) - beta_unfold(central_line_beta),
             color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    fig1.tight_layout()
    ax1.legend(['αd - α0d '])
    ax2.legend([ 'βd - β0d'],loc = 'upper left')
    # ---------------------R , X PLOTS ----------------------------
    fig2, ax22 = plt.subplots()
    color = 'tab:blue'
    fig2.suptitle('Floquet R and X')
    ax22.set_ylabel('η [Ω]', color=color)
    ax22.plot(frequency_range, floquet_r, color=color)
    ax22.tick_params(axis='y', labelcolor=color)
    ax22.set_xlabel('Frequency [GHz]')
    ax22.set_ylim([-60, 300])

    ax22.plot(frequency_range, floquet_x, color='tab:orange')
    fig2.tight_layout()
    ax22.legend(['r', 'x'])


    # ---------------------Transmission PLOT ----------------------------
    fig3, ax33 = plt.subplots()
    color = 'tab:red'
    fig3.suptitle('Transmission')
    ax33.set_ylabel('Transmission', color=color)
    ax33.plot(frequency_range, floquet_transmission, color=color)
    ax33.tick_params(axis='y', labelcolor=color)
    ax33.set_xlabel('Frequency [GHz]')
    fig3.tight_layout()

    # ------------------- BETA vs BETA UNFOLDED---------------------------------

    fig4, ax44 = plt.subplots()
    color = 'tab:red'
    fig4.suptitle('Floquet Beta vs Floquet Beta Unfolded')
    ax44.plot(frequency_range, floquet_beta, color=color)
    ax44.plot(frequency_range, beta_unfold(floquet_beta))
    ax44.tick_params(axis='y', labelcolor=color)
    ax44.set_xlabel('Frequency [GHz]')
    fig4.tight_layout()

    # ------------------- central line ---------------------------------

    fig5, ax55 = plt.subplots()
    fig5.suptitle('Central line Alpha d and beta d')

    ax55.set_ylabel('α0d', color='tab:red')
    ax55.plot(frequency_range, np.array(central_line_alpha), color='tab:red')
    ax55.tick_params(axis='y', labelcolor='tab:red')
    ax55.set_xlabel('Frequency [GHz]')

    ax2 = ax55.twinx()
    ax2.set_ylabel('β0d', color='tab:green')
    ax2.plot(frequency_range, beta_unfold(central_line_beta), color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    fig5.tight_layout()

    return [fig1, fig2, fig3, fig4, fig5]


def simulate(line_model):
    if line_model.type == "SMAT":

        frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x, floquet_transmission = __simulate_hfss_file(
            line_model)
    else:
        frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x, floquet_transmission = __siulate_transmission_line(
            line_model)

    return mk_plots(frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r,
                    floquet_x, floquet_transmission)


def __simulate_hfss_file(line_model):
    return hsff_simulate(line_model.file_path, int(line_model.n_interp_points.get_value()))


def __siulate_transmission_line(line_model):
    # ----------------------- making  floquet_line -----------------

    floquet_line = floquet_line_builder(line_model)
    inputs = line_model.get_inputs()

    # ---------------------------- storage -------------------
    floquet_alpha, floquet_beta, floquet_r, floquet_x = [], [], [], []
    floquet_transmission = []

    central_line_beta = []
    central_line_alpha = []

    # ---------------------------- simulation -------------------
    resoultion = int(inputs["Frequency Range"][resolution.get_name()])
    start_freq_GHz = toGHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
    end_freq_GHz = toGHz(int(inputs["Frequency Range"][end_frequency.get_name()]))
    frequency_range = np.linspace(start_freq_GHz, end_freq_GHz, resoultion)

    for frequency in frequency_range:
        alpha, beta, alphaCl, betaCL, r_, x_, floquet_transmission_ = floquet_line.simulate(frequency)
        central_line_beta.append(betaCL)
        central_line_alpha.append(alphaCl)
        floquet_beta.append(beta)
        floquet_alpha.append(alpha)
        floquet_r.append(r_)
        floquet_x.append(x_)
        floquet_transmission.append(floquet_transmission_)

    return frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x, floquet_transmission

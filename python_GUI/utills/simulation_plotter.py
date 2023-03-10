'''
Testing file for calculating A B R X
'''

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line_builder import floquet_line_builder
from gain_models.multiprocessing_gain_simulate import simulate_gain_multiprocesses
from hfss.read_hsff_file import hsff_simulate
from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency
from utills.functions import toGHz, beta_unfold


# ---------------------------- unit cell inputs from paper


def mk_plots(frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x,
             floquet_transmission,gain_data):
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

    ax22.plot(frequency_range, floquet_x, '--',color='tab:orange')
    fig2.tight_layout()
    ax22.legend(['r', 'x'])

    # ------------------- BETA vs BETA UNFOLDED---------------------------------

    fig4, ax44 = plt.subplots()
    color = 'tab:red'
    fig4.suptitle('Floquet Beta vs Floquet Beta Unfolded')
    ax44.plot(frequency_range, floquet_beta, color=color)
    ax44.plot(frequency_range, beta_unfold(floquet_beta))
    ax44.tick_params(axis='y', labelcolor=color)
    ax44.set_xlabel('Frequency [GHz]')
    fig4.tight_layout()
    # ---------------------Alpha vs Transmission  PLOT ----------------------------

    fig5, ax55 = plt.subplots(2)
    fig5.suptitle('Alpha and Transmission')

    ax55[0].set_ylabel('α0d', color='tab:red')
    ax55[0].plot(frequency_range,np.array(floquet_alpha) - np.array(central_line_alpha), color='tab:red')

    ax55[0].tick_params(axis='y', labelcolor='tab:red')
    ax55[1].set_ylabel('Transmission', color='tab:blue')
    ax55[1].plot(frequency_range, floquet_transmission, color='tab:blue')
    ax55[1].tick_params(axis='y', labelcolor='tab:blue')
    ax55[1].set_xlabel('Frequency [GHz]')


    fig3, ax33 = plt.subplots()
    fig3.suptitle('Transmission')
    ax33.set_ylabel('α0d', color='tab:red')
    ax33.plot(frequency_range, floquet_transmission, color='tab:blue')
    ax33.tick_params(axis='y', labelcolor='tab:red')


    #----------- GAIN ---------

    gain,gain_meta_data = gain_data

    gain_freq_range,PUMP_FREQUENCY,n_unitcells,pump_current = gain_meta_data
    fig6, ax66 = plt.subplots()
    plt.suptitle(f"[Pump Freq: {PUMP_FREQUENCY} GHz] [# cells: {n_unitcells}] [pump current: {pump_current.real}]")
    ax66.plot(gain_freq_range/ 1e8, gain, '-', color='tab:orange')
    ax66.set_ylim([None, None])
    ax66.set_title(f"SIGNAL GAIN [Db]")
    ax66.set_xlabel('Frequency [GHz]')

    return [fig1,fig2,
            fig5,fig4,
            fig6]


def simulate(line_model):
    if line_model.type == "SMAT":

        frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x, floquet_transmission,gain_data = __simulate_hfss_file(
            line_model)
    else:
        frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r, floquet_x, floquet_transmission,gain_data = __simulate_transmission_line(
            line_model)

    return mk_plots(frequency_range, floquet_alpha, central_line_alpha, floquet_beta, central_line_beta, floquet_r,
                    floquet_x, floquet_transmission,gain_data)


def __simulate_hfss_file(line_model):
    return hsff_simulate(line_model.file_path, int(line_model.n_interp_points.get_value()))


def __simulate_transmission_line(line_model):
    # ----------------------- making  floquet_line -----------------

    floquet_line = floquet_line_builder(line_model)
    inputs = line_model.get_inputs()

    # ---------------------------- storage -------------------
    floquet_alpha_d, floquet_beta_d, floquet_r, floquet_x = [], [], [], []
    floquet_transmission = []
    central_line_beta = []
    central_line_alpha = []

    # ---------------------------- simulation -------------------
    resoultion = int(inputs["Frequency Range"][resolution.get_name()])
    start_freq_GHz = toGHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
    end_freq_GHz = toGHz(int(inputs["Frequency Range"][end_frequency.get_name()]))
    frequency_range = np.linspace(start_freq_GHz, end_freq_GHz, resoultion)

    for frequency in frequency_range:
        alpha_d, beta_d, alpha_d_CL, beta_d_CL, r, x, transmission_ = floquet_line.simulate(frequency)
        central_line_beta.append(beta_d_CL)
        central_line_alpha.append(alpha_d_CL)
        floquet_beta_d.append(beta_d)
        floquet_alpha_d.append(alpha_d)
        floquet_r.append(r)
        floquet_x.append(x)
        floquet_transmission.append(transmission_)


    unit_cell_length = floquet_line.get_unit_cell_length()
    n_unitcells = 150
    PUMP_FREQ = 11.33
    I_star = 1
    init_amplitudes = [complex(1e-7,0),complex(0,0),complex(.2*I_star,0)]


    gain,gain_freq_range = simulate_gain_multiprocesses(resoultion, unit_cell_length, n_unitcells, frequency_range, PUMP_FREQ, init_amplitudes, I_star,
                                                        floquet_beta_d, floquet_alpha_d, floquet_r, floquet_x)


    gain_data = (gain,(gain_freq_range,PUMP_FREQ,n_unitcells,init_amplitudes[2]))

    return frequency_range,\
           floquet_alpha_d,\
           central_line_alpha,\
           floquet_beta_d,\
           central_line_beta,\
           floquet_r,\
           floquet_x,\
           floquet_transmission,\
           gain_data
'''



    this file will fun the simulation to make the plots that end up getting shown on
    plot_window.py





'''

import numpy as np
from matplotlib import pyplot as plt

from simulation.floquet_line_models.floquet_line_builder_new import floquet_line_from_line_model
from simulation.gain_models.multiprocessing_gain_simulate import simulate_gain_multiprocessing
from simulation.utills.constants import PI2
from simulation.utills.functions import beta_unfold, RLGC_circuit_factors, hertz_to_GHz


# ---------------------------- unit cell inputs from paper


def mk_plots(frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission,
             gain_data, fl):
    gamma_d = np.array(gamma_d)
    bloch_impedance = np.array(bloch_impedance)

    floquet_alpha = np.real(gamma_d)
    floquet_beta = np.imag(gamma_d)
    floquet_r = np.real(bloch_impedance)
    floquet_x = np.imag(bloch_impedance)

    plt.close()

    figs = []

    # scaling down so plots look nice on x axis (this does not afect any calculation , purly for looks)
    frequency_range /= 10e8
    # -------------------delta ALPHA , delta BETA PLOTS---------------------------------

    fig1, ax1 = plt.subplots()
    fig1.suptitle('αd - α0d  |  βd - β0d')
    ax1.set_ylabel('δ αd', color='tab:red')
    ax1.plot(frequency_range, np.array(floquet_alpha) - np.array(central_line_alpha_d), color='tab:red')

    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_xlabel('Frequency [GHz]')

    ax2 = ax1.twinx()
    ax2.set_ylabel('δ βd', color='tab:green')
    ax2.plot(frequency_range, beta_unfold(floquet_beta) - beta_unfold(central_line_beta_d),
             color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    fig1.tight_layout()
    ax1.legend(['αd - α0d '], loc='upper right')
    ax2.legend(['βd - β0d'], loc='upper left')
    figs.append(fig1)

    # ---------------------R , X PLOTS ----------------------------
    fig2, ax22 = plt.subplots()
    color = 'tab:blue'
    fig2.suptitle('Floquet R and X')
    ax22.set_ylabel('η [Ω]', color=color)
    ax22.plot(frequency_range, floquet_r, color=color)
    ax22.tick_params(axis='y', labelcolor=color)
    ax22.set_xlabel('Frequency [GHz]')
    ax22.set_ylim([-60, 300])

    ax22.plot(frequency_range, floquet_x, '--', color='tab:orange')
    fig2.tight_layout()
    ax22.legend(['r', 'x'])
    figs.append(fig2)

    # ------------------- BETA vs BETA UNFOLDED---------------------------------

    fig4, ax44 = plt.subplots()
    color = 'tab:red'
    fig4.suptitle('Floquet Beta vs Floquet Beta Unfolded')
    ax44.plot(frequency_range, floquet_beta, color=color)
    ax44.plot(frequency_range, beta_unfold(floquet_beta))
    ax44.tick_params(axis='y', labelcolor=color)
    ax44.set_xlabel('Frequency [GHz]')
    fig4.tight_layout()
    # figs.append(fig4)

    # ---------------------Alpha vs Transmission  PLOT ----------------------------

    fig5, ax55 = plt.subplots(2)
    fig5.suptitle('Alpha and Transmission')
    ax55[0].set_ylabel('α0d', color='tab:red')
    ax55[0].plot(frequency_range, np.array(floquet_alpha) - np.array(central_line_alpha_d), color='tab:red')
    ax55[0].tick_params(axis='y', labelcolor='tab:red')
    ax55[1].set_ylabel('Transmission', color='tab:blue')
    ax55[1].plot(frequency_range, floquet_transmission, color='tab:blue')
    ax55[1].tick_params(axis='y', labelcolor='tab:blue')
    ax55[1].set_xlabel('Frequency [GHz]')
    figs.append(fig5)

    fig3, ax33 = plt.subplots()
    fig3.suptitle('Transmission')
    ax33.set_ylabel('α0d', color='tab:red')
    ax33.plot(frequency_range, floquet_transmission, color='tab:blue')
    ax33.tick_params(axis='y', labelcolor='tab:red')
    figs.append(fig3)

    # ----------- GAIN ---------
    fig6, ax66 = plt.subplots()
    if gain_data:
        gain, gain_meta_data = gain_data
        pump_range, PUMP_FREQUENCY, n_unitcells, pump_current = gain_meta_data

        plt.suptitle(
            f"[Pump Freq: {PUMP_FREQUENCY / 1e9} GHz] [# cells: {n_unitcells}] [pump current: {pump_current.real}]")
        ax66.plot(pump_range * 1E9, gain, '-', color='tab:orange')
        ax66.set_ylim([None, None])
        ax66.set_xlim([0, (2 * PUMP_FREQUENCY)])
        ax66.set_title(f"SIGNAL GAIN [Db]")
        ax66.set_xlabel('Frequency [GHz]')
        figs.append(fig6)

    # ----------- jav's RLGC circuit factors ---------
    fig7, ax77 = plt.subplots()

    # todo does jav use beta*d or just beta and do we unfold beta before putting in RLGC_circuit_factors





    # from javiar code
    omega = PI2 * frequency_range
    b = 2 * beta_unfold(gamma_d)
    a = 2 * floquet_alpha
    gd = a + 1j * b
    R, L, G, C = RLGC_circuit_factors(gd, bloch_impedance, omega)
    I = .1

    EngTerm1 = np.abs(beta_unfold(gamma_d / fl.get_unit_cell_length()) ** 2 * I)
    EngTerm2 = np.abs(C * L * omega ** 2 * I)
    EngTerm3 = np.abs(C * R * omega * I)
    EngTerm4 = np.abs(G * L * omega * I)
    EngTerm5 = np.abs(R * G * I)
    EngTerm6 = np.abs(L * G * omega / 3 * (I ** 3))
    EngTerm7 = np.abs(L * C * omega ** 2 / 3 * (I ** 3))

    ax77.plot(frequency_range, EngTerm1, color='darkslategray', label='$\gamma^2 I$')
    ax77.plot(frequency_range, EngTerm2, '--', color='c', label='$CL_0\omega^2 I$', ls='--')
    ax77.plot(frequency_range, EngTerm3, color='tab:orange', label='$CR\omega$ I')
    ax77.plot(frequency_range, EngTerm4, '--', color='tab:red', label='$GL_0\omega I$')
    ax77.plot(frequency_range, EngTerm5, color='tab:purple', label='$RG I$')
    ax77.plot(frequency_range, EngTerm6, color='tab:brown', label='$GL_0 I^3 \omega/3$')
    ax77.plot(frequency_range, EngTerm7, color='navy', label='$CL_0 I^3 \omega^2/3$')
    ax77.set_xlabel('Frequency [GHz]')
    ax77.set_yscale('log')
    ax77.legend(loc='lower right', ncol=2)
    figs.append(fig7)

    # list of figures to display in GUI
    return figs


def pre_sim(line_model):
    # todo add in gain

    floquet_line = floquet_line_from_line_model(line_model)

    if line_model.type == "HFSS_TOUCHSTONE_FILE":
        frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission = floquet_line.simulate_over_frequency_range()
    else:
        inputs = line_model.get_inputs()
        frequecy_data = inputs.get("Frequency_Range", {})
        start_frequency = hertz_to_GHz(float(frequecy_data.get("Start Frequency")))
        end_frequency = hertz_to_GHz(float(frequecy_data.get("End Frequency")))
        delta_f = hertz_to_GHz(float(frequecy_data.get("Resolution")))
        frequency_range = np.arange(start_frequency, end_frequency, delta_f)

        frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission = floquet_line.simulate_over_frequency_range(
            frequency_range)

    # todo refactor this into a new gain function
    inputs = line_model.get_inputs()
    gain_properties = inputs.get("gain_properties", {})
    should_calc_gain = bool(int(gain_properties.get('calc_gain')))
    s_amp_0 = float(gain_properties.get('Signal Amplitude'))
    i_amp_0 = float(gain_properties.get('Idler Amplitude'))
    p_amp_0 = float(gain_properties.get('Pump Amplitude'))
    pump_frequency = hertz_to_GHz(float(gain_properties.get('Pump Frequency')))
    gain_data = None
    if should_calc_gain:
        unit_cell_length = floquet_line.get_unit_cell_length()
        n_unit_cells = floquet_line.get_n_repeated_cells()
        init_amplitudes = [s_amp_0 + 0j, i_amp_0 + 0j, p_amp_0 + 0j]
        I_star = 1

        res = len(frequency_range)
        gain, pump_range = simulate_gain_multiprocessing(res, unit_cell_length, n_unit_cells,
                                                         frequency_range,
                                                         pump_frequency, init_amplitudes, I_star,
                                                         gamma_d, bloch_impedance)

        gain_data = (gain, (pump_range, pump_frequency, n_unit_cells, init_amplitudes[2]))

    return frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission, gain_data, floquet_line


def simulate(line_model):
    """

    this function is called from the GUI code, and given a line model made from the GUI, it will
    run the appropriate simulation for that line type

    :param line_model: from the GUI that holds all the user inputs from the GUI
    :return: matpltlib figures 1d list
    """
    if line_model.type in ["HFSS_TOUCHSTONE_FILE", "PRE_SIM_FILE"]:
        frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission, gain_data, fl = pre_sim(
            line_model)

    else:
        frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, \
        central_line_beta_d, floquet_transmission, gain_data, fl = __simulate_floquet_line(line_model)

    return mk_plots(frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d,
                    floquet_transmission, gain_data, fl)


def __simulate_floquet_line(line_model):
    """

    # todo document and comments steps that hapen in this function
    # todo model input checking and catching any errors raised
    # todo rename gamma_d and bloch_impedance to indicate its a list of bloch_impedance and gama_d

    :param line_model:
    :return: characteristics of a floquet line at a given frequency
    """
    # ----------------------- making the right floquet_line given GUI inputs -----------------

    inputs = line_model.get_inputs()
    frequecy_data = inputs.get("frequency_range", {})
    gain_properties = inputs.get("gain_properties", {})

    start_frequency = hertz_to_GHz(float(frequecy_data.get("Start Frequency")))
    end_frequency = hertz_to_GHz(float(frequecy_data.get("End Frequency")))
    delta_f = hertz_to_GHz(float(frequecy_data.get("Resolution")))

    should_calc_gain = bool(int(gain_properties.get('calc_gain')))
    s_amp_0 = float(gain_properties.get('Signal Amplitude'))
    i_amp_0 = float(gain_properties.get('Idler Amplitude'))
    p_amp_0 = float(gain_properties.get('Pump Amplitude'))
    pump_frequency = hertz_to_GHz(float(gain_properties.get('Pump Frequency')))
    frequency_range = np.arange(start_frequency, end_frequency, delta_f)

    floquet_line = floquet_line_from_line_model(line_model)

    gamma_d, \
    bloch_impedance, central_line_alpha_d, \
    central_line_beta_d, floquet_transmission = \
        floquet_line.simulate_over_frequency_range(frequency_range)

    # only run if gain was selected in GUI

    gain_data = None
    if should_calc_gain:
        unit_cell_length = floquet_line.get_unit_cell_length()
        n_unit_cells = floquet_line.get_n_repeated_cells()
        init_amplitudes = [s_amp_0 + 0j, i_amp_0 + 0j, p_amp_0 + 0j]
        I_star = 1

        res = len(frequency_range)
        gain, pump_range = simulate_gain_multiprocessing(res, unit_cell_length, n_unit_cells,
                                                         frequency_range,
                                                         pump_frequency, init_amplitudes, I_star,
                                                         gamma_d, bloch_impedance)

        gain_data = (gain, (pump_range, pump_frequency, n_unit_cells, init_amplitudes[2]))

    return frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, \
           central_line_beta_d, floquet_transmission, gain_data, floquet_line

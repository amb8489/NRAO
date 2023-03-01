import cmath

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

import utills.functions
from floquet_line_model.floquet_line import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine


def __CalculateBetas(floquet_line, freq_range):
    return [floquet_line.simulate(f)[1] for f in freq_range]


def __get_closest_betas_at_given_freq(master, targets, betas):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta

    sorted_keys = np.argsort(master)
    return betas[sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys)]]


def __get_closest_betas_at_given_freq_slow(master, targets, betas):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta

    res = {}
    for f in targets:
        # the idx of the cloest frequency in master to f
        idx_of_closest_freq_t_f_in_master = np.abs(master - f).argmin()

        # the closest freq in master to f
        closest_freq_t_f_in_master = master[idx_of_closest_freq_t_f_in_master]

        # the beta to that frequency
        res[closest_freq_t_f_in_master] = betas[idx_of_closest_freq_t_f_in_master]

        print(closest_freq_t_f_in_master)

    return res


def ODE_model_1(z, init_amplitudes, beta_s, beta_i, beta_p, delta_beta, I_Star):
    # signal-idler-pump equations for N = 3
    amp_S, amp_I, amp_P = init_amplitudes

    As_div_istar = 1j * (-beta_s / (8 * I_Star ** 2)) * (
            amp_S * (abs(amp_S) ** 2 + 2 * abs(amp_I) ** 2 + 2 * abs(amp_P) ** 2)
            + amp_I.conjugate() * amp_P ** 2 * cmath.exp(1j * delta_beta * z))

    Ai_div_istar = 1j * (-beta_i / (8 * I_Star ** 2)) * (
            amp_I * (2 * abs(amp_S) ** 2 + abs(amp_I) ** 2 + 2 * abs(amp_P) ** 2)
            + amp_S.conjugate() * amp_P ** 2 * cmath.exp(1j * delta_beta * z))

    Ap_div_istar = 1j * (-beta_p / (8 * I_Star ** 2)) * (
            amp_P * (2 * abs(amp_S) ** 2 + 2 * abs(amp_I) ** 2 + abs(amp_P) ** 2)
            + 2 * amp_P.conjugate() * amp_S * amp_I * cmath.exp(-1j * delta_beta * z))

    return [As_div_istar, Ai_div_istar, Ap_div_istar]


json_inputs = {'SC': {'Er': 11.44, 'Height': 0.0, 'Ts': 35.0, 'Ground Thickness': 0.0,
                      'Super Conductor Operation Temperature': 4.0, 'Super Conductor Critical Temperature': 14.7,
                      'Super Conductor Critical Current': 0.0, 'Super Conductor Normal Resistivity': 100.0,
                      'Super Conductor Tangent Delta': 0.0},
               'Dimensions': {'loads': [['60', '3.4'], ['60', '3.4'], ['50', '3.4']], 'Unit Cell Length': 4.734,
                              'Central Line Width': 1.0, 'D0': 1.578, 'S': 1.0},
               'Frequency Range': {'Start Frequency': 0.0, 'End Frequency': 40.0, 'Resolution': 1000.0},
               'gain_models': {'Signal Amplitude': 0.0, 'Idler Amplitude': 0.0, 'Pump Amplitude': 0.0,
                               'Pump Frequency': 0.0}}

inputs = CPWInputs(json_inputs)

super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)

central_line_model = SuperConductingCPWLine(inputs.central_line_width, inputs.ground_spacing,
                                            inputs.line_thickness, inputs.er, inputs.tangent_delta)
load_line_models = [SuperConductingCPWLine(load_width, inputs.ground_spacing, inputs.line_thickness, inputs.er,
                                           inputs.tangent_delta) for load_width in inputs.load_widths]

floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals,
                                          load_line_models, central_line_model, super_conductivity_model,
                                          inputs.central_line_width, inputs.load_widths, inputs.line_thickness,
                                          inputs.crit_current)

########################################################################################

nCells = 150
t_eval = np.linspace(0, floquet_line.unit_cell.unit_cell_length * nCells, inputs.resoultion)
PUMP_FREQUENCY = utills.functions.toGHz(11.63)

as0 = 1e-7 + 0j
ai0 = 0.1 + 0j
ap0 = 0.0 + 0j

L = 500
I_Star = 1
########################################################################################

# get and unfold betas
frequency_range = np.linspace(inputs.start_freq_GHz, 2 * PUMP_FREQUENCY, inputs.resoultion)

betas = utills.functions.beta_unfold(__CalculateBetas(floquet_line, frequency_range))

# betas for signal idler Pump at each frequency
betas_signal = betas

inital_amplitudes = [as0, ai0, ap0]
gain_sig = []
gain_idler = []
gain_pump = []
z_span = (t_eval[0], t_eval[-1])

# for each frequency find the gain
def get_closest_beta_for_idler_freq(freq):
    return betas[np.abs(frequency_range - freq).argmin()]


def get_closest_beta_for_pump_freq(freq):

    return betas[np.abs(frequency_range - freq).argmin()]

for f_idx, sim_frequency in enumerate(frequency_range):
    beta_signal = betas_signal[f_idx]

    beta_idler = get_closest_beta_for_idler_freq(2 * PUMP_FREQUENCY - sim_frequency)

    beta_pump = get_closest_beta_for_pump_freq(PUMP_FREQUENCY)

    delta_beta = beta_signal + beta_idler - 2 * beta_pump

    args = (beta_signal, beta_idler, beta_pump, delta_beta, I_Star)
    sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=t_eval)

    amp_signal, amp_idler, amp_pump = sol.y
    gain_sig.append(amp_signal[L])
    gain_idler.append(amp_idler[L])
    gain_pump.append(amp_pump[L])

fig, ax = plt.subplots(3)

# set data with subplots and plot
ax[0].plot(frequency_range, gain_sig)
ax[0].set_title("SIGNAL")
ax[1].plot(frequency_range, gain_idler)
ax[1].set_title("IDLER")
ax[2].plot(frequency_range, gain_pump)
ax[2].set_title("PUMP")

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.294)

fig.set_size_inches(7, 7)

plt.show()

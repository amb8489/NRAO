import math

import numpy as np
from scipy.integrate import solve_ivp

import utills.functions
from floquet_line_model.floquet_line import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine


def ODE_model_1(z, inital_amplitudes, arg1, arg2, arg3):
    as0, ai0, ap0 = inital_amplitudes
    return []


def solve(z_span, inital_amplitudes, args, t_eval):
    # todo dont know about t_eval to e z or frequency
    sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=t_eval)
    return sol


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


def __CalculateBetas(floquet_line, freq_range):
    return [floquet_line.simulate(f)[1] for f in freq_range]


def __get_closest_betas_at_given_freq(master, targets, betas):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta

    sorted_keys = np.argsort(master)
    return betas[sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys)]]


########################################################################################
t_eval = np.linspace(0, floquet_line.unit_cell.unit_cell_length, inputs.resoultion)
z_span = (t_eval[0], t_eval[-1])
PUMP_FREQUENCY = utills.functions.toGHz(11.63)
########################################################################################

# range of frequency's to simulate over
frequency_range = np.linspace(inputs.start_freq_GHz, max(inputs.end_freq_GHz, 2 * PUMP_FREQUENCY), inputs.resoultion)

# get and unfold betas
betas = utills.functions.beta_unfold(__CalculateBetas(floquet_line, frequency_range))

# betas for signal idler Pump at each frequency
betas_signal = betas
betas_pump = __get_closest_betas_at_given_freq(frequency_range, np.full(inputs.resoultion, PUMP_FREQUENCY), betas)
betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY - frequency_range), betas)

# delta beta
delta_betas = betas_signal + betas_idler - 2 * betas_pump

as0, ai0, ap0 = [..., ..., ...]

for f_idx,frequency in enumerate(frequency_range):
    inital_amplitudes = [as0, ai0, ap0]

    args = (..., ..., ...,...)
    sol = solve(z_span, inital_amplitudes, args, t_eval)


def AmplitudeEqs1(z, init_amplitudes, beta_s, beta_i, beta_p, delta_beta):

    #todo make sure beta_s, beta_i, beta_p, delta_beta are commng in okay

    # signal-idler-pump equations for N = 3
    amp_S, amp_I, amp_P = init_amplitudes

    conj_amp_S = amp_S.conjugate()
    conj_amp_I = amp_I.conjugate()
    conj_amp_P = amp_P.conjugate()

    As_div_istar = -1j * (beta_s / 8) * (amp_S * (abs(amp_S) ** 2 + 2 * abs(amp_I) ** 2 + 2 * abs(amp_P) ** 2)
                                         + conj_amp_I * amp_P ** 2 * math.exp(1j * delta_beta * z))

    Ai_div_istar = -1j * (beta_i / 8) * (amp_I * (2 * abs(amp_S) ** 2 + abs(amp_I) ** 2 + 2 * abs(amp_P) ** 2)
                                         + conj_amp_S * amp_P ** 2 * math.exp(1j * delta_beta * z))

    Ap_div_istar = -1j * (beta_p / 8) * (amp_P * (2 * abs(amp_S) ** 2 + 2 * abs(amp_I) ** 2 + abs(amp_P) ** 2)
                                         + 2 * conj_amp_P * amp_S * amp_I * math.exp(1j * delta_beta * z))

    return [As_div_istar, Ai_div_istar, Ap_div_istar]

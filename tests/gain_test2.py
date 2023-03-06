import time
from cmath import exp

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

import utills.functions
from floquet_line_model.floquet_line import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine


def calculate_betasD_over_range(floquet_line, freq_range):
    return [floquet_line.simulate(f)[1] for f in freq_range]


def __get_closest_betas_at_given_freq(master, targets, betas):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta

    # # # todo could interpolate more values
    # x_org =  np.linspace(0, resolution, resolution)
    # x_interp = np.linspace(0, resolution, resolution*2)
    # master = np.interp(x_interp, x_org, master)
    # betas = np.interp(x_interp, x_org, betas)










    sorted_keys = np.argsort(master)
    return betas[sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys)]]


def ODE_model_1(z, init_amplitudes, beta_s, beta_i, beta_p, delta_betaD, I_Star):
    # signal-idler-pump equations for N = 3
    amp_S, amp_I, amp_P = init_amplitudes

    abs_ampS_sqrd = abs(amp_S) ** 2
    abs_ampI_sqrd = abs(amp_I) ** 2
    abs_ampP_sqrd = abs(amp_P) ** 2


    I_Star_sqrd = I_Star ** 2

    j_db1_z = 1j * delta_betaD * z

    eight_is_sqred = (8 * I_Star_sqrd)

    As = ((1j * -beta_s / eight_is_sqred)
          * (amp_S * (abs_ampS_sqrd + 2 * abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_I.conjugate() * amp_P ** 2 * exp(j_db1_z)))

    Ai = ((1j * -beta_i / eight_is_sqred)
          * (amp_I * (2 * abs_ampS_sqrd + abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_S.conjugate() * amp_P ** 2 * exp(j_db1_z)))

    Ap = ((1j * -beta_p / eight_is_sqred)
          * (amp_P * (2 * abs_ampS_sqrd + 2 * abs_ampI_sqrd + abs_ampP_sqrd)
             + 2 * amp_P.conjugate() * amp_S * amp_I * exp(-j_db1_z)))

    return [As, Ai, Ap]


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
                                            inputs.line_thickness, inputs.er, inputs.tangent_delta, inputs.crit_current)
load_line_models = [SuperConductingCPWLine(load_width, inputs.ground_spacing, inputs.line_thickness, inputs.er,
                                           inputs.tangent_delta, inputs.crit_current) for load_width in
                    inputs.load_widths]

floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals, load_line_models,
                                          central_line_model, super_conductivity_model, inputs.central_line_width,
                                          inputs.load_widths, inputs.line_thickness)
unit_cell_length = floquet_line.unit_cell.unit_cell_length
################################## GAIN PARAMS #######################################
resolution = 5000

n_unitcells = 150
z_eval = np.linspace(0, unit_cell_length * n_unitcells, resolution)
PUMP_FREQUENCY = utills.functions.toGHz(11.63)

I_star = 1  # todo i star val ??

as0 = 0.0000001 + 0j
ai0 = 0 + 0j
ap0 = .2 * I_star + 0j


inital_amplitudes = [as0, ai0, ap0]
z_span = (z_eval[0], z_eval[-1])

print("z/d = ", z_eval[-1] / floquet_line.unit_cell.unit_cell_length,f"init amplitudes s i p : {inital_amplitudes}")

########################################################################################


# 1) get frequencys to simulate over
frequency_range = np.linspace(0, 2 * PUMP_FREQUENCY, resolution)

# 2) simulate batas and unfold betas  #todo / by unit cll len to make betaD to beta
print(f"calculating {resolution} betas...")
s = time.time()
betas_unfolded = utills.functions.beta_unfold(
    calculate_betasD_over_range(floquet_line, frequency_range)) / unit_cell_length
print(f"{resolution} betas complete in {time.time() - s} seconds")

#
# get betas for pump, idler, delta, and  betas
betas_signal = betas_unfolded
betas_pump = __get_closest_betas_at_given_freq(frequency_range, [PUMP_FREQUENCY] * resolution, betas_unfolded)
betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY - frequency_range),
                                                betas_unfolded)
delta_betas = betas_signal + betas_idler - 2 * betas_pump




power_gain, gain_idler, gain_pump = [], [], []
fix1, ax1 = plt.subplots(3)
fix1.set_size_inches(8, 8)
ax1[0].set_title("signal")
ax1[1].set_title("idler")
ax1[2].set_title("pump")

for f_idx in range(len(frequency_range)):
    args = (betas_signal[f_idx], betas_idler[f_idx], betas_pump[f_idx], delta_betas[f_idx], I_star)
    sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=z_eval)
    amplitude_signal, amplitude_idler, amplitude_pump = sol.y

    signal_amplitude_before = amplitude_signal[0]
    signal_amplitude_after = amplitude_signal[-1]

    power_gain.append(20 * np.log10(abs(signal_amplitude_after) / abs(signal_amplitude_before)))

    if f_idx % (len(frequency_range) // 10) == 0:
        ax1[0].plot(np.abs(amplitude_signal) ** 2)
        ax1[1].plot(np.abs(amplitude_idler) ** 2)
        ax1[2].plot(np.abs(amplitude_pump) ** 2)
        print(f"{f_idx / len(frequency_range) * 100}% complete")

plt.show()

#
#
#
#
#
#
#
#
# plot gain signal

fig, ax = plt.subplots()
plt.suptitle(f"Frequency Pump: {PUMP_FREQUENCY / 1e9} GHz")

ax.plot(frequency_range / 10e9, power_gain)
ax.set_ylim([0, None])

ax.set_title(f"SIGNAL GAIN [Db]")
fig.set_size_inches(7, 7)
ax.set_xlabel('Frequency [GHz]')
plt.show()

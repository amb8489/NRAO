import math
from cmath import exp

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

import utills.functions
from floquet_line_model.floquet_line import SuperConductingFloquetLine
from hfss.read_hsff_file import hsff_simulate
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine
from utills.constants import PI



################################################################################################################################################

def get_betas_d(filepath,resolution):
    frequency_range, _,_, floquet_betas, _, _, _,_ = hsff_simulate(filepath, resolution)

    return frequency_range,floquet_betas


def __get_closest_betas_at_given_freq(master, targets, betas_unfolded):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta

    x_org = np.linspace(0, resolution, resolution)
    x_interp = np.linspace(0, resolution, resolution * 2)
    master = np.interp(x_interp, x_org, master)
    betas_unfolded = np.interp(x_interp, x_org, betas_unfolded)

    sorted_keys = np.argsort(master)
    return betas_unfolded[sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys)]]


def ODE_model_1(z, init_amplitudes, beta_s, beta_i, beta_p, delta_beta, I_Star):
    # signal-idler-pump equations for N = 3


    amp_S, amp_I, amp_P = init_amplitudes

    abs_ampS_sqrd = abs(amp_S) ** 2
    abs_ampI_sqrd = abs(amp_I) ** 2
    abs_ampP_sqrd = abs(amp_P) ** 2



    I_Star_sqrd = I_Star ** 2

    j_db1_z = (1j * delta_beta*z)

    eight_is_sqred = (8 * I_Star_sqrd)

    As = (((-1j * beta_s) / eight_is_sqred)
          * (amp_S * (abs_ampS_sqrd + 2 * abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_I.conjugate() * amp_P ** 2 * exp(j_db1_z)))

    Ai = (((-1j * beta_i) / eight_is_sqred)
          * (amp_I * (2 * abs_ampS_sqrd + abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_S.conjugate() * amp_P ** 2 * exp(j_db1_z)))

    Ap = (((-1j * beta_p) / eight_is_sqred)
          * (amp_P * (2 * abs_ampS_sqrd + 2 * abs_ampI_sqrd + abs_ampP_sqrd)
             + 2 * amp_P.conjugate() * amp_S * amp_I * exp(-j_db1_z)))

    return [As, Ai, Ap]


################################## GAIN PARAMS #######################################
unit_cell_length = 0.003140
resolution = 1000
n_unitcells = 62
z_eval = np.linspace(0, (unit_cell_length * n_unitcells), resolution)
PUMP_FREQUENCY = utills.functions.toGHz(3.284)

I_star = 1  # todo i star val ??

as0 = 1e-9+ 0j
ai0 = 0 + 0j
ap0 = .12 * I_star + 0j

inital_amplitudes = [as0, ai0, ap0]
z_span = (z_eval[0], z_eval[-1])
print("z/d = ", z_eval[-1] / unit_cell_length)

########################################################################################

frequency_range,betas_d = get_betas_d("/Users/aaron/PycharmProjects/NRAO/python_gui/Artificial_03_Artificial_UnitCell_Df=0.1GHz.s2p",resolution)
print(len(frequency_range))

betas_unfolded = utills.functions.beta_unfold(betas_d)/unit_cell_length

# plt.plot(betas_unfolded)
# plt.show()
# get betas for pump, idler, delta, and  betas
betas_signal = betas_unfolded
betas_pump = __get_closest_betas_at_given_freq(frequency_range, [PUMP_FREQUENCY] * resolution, betas_unfolded)
betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY - frequency_range), betas_unfolded)
delta_betas = betas_signal + betas_idler - 2 * betas_pump





power_gain, gain_idler, gain_pump = [], [], []

frequency_range = frequency_range[np.where(frequency_range <= 2*PUMP_FREQUENCY)]
for f_idx,freq in enumerate(frequency_range):

    args = (betas_signal[f_idx], betas_idler[f_idx], betas_pump[f_idx], delta_betas[f_idx], I_star)

    zstep = (z_eval[-1] - 0) / (len(z_eval) - 1)
    sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=z_eval ,max_step=zstep)
    amplitude_signal_over_z_range, amplitude_idler_over_z_range, amplitude_pump_over_z_range = sol.y
    signal_amplitude_before = amplitude_signal_over_z_range[0]
    signal_amplitude_after = amplitude_signal_over_z_range[-1]

    power_gain.append(10 * np.log10(abs(signal_amplitude_after) / abs(signal_amplitude_before)))




    ds = np.abs(amplitude_signal_over_z_range)
    di = np.abs(amplitude_idler_over_z_range)
    dp = np.abs(amplitude_pump_over_z_range)

    if f_idx %10 == 0:
        print(f"{int(f_idx / len(frequency_range) * 100)}% complete")





fig, ax = plt.subplots()
plt.suptitle(f"Frequency Pump: {PUMP_FREQUENCY / 1e9} GHz")
# ax.plot(frequency_range / 1e9, power_gain,'-',color='tab:orange')
ax.plot(frequency_range/ 1e9, power_gain, '-', color='tab:orange')
ax.set_ylim([None, None])
ax.set_title(f"SIGNAL GAIN [10*log10]")
fig.set_size_inches(7, 7)
ax.set_xlabel('Frequency [GHz]')
plt.show()

import csv

fields = ['Frequency', 'Gain-DB']
rows = list(zip(frequency_range,power_gain))

with open(f'../../../Desktop/gain__ap0:{ap0}___Pumpf:{PUMP_FREQUENCY/1e9}', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(rows)

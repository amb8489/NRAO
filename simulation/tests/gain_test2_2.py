import math
import time
from cmath import exp

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

import utills.functions
from floquet_line_model.floquet_line_MS_CPW import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine
from utills.constants import PI

json_inputs = {'SC': {'Er': 11.44, 'Height': 0.0, 'Ts': 35.0, 'Ground Thickness': 0.0,
                      'Super Conductor Operation Temperature': 4.0, 'Super Conductor Critical Temperature': 14.7,
                      'Super Conductor Critical Current': 0.0, 'Super Conductor Normal Resistivity': 100.0,
                      'Super Conductor Tangent Delta': 0.0},
               'Dimensions': {'loads': [['60', '3.4'], ['60', '3.4'], ['50', '3.4']], 'Unit Cell Length': 4.734,
                              'Central Line Width': 1.0, 'D0': 1.578, 'S': 1.0},
               'Frequency Range': {'Start Frequency': 0.0, 'End Frequency': 40.0, 'Resolution': 1000.0},
               'gain_models': {'Signal Amplitude': 0.0, 'Idler Amplitude': 0.0, 'Pump Amplitude': 0.0,
                               'Pump Frequency': 0.0}}



# json_inputs = {"SC": {"Er": 11.44, "Height": 0.0, "Ts": 20.0, "Ground Thickness": 0.0, "Super Conductor Operation Temperature": 0.0, "Super Conductor Critical Temperature": 15.83, "Super Conductor Critical Current": 0.0, "Super Conductor Normal Resistivity": 95.0, "Super Conductor Tangent Delta": 1e-10}, "Dimensions": {"loads": [["60", "14"], ["60", "14"], ["50", "14"]], "Unit Cell Length": 5.386, "Central Line Width": 2.0, "D0": 1.795, "S": 2.0}, "Frequency Range": {"Start Frequency": 1.0, "End Frequency": 40.0, "Resolution": 1000.0}, "gain_models": {"Signal Amplitude": 0.0, "Idler Amplitude": 0.0, "Pump Amplitude": 0.0, "Pump Frequency": 0.0}}

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


################################################################################################################################################

def get_betas_d(floquet_line, freq_range):
    return np.array([floquet_line.simulate(f)[1] for f in freq_range])


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
resolution = 1000
n_unitcells = 150
z_eval = np.linspace(0, (unit_cell_length * n_unitcells), resolution)
PUMP_FREQUENCY = utills.functions.hertz_to_GHz(11.33)

I_star = 1  # todo i star val ??

as0 = 1e-7+ 0j
ai0 = 0 + 0j
ap0 = .2 * I_star + 0j

inital_amplitudes = [as0, ai0, ap0]
z_span = (z_eval[0], z_eval[-1])
print("z/d = ", z_eval[-1] / unit_cell_length)
zstep = ((z_eval[-1] - 0) / (len(z_eval) - 1))*8

########################################################################################


# 1) get frequencys to simulate over
frequency_range = np.linspace(0,2*PUMP_FREQUENCY, resolution)

# 2) simulate batas and unfold betas*D, then divid by unitcell len to get beta
betas_unfolded = utills.functions.beta_unfold(get_betas_d(floquet_line, frequency_range))/unit_cell_length
# get betas for pump, idler, delta, and  betas
betas_signal = betas_unfolded
betas_pump = __get_closest_betas_at_given_freq(frequency_range, [PUMP_FREQUENCY] * resolution, betas_unfolded)
betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY - frequency_range), betas_unfolded)
delta_betas = betas_signal + betas_idler - 2 * betas_pump





power_gain, gain_idler, gain_pump = [], [], []

fig5, ax55 = plt.subplots(3)
ax55[0].set_title("signal")
ax55[1].set_title("idler")
ax55[2].set_title("PUMP")



probs = [int(resolution/10),int(resolution*(2/10)),int(resolution*(4/10)),int(resolution*(5/10)),int(resolution*(6/10)),int(resolution*(9/10))]
colors = ["b","g","r","c","m","k"]
coloridx = 0
s = time.time()

for f_idx,freq in enumerate(frequency_range):

    args = (betas_signal[f_idx], betas_idler[f_idx], betas_pump[f_idx], delta_betas[f_idx], I_star)
    sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=z_eval,max_step=zstep)
    amplitude_signal_over_z_range, amplitude_idler_over_z_range, amplitude_pump_over_z_range = sol.y

    # todo could be somthing weird or the sol.y
    signal_amplitude_before = amplitude_signal_over_z_range[0]
    signal_amplitude_after = amplitude_signal_over_z_range[-1]

    power_gain.append(10*math.log10(abs(signal_amplitude_after)**2 / abs(signal_amplitude_before)**2))




    # ds = np.abs(amplitude_signal_over_z_range)
    # di = np.abs(amplitude_idler_over_z_range)
    # dp = np.abs(amplitude_pump_over_z_range)
    #
    # if f_idx in probs:
    #     print(f"{int(f_idx / len(frequency_range) * 100)}% complete")
    #     ax55[0].plot(z_eval, ds, '-', color=colors[coloridx],)
    #     ax55[1].plot(z_eval, di, '-', color=colors[coloridx])
    #     ax55[2].plot(z_eval, dp, '-', color=colors[coloridx])
    #     coloridx+=1
print("time taken :",time.time()-s)



fig5.legend(np.round(frequency_range[probs]/1e9,2))

ax55[2].set_xlabel('z [Meters]')




fig, ax = plt.subplots()
plt.suptitle(f"Frequency Pump: {PUMP_FREQUENCY / 1e9} GHz -- ap0: {ap0.real} --- as0: {as0.real}")

# ax.plot(frequency_range / 1e9, power_gain,'-',color='tab:orange')
ax.plot(frequency_range/ 1e9, power_gain, '-', color='tab:orange')


for coloridx,prob in enumerate((frequency_range/1e9)[probs]):
    ax.axvline(x=prob, color=colors[coloridx])

ax.set_ylim([None, None])

ax.set_title(f"SIGNAL GAIN [20*log10]")
fig.set_size_inches(7, 7)
ax.set_xlabel('Frequency [GHz]')
plt.show()

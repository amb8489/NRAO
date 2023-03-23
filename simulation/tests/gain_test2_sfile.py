import math
from cmath import exp

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

import csv

from simulation.utills.functions import beta_unfold, hertz_to_GHz, toDb

import cmath
import numpy as np
import skrf as rf

from simulation.utills.functions import Transmission_Db


def Bloch_impedance_Zb(ABCD_mat_2x2: [[complex]]):
    A = ABCD_mat_2x2[0][0]
    B = ABCD_mat_2x2[0][1]
    D = ABCD_mat_2x2[1][1]

    ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
    ADm = A - D

    B2 = 2 * B

    ZB = - (B2 / (ADm + ADs2))
    ZB2 = - (B2 / (ADm - ADs2))
    if ZB.real < 0:
        ZB = ZB2

    return ZB





def gamma_d(ABCD_mat_2x2: [[complex]]):
    A = ABCD_mat_2x2[0][0]
    D = ABCD_mat_2x2[1][1]

    return np.arccosh(((A + D) / 2))


# reading in file and making a network


def abcd_and_frequency_range_from_hfss_touchstone_file(hfss_touchstone_file_path: str, n_interp_points: int = 1000):
    # make network
    network = rf.hfss_touchstone_2_network(hfss_touchstone_file_path)


    print(n_interp_points)

    # zero points means don't do any interpolation
    if n_interp_points > 0:
        if n_interp_points < network.frequency.npoints:
            raise Exception(
                f"n_interp_points must be > number of already simulated frequency points: {n_interp_points} < {network.sim_frequency.npoints}")

        interp_freq_range = rf.frequency.Frequency(start=network.frequency.start / 1e9,
                                                   stop=network.frequency.stop / 1e9,
                                                   npoints=n_interp_points, unit='ghz')

        network = network.interpolate(interp_freq_range, basis="a")

    # get abcd mats
    unit_cell_ABCD_mats = network.a

    # get the frequency range
    simulated_frequency_range = network.f

    return unit_cell_ABCD_mats, simulated_frequency_range


#  todo add these inputs to UI for transmission
N_unit_cells = 62
impedance = 50
unit_cell_length_todo = 0.003140

def hsff_simulate(file_path, n_interp_points):
    unit_cell_ABCD_mats, frequency_range = abcd_and_frequency_range_from_hfss_touchstone_file(file_path,
                                                                                              n_interp_points)

    floquet_alphas_d, floquet_betas_d, floquet_rs, floquet_xs,floquet_transmission = [], [], [], [],[]
    for unit_cell_abcd_mat in unit_cell_ABCD_mats:
        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell

        floquet_propagation_const_gamma = gamma_d(unit_cell_abcd_mat)
        ZB = Bloch_impedance_Zb(unit_cell_abcd_mat)

        floquet_transmission_ = Transmission_Db(N_unit_cells,
                                                impedance,
                                                ZB,
                                                floquet_propagation_const_gamma)
        floquet_transmission.append(floquet_transmission_)


        # floquet_bloch_impedance_pos_dir = abs(floquet_bloch_impedance_pos_dir.real)+ 1j*floquet_bloch_impedance_pos_dir.imag

        # get alpha beta r x
        floquet_alpha = floquet_propagation_const_gamma.real
        floquet_beta = floquet_propagation_const_gamma.imag
        floquet_r = ZB.real
        floquet_x = ZB.imag

        floquet_alphas_d.append(floquet_alpha)
        floquet_betas_d.append(floquet_beta)
        floquet_rs.append(floquet_r)
        floquet_xs.append(floquet_x)




    return frequency_range, floquet_alphas_d, [0] * len(floquet_alphas_d), floquet_betas_d, [0] * len(
        floquet_betas_d), floquet_rs, floquet_xs,floquet_transmission
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



unit_cell_length = 0.003140 #todo add to input
resolution = 1000
n_unitcells = 62            # todo add to input
z_eval = np.linspace(0, (unit_cell_length * n_unitcells), resolution)
z_span = (z_eval[0], z_eval[-1])
frequency_range, betas_d = get_betas_d(
    "/Users/aaron/PycharmProjects/NRAO/python_gui/Artificial_03_Artificial_UnitCell_Df=0.1GHz.s2p", resolution)
betas_unfolded =beta_unfold(betas_d) / unit_cell_length

i = 0
# pf,ap0 = 3.284 , .12
for ap0 in [.12]:
    for pf in [3.284]:

        ################################## GAIN PARAMS #######################################

        PUMP_FREQUENCY =hertz_to_GHz(pf)

        I_star = 1
        as0 = 1e-9+ 0j
        ai0 = 0 + 0j
        inital_amplitudes = [as0+0j, ai0+0j, ap0+0j]
        # print("z/d = ", z_eval[-1] / unit_cell_length)

        ########################################################################################


        # plt.plot(betas_unfolded)
        # plt.show()
        # get betas for pump, idler, delta, and  betas
        betas_signal = betas_unfolded
        betas_pump = __get_closest_betas_at_given_freq(frequency_range, [PUMP_FREQUENCY] * resolution, betas_unfolded)
        betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY - frequency_range), betas_unfolded)
        delta_betas = betas_signal + betas_idler - 2 * betas_pump





        power_gain, gain_idler, gain_pump = [], [], []

        frequency_range2 = frequency_range[np.where(frequency_range <= 2*PUMP_FREQUENCY)]
        for f_idx,freq in enumerate(frequency_range2):

            args = (betas_signal[f_idx], betas_idler[f_idx], betas_pump[f_idx], delta_betas[f_idx], I_star)

            # zstep = (z_eval[-1] - 0) / (len(z_eval) - 1)*n_unitcells*2
            sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=z_eval )#,max_step=zstep
            amplitude_signal_over_z_range, amplitude_idler_over_z_range, amplitude_pump_over_z_range = sol.y
            signal_amplitude_before = amplitude_signal_over_z_range[0]
            signal_amplitude_after = amplitude_signal_over_z_range[-1]

            power_gain.append(toDb((abs(sol.y[0][-1]) ** 2) / (abs(sol.y[0][0]) ** 2)))

            ds = np.abs(amplitude_signal_over_z_range)
            di = np.abs(amplitude_idler_over_z_range)
            dp = np.abs(amplitude_pump_over_z_range)

            if f_idx %10 == 0:
                print(f"{int(f_idx / len(frequency_range2) * 100)}% complete")




        print(inital_amplitudes,)
        fig, ax = plt.subplots()
        plt.suptitle(f"Frequency Pump: {PUMP_FREQUENCY / 1e9} GHz -- ap0: {ap0.real} -- id:{i}")
        # ax.plot(frequency_range / 1e9, power_gain,'-',color='tab:orange')
        ax.plot(frequency_range2/ 1e9, power_gain, '-', color='tab:orange')
        ax.set_ylim([None, None])
        ax.set_title(f"SIGNAL GAIN [10*log10]")
        fig.set_size_inches(7, 7)
        ax.set_xlabel('Frequency [GHz]')
        plt.show()
        exit(1)

        fig.savefig(f'../../../Desktop/results/id{i}plot_gain__ap0:{ap0.real}___Pumpf:{PUMP_FREQUENCY/1e9}.pdf', bbox_inches='tight')



        fields = ['Frequency', 'Gain-DB']
        rows = list(zip(frequency_range2,power_gain))

        with open(f'../../../Desktop/results/id{i}gain__ap0:{ap0.real}___Pumpf:{PUMP_FREQUENCY/1e9}', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(rows)
        i+=1
        plt.close()
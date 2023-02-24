import cmath

import matplotlib.pyplot as plt
import numpy as np
import skrf as rf

from utills.functions import unfold, mk_monotinic_inc


def Bloch_impedance_Zb(ABCD_mat_2x2: [[complex]]):
    A = ABCD_mat_2x2[0][0]
    B = ABCD_mat_2x2[0][1]
    D = ABCD_mat_2x2[1][1]

    ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
    B2 = 2 * B
    ADm = A - D

    # positive dir             # neg dir
    return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]


def mk_monotonic(lst):
    lst = np.array(lst)
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            lst[i:] += (lst[i - 1] - lst[i])
    return lst


def Pd(ABCD_mat_2x2: [[complex]]):
    A = ABCD_mat_2x2[0][0]
    D = ABCD_mat_2x2[1][1]

    return np.arccosh(((A + D) / 2))


# reading in file and making a network


def abcd_and_frequency_range_from_hfss_touchstone_file(hfss_touchstone_file_path: str, n_interp_points: int = 1000):
    # make network
    network = rf.hfss_touchstone_2_network(hfss_touchstone_file_path)

    # zero points means don't do any interpolation
    if n_interp_points > 0:
        if n_interp_points < network.frequency.npoints:
            raise Exception(
                f"n_interp_points must be > number of already simulated frequency points: {n_interp_points} < {network.frequency.npoints}")

        interp_freq_range = rf.frequency.Frequency(start=network.frequency.start / 1e9,
                                                   stop=network.frequency.stop / 1e9,
                                                   npoints=n_interp_points, unit='ghz')

        network = network.interpolate(interp_freq_range, basis="a")

    # get abcd mats
    unit_cell_ABCD_mats = network.a

    # get the frequency range
    simulated_frequency_range = network.f

    return unit_cell_ABCD_mats, simulated_frequency_range


def hsff_simulate(file_path, n_interp_points):
    unit_cell_ABCD_mats, frequency_range = abcd_and_frequency_range_from_hfss_touchstone_file(file_path,
                                                                                              n_interp_points)

    floquet_alphas, floquet_betas, floquet_rs, floquet_xs = [], [], [], []
    for unit_cell_abcd_mat in unit_cell_ABCD_mats:
        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell
        floquet_bloch_impedance_pos_dir, floquet_bloch_impedance_neg_dir = Bloch_impedance_Zb(unit_cell_abcd_mat)
        floquet_propagation_const = Pd(unit_cell_abcd_mat)

        # get alpha beta r x
        floquet_beta = floquet_propagation_const.imag
        floquet_alpha = floquet_propagation_const.real
        floquet_r = floquet_bloch_impedance_pos_dir.real
        floquet_x = floquet_bloch_impedance_pos_dir.imag

        floquet_alphas.append(floquet_alpha)
        floquet_betas.append(floquet_beta)
        floquet_rs.append(floquet_r)
        floquet_xs.append(floquet_x)



    fig1, ax1 = plt.subplots()
    ax1.set_ylabel('alpha - alpha0', color='tab:red')

    ax1.plot(frequency_range, np.array(floquet_alphas), color='tab:red')

    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_xlabel('Frequency [GHz]')
    ax2 = ax1.twinx()
    ax2.set_ylabel('beta - beta0', color='tab:green')
    # floquet_betas = savgol_filter(floquet_betas, 15, 1)
    ax2.plot(frequency_range, np.array(mk_monotinic_inc(floquet_betas)), color='tab:green')

    ax2.tick_params(axis='y', labelcolor='tab:green')
    fig1.tight_layout()

    # --------------------------------------------------------------------
    fig2, ax12 = plt.subplots()
    color = 'tab:blue'
    ax12.set_ylabel('r Blue -- x orange', color=color)
    ax12.plot(frequency_range, floquet_rs, color=color)
    ax12.tick_params(axis='y', labelcolor=color)
    ax12.set_xlabel('Frequency [GHz]')
    ax12.plot(frequency_range, floquet_xs, color='tab:orange')
    fig2.tight_layout()

    return [fig1, fig2]

import cmath

import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
from scipy.signal import savgol_filter


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


def abcd_N_frequency_range_from_hfss_touchstone_file(hfss_touchstone_file_path: str, n_interp_points: int = 1000):
    # make network
    network = rf.hfss_touchstone_2_network(hfss_touchstone_file_path)

    if n_interp_points < network.frequency.npoints:
        raise Exception(
            f"n_interp_points must be > number of already simulated frequency points: {n_interp_points} < {network.frequency.npoints}")

    interp_freq_range = rf.frequency.Frequency(start=network.frequency.start / 1e9, stop=network.frequency.stop / 1e9,
                                               npoints=n_interp_points, unit='ghz')

    network = network.interpolate(interp_freq_range, basis="a")

    unit_cell_ABCD_mats = network.a
    simulated_frequency_range = network.f

    return unit_cell_ABCD_mats, simulated_frequency_range


hfss_touchstone_file_path = '/Users/aaron/Desktop/Artificial_03_Artificial_UnitCell.s2p'
n_interp_points = 1000
unit_cell_ABCD_mats, frequency_range = abcd_N_frequency_range_from_hfss_touchstone_file(hfss_touchstone_file_path,
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

plt.plot(frequency_range, floquet_alphas)

floquet_betas = savgol_filter(floquet_betas, 15, 1)
plt.plot(frequency_range, floquet_betas)

# plt.plot(frequency_range, unfold(floquet_betas))
plt.plot(frequency_range, mk_monotonic(floquet_betas))
plt.show()

import cmath

import numpy as np
import skrf as rf

from utills.functions import beta_unfold, Transmission


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

    floquet_alphas, floquet_betas, floquet_rs, floquet_xs,floquet_transmission = [], [], [], [],[]
    for unit_cell_abcd_mat in unit_cell_ABCD_mats:
        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell

        floquet_propagation_const_gamma = gamma_d(unit_cell_abcd_mat)
        ZB = Bloch_impedance_Zb(unit_cell_abcd_mat)

        floquet_transmission_ = Transmission(N_unit_cells,
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

        floquet_alphas.append(floquet_alpha)
        floquet_betas.append(floquet_beta)
        floquet_rs.append(floquet_r)
        floquet_xs.append(floquet_x)

    # import csv
    #
    # fields = ['Frequency', 'floquet_transmission', 'floquet_rs', 'floquet_xs']
    #
    # rows = list(zip(frequency_range,floquet_transmission,floquet_rs,floquet_xs))
    #
    # with open('data', 'w') as f:
    #     # using csv.writer method from CSV package
    #     write = csv.writer(f)
    #     write.writerow(fields)
    #     write.writerows(rows)



    return frequency_range, floquet_alphas, [0] * len(floquet_alphas), floquet_betas, [0] * len(
        floquet_betas), floquet_rs, floquet_xs,floquet_transmission

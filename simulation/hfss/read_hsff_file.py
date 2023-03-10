import cmath
import numpy as np
import skrf as rf

from simulation.gain_models.multiprocessing_gain_simulate import simulate_gain_multiprocesses
from simulation.utills.functions import Transmission


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

    floquet_alphas_d, floquet_betas_d, floquet_rs, floquet_xs,floquet_transmission = [], [], [], [],[]
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

        floquet_alphas_d.append(floquet_alpha)
        floquet_betas_d.append(floquet_beta)
        floquet_rs.append(floquet_r)
        floquet_xs.append(floquet_x)



    # #todo make these inputs in UI
    unit_cell_length = 0.003140
    n_unitcells = 62
    PUMP_FREQUENCY = 3.284
    I_star = 1



    init_amplitudes = [complex(1e-9, 0), complex(0, 0), complex(.12 * I_star, 0)]
    resoultion= len(frequency_range)
    gain, gain_freq_range = simulate_gain_multiprocesses(resoultion, unit_cell_length, n_unitcells, frequency_range, PUMP_FREQUENCY,
                                                         init_amplitudes, I_star,
                                                         floquet_betas_d, floquet_alphas_d, floquet_rs, floquet_xs)
    gain_data = (gain, (gain_freq_range, PUMP_FREQUENCY, n_unitcells, init_amplitudes[2]))

    return frequency_range, floquet_alphas_d, [0] * len(floquet_alphas_d), floquet_betas_d, [0] * len(
        floquet_betas_d), floquet_rs, floquet_xs,floquet_transmission,gain_data

# from multiprocessing import Pool
import numpy as np
from pathos.multiprocessing import ProcessingPool as Pool
from scipy.integrate import solve_ivp

from simulation.gain_models.amplitude_equations.amplitude_equations1 import SIP_MODEL_1
from simulation.gain_models.amplitude_equations.amplitude_equations2 import SIP_MODEL_2
from simulation.utills.functions import toDb, beta_unfold


def __get_closest(find_in, needles, transform_to_lst, dointerp=False):
    '''
    todo refactor this explanation
    find the closest needle in find_in

    because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    simulated we find the closest frequency that was simulated to the one that was wanted


    :param find_in: list of values to find the closest value in to the wanted
    :param needles: wanted values to search in master for the closest
    :param betas_unfolded: unfolded batas
    :param dointerp: interpret more points to redude the distance to the closest point from needed point
    :return: list of transform_to_lst closest to target in find in
    '''

    if dointerp:
        x_len = len(find_in)
        x_org = np.linspace(0, x_len, x_len)
        x_interp = np.linspace(0, x_len, x_len * 2)
        find_in = np.interp(x_interp, x_org, find_in)
        transform_to_lst = np.interp(x_interp, x_org, transform_to_lst)

    sorted_keys = np.argsort(find_in)
    return transform_to_lst[sorted_keys[np.searchsorted(find_in, needles, sorter=sorted_keys)]]


def simulate_gain_multiprocessing(resolution, unit_cell_length, n_repeated_unitcells, frequency_range,
                                  pump_frequency, init_amplitudes, I_star,gamma_d_per_freq, ZB_per_freq, n_cores=6):
    '''

    multiprocessing solving ODE

    :param resolution:
    :param unit_cell_length:
    :param n_repeated_unitcells:
    :param frequency_range:
    :param pump_frequency:
    :param init_amplitudes:
    :param I_star:
    :param beta_d:
    :param alpha_d:
    :param r:
    :param x:
    :param n_cores: number of cores to use in pool
    :return: list of gain at each frequency and the frequency range it was simulated at
    '''
    # todo docs : frequency_range must >= 0 <--> 2*pump frequency to calc full gain plot

    ################################## gain / ODE solver params #######################################

    total_simulated_line_len = n_repeated_unitcells * unit_cell_length

    # points to eval the amplitude equations at
    z_eval = np.linspace(0, (unit_cell_length * n_repeated_unitcells), resolution)

    # start and end of z_eval
    z_span = (z_eval[0], z_eval[-1])

    # step amount for ODE solver
    # todo make this a UI option to pick mult factor to z step aka 32
    zstep = (total_simulated_line_len / resolution) * 32
    signal = 0

    # todo make this a UI option
    amplitude_model = 1

    ########################################################################################
    # -------- todo refacotr this into its own file or class --------

    alphas_signal = np.real(gamma_d_per_freq) / unit_cell_length
    alphas_pump = __get_closest(frequency_range, [pump_frequency] * resolution, alphas_signal)
    alphas_idler = __get_closest(frequency_range, (2 * pump_frequency - frequency_range), alphas_signal)

    betas_unfolded = beta_unfold(np.imag(gamma_d_per_freq)) / unit_cell_length
    betas_signal = betas_unfolded
    betas_pump = __get_closest(frequency_range, [pump_frequency] * resolution, betas_unfolded)
    betas_idler = __get_closest(frequency_range, (2 * pump_frequency - frequency_range), betas_unfolded)
    delta_betas = betas_signal + betas_idler - 2 * betas_pump

    r_signal = np.real(ZB_per_freq)
    r_pump = __get_closest(frequency_range, [pump_frequency] * resolution, r_signal)
    r_idler = __get_closest(frequency_range, (2 * pump_frequency - frequency_range), r_signal)

    x_signal = np.imag(ZB_per_freq)
    x_pump = __get_closest(frequency_range, [pump_frequency] * resolution, x_signal)
    x_idler = __get_closest(frequency_range, (2 * pump_frequency - frequency_range), x_signal)

    if amplitude_model == 1:
        func = SIP_MODEL_1
        func_args = list(zip(betas_signal, betas_idler, betas_pump, delta_betas, [I_star] * resolution))
    elif amplitude_model == 2:
        func = SIP_MODEL_2

        gs_signal = (alphas_signal ** 2 * r_signal ** 2 - betas_signal ** 2 * x_signal ** 2) / (
                betas_signal * (r_signal ** 2 + x_signal ** 2))
        gs_idler = (alphas_idler ** 2 * r_idler ** 2 - betas_idler ** 2 * x_idler ** 2) / (
                betas_idler * (r_idler ** 2 + x_idler ** 2))
        gs_pump = (alphas_pump ** 2 * r_pump ** 2 - betas_pump ** 2 * x_pump ** 2) / (
                betas_pump * (r_pump ** 2 + x_pump ** 2))

        func_args = list(zip(betas_signal, betas_idler, betas_pump,
                             alphas_signal, alphas_idler, alphas_pump,
                             gs_signal, gs_idler, gs_pump, delta_betas, [I_star] * resolution))
    else:
        raise NotImplementedError(f"amplitude_model {amplitude_model} is not implemented")

    # -------- end refactor

    def solve(solve_args):
        sol = solve_ivp(fun=func, t_span=z_span, y0=init_amplitudes, args=solve_args, t_eval=z_eval, max_step=zstep)
        return toDb((abs(sol.y[signal][-1]) ** 2) / (abs(sol.y[signal][0]) ** 2))

    # number of cores to use
    n_cores = max(1, int(n_cores))
    with Pool(n_cores) as p:
        # list of lists of arguments for each frequency we want to simulate at
        power_gain = np.array(p.map(solve, func_args))

    return power_gain,frequency_range

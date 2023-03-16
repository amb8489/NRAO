# from multiprocessing import Pool
import numpy as np
from pathos.multiprocessing import ProcessingPool as Pool
from scipy.integrate import solve_ivp

from simulation.gain_models.amplitude_equations.amplitude_equations1 import SIP_MODEL_1
from simulation.utills.functions import toDb, beta_unfold


def __get_closest_betas_at_given_freq(master, targets, betas_unfolded, dointerp=True):
    '''

    because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    simulated we find the closest frequency that was simulated to the one that was not and use that beta


    :param master: list of values to find the closest value in to the wanted
    :param targets: wanted values to search in master for the closest
    :param betas_unfolded: unfolded batas
    :param dointerp: interpret more points to redude the distance to the closest point from needed point
    :return: list of betas closest to target frequencies
    '''

    if dointerp:
        x_len = len(master)
        x_org = np.linspace(0, x_len, x_len)
        x_interp = np.linspace(0, x_len, x_len * 2)
        master = np.interp(x_interp, x_org, master)
        betas_unfolded = np.interp(x_interp, x_org, betas_unfolded)

    sorted_keys = np.argsort(master)
    return betas_unfolded[sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys)]]


def simulate_gain_multiprocessing(resolution, unit_cell_length, n_repeated_unitcells, frequency_range, PUMP_FREQUENCY_GHz,
                                  init_amplitudes, I_star,
                                  gamma_d_per_freq, bloch_impedance_per_freq, n_cores=6):

    '''

    multiprocessing solving ODE

    :param resolution:
    :param unit_cell_length:
    :param n_repeated_unitcells:
    :param frequency_range:
    :param PUMP_FREQUENCY_GHz:
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

    #points to eval the amplitude equations at
    z_eval = np.linspace(0, (unit_cell_length * n_repeated_unitcells), resolution)

    # start and end of z_eval
    z_span = (z_eval[0], z_eval[-1])

    # step amount for ODE solver
    zstep = (total_simulated_line_len / resolution) * 64
    signal = 0

    ########################################################################################

    def solve(args):
        sol = solve_ivp(fun=SIP_MODEL_1, t_span=z_span, y0=init_amplitudes, args=args, t_eval=z_eval, max_step=zstep)
        return toDb((abs(sol.y[signal][-1]) ** 2) / (abs(sol.y[signal][0]) ** 2))


    # simulate batas_d and unfold betas*D, then divid by unitcell len to get just beta

    betas_unfolded = beta_unfold(np.imag(gamma_d_per_freq)) / unit_cell_length

    # get betas for signal, idler, pump, delta betas
    betas_signal = betas_unfolded
    betas_pump = __get_closest_betas_at_given_freq(frequency_range, [PUMP_FREQUENCY_GHz] * resolution, betas_unfolded)
    betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY_GHz - frequency_range), betas_unfolded)
    delta_betas = betas_signal + betas_idler - 2 * betas_pump


    # number of cores to use
    n_cores = max(1, int(n_cores))


    with Pool(n_cores) as p:

        # list of lists of arguments for each frequency we want to simulate at
        args = list(zip(betas_signal, betas_idler, betas_pump, delta_betas, [I_star] * resolution))
        power_gain = np.array(p.map(solve, args))

    return power_gain, frequency_range

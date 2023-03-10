import time
# from multiprocessing import Pool
from pathos.multiprocessing import ProcessingPool as Pool
import numpy as np
from scipy.integrate import solve_ivp

from simulation.gain_models.amplitude_equations.amplitude_equations1 import SIP_MODEL_1
from simulation.utills.functions import hertz_to_GHz, toDb, beta_unfold


def __get_closest_betas_at_given_freq(master, targets, betas_unfolded, dointerp=True):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta

    # todo len(master) == len(targets)  in docs

    if dointerp:
        x_len = len(master)
        x_org = np.linspace(0, x_len, x_len)
        x_interp = np.linspace(0, x_len, x_len * 2)
        master = np.interp(x_interp, x_org, master)
        betas_unfolded = np.interp(x_interp, x_org, betas_unfolded)

    sorted_keys = np.argsort(master)
    return betas_unfolded[sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys)]]


def simulate_gain_multiprocesses(resolution, unit_cell_length, n_unitcells, frequency_range, PUMP_FREQUENCY, init_amplitudes, I_star,
                                 beta_d, alpha_d, r, x):

    # todo docs : frequency_range must >= 0 <--> 2*pump frequency to calc full gain plot
    # alpha_d, r, x are unused in this implentation of gain equation

    ################################## GAIN PARAMS #######################################
    PUMP_FREQUENCY = hertz_to_GHz(PUMP_FREQUENCY)
    total_line_len = n_unitcells * unit_cell_length
    z_eval = np.linspace(0, (unit_cell_length * n_unitcells), resolution)
    z_span = (z_eval[0], z_eval[-1])
    zstep = (total_line_len / (resolution)) * 32
    signal = 0
    ########################################################################################

    def solve(args):
        sol = solve_ivp(fun=SIP_MODEL_1, t_span=z_span, y0=init_amplitudes, args=args, t_eval=z_eval, max_step=zstep)
        return toDb((abs(sol.y[signal][-1]) ** 2) / (abs(sol.y[signal][0]) ** 2))



    # simulate batas and unfold betas*D, then divid by unitcell len to get just beta
    betas_unfolded = beta_unfold(beta_d) / unit_cell_length

    # get betas for pump, idler, delta, and  betas


    betas_signal = betas_unfolded
    betas_pump = __get_closest_betas_at_given_freq(frequency_range, [PUMP_FREQUENCY] * resolution, betas_unfolded)
    betas_idler = __get_closest_betas_at_given_freq(frequency_range, (2 * PUMP_FREQUENCY - frequency_range),
                                                    betas_unfolded)

    delta_betas = betas_signal + betas_idler - 2 * betas_pump

    n_cores = 6
    with Pool(n_cores) as p:
        args = list(zip(betas_signal, betas_idler, betas_pump, delta_betas, [I_star] * resolution))
        power_gain = np.array(p.map(solve, args))

    wheres = np.where(frequency_range <= 2 * PUMP_FREQUENCY)
    return power_gain[wheres],frequency_range[wheres]

# steps
#   calc beta_plt for given range and resolution
#   calc beta_plt at pumpFreq
#   calc beta_plt for all pumpFreqs and idler freqencys
#   calc for each frequency the gain using lst calced above and other init vars
#   turn gain into dB, mult back by Istar*, calc power
import numpy as np

import utills.functions
from gain_models.amplitude_equations.amplitude_equations1 import AmplitudeEqs1
from gain_models.solve_ode import Solve_ode


def CalculateBetas(FloquetLine, FreqRange):
    Betas = []
    for frequency in FreqRange:
        alpha, beta, alpha_cl, beta_cl, r, x,t = FloquetLine.simulate(frequency)
        Betas.append(beta)
    return Betas

def IC(critical_current,area):
    return critical_current * area


def Calc_Gain(floquet_line, resolution, pump_freq, init_amplitudes, L):
    frequencys = np.linspace(1, pump_freq * 2, resolution)

    z = np.linspace(0, floquet_line.unit_cell.unit_cell_length*1, resolution)

    # step 1) calc unfolded beta_plt for given range and resolution (lst for signal frequency)
    beta_signal = np.array(utills.functions.beta_unfold(CalculateBetas(floquet_line, frequencys)))

    # step 2) find the beta_plt for pumpFreq
    beta_pump = beta_signal[np.searchsorted(frequencys, pump_freq)]

    # step 3) calc beta_plt for all idler freqencys
    beta_idler = beta_signal[np.searchsorted(frequencys, (pump_freq * 2) - frequencys)]

    # step 4) calc gain for each frequency using lst calced above and other init vars
    gain = []
    for i in range(len(frequencys)):
        # todo generalize amplitude equations into floquet_alpha class maybe that holds all amplitude_eqs1_args info and what equations to use?
        amplitude_eqs1_args = (beta_signal[i], beta_idler[i], beta_pump)

        # opt split up into multiple processes then recombine
        gain.append(Solve_ode(init_amplitudes, AmplitudeEqs1, amplitude_eqs1_args, z, L))

    # todo gain into dB
    # todo into Istar
    # todo calc power
    return frequencys, gain

# steps
#   calc beta for given range and resolution
#   calc beta at pumpFreq
#   calc beta for all pumpFreqs and idler freqencys
#   calc for each freq the gain using betas calced above and other init vars
#   turn gain into dB, mult back by Istar*, calc power
import numpy as np

from Gain.AmplitudeEquations.AmplitudeEquations1 import AmplitudeEqs1
from Gain.MicroStrip.solveODEs import Solve_ode


def CalculateBetas(FloquetLine, FreqRange):
    Betas = []
    for F in FreqRange:
        a, t, beta, r, x, R, L, G, C = FloquetLine.abrx(F)
        Betas.append(beta)
    return Betas


def Calc_Gain(floquet_line, resolution, pump_freq, init_amplitudes, L):
    frequencys = np.linspace(.5e9, pump_freq * 2, resolution)
    z = np.linspace(0, floquet_line.unit_cell_length, resolution)

    # step 1) calc unfolded beta for given range and resolution (betas for signal freq)
    beta_signal = np.array(floquet_line.unfold(CalculateBetas(floquet_line, frequencys)))

    # step 2) find the beta for pumpFreq
    beta_pump = beta_signal[np.searchsorted(frequencys, pump_freq)]

    # step 3) calc beta for all idler freqencys
    # todo (pump_freq*2) - FreqRange may need to be reversed
    beta_idler = beta_signal[np.searchsorted(frequencys, (pump_freq * 2) - frequencys)]

    # step 4) calc gain for each freq using betas calced above and other init vars
    gain = []
    for i in range(len(frequencys)):
        # todo generalize amplitude equations into a class maybe that holds all amplitude_eqs1_args info and what equations to use?
        amplitude_eqs1_args = (beta_signal[i], beta_idler[i], beta_pump)

        # opt split up into multiple processes then recombine
        gain.append(Solve_ode(init_amplitudes, AmplitudeEqs1, amplitude_eqs1_args, z, L))

    # todo gain into dB
    # todo into Istar
    # todo calc power
    return frequencys,gain

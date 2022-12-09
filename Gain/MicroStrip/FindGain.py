# steps
#   calc beta for given range and resolution
#   calc beta at pumpFreq
#   calc beta for all pumpFreqs and idler freqencys
#   calc for each freq the gain using betas calced above and other init vars
import numpy as np

from Gain.AmplitudeEquations.AmplitudeEquations1 import AmplitudeEqs1
from Gain.MicroStrip.solveODEs import Solve_ode


def CalculateBetas(FloquetLine, FreqRange):
    Betas = []
    for F in FreqRange:
        _, beta, _, _, _, _, _, _ = FloquetLine.abrx(F)
        Betas.append(beta)
    return Betas


def Calc_Gain(FloquetLine, StartFreq, EndFreq, Resolution, PumpFreq, As_init, Ai_init, Ap_init, L, I):
    Frequencys = np.linspace(.5e9, PumpFreq * 2, Resolution)
    z = np.linspace(0, FloquetLine.Unit_Cell_Len, Resolution)

    # step 1 calc beta for given range and resolution (betas for signal freq)
    betas = FloquetLine.unfold(CalculateBetas(FloquetLine, Frequencys))

    # step 2 find the beta for pumpFreq
    beta_pump = betas[np.searchsorted(Frequencys, PumpFreq)]

    # step 3 calc beta for all idler freqencys
    # todo (PumpFreq*2) - FreqRange may need to be reversed
    beta_idler = betas[np.searchsorted(Frequencys, (PumpFreq * 2) - Frequencys)]

    # step 4 calc gain for each freq using betas calced above and other init vars
    gain = []
    for i in range(len(Frequencys)):
        AmplitudeEqs1Args = (betas[i], beta_idler[i], beta_pump, I)
        gain.append(Solve_ode([As_init, Ai_init, Ap_init], AmplitudeEqs1, AmplitudeEqs1Args, z, L))

    return gain

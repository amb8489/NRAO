# steps
#   calc beta for given range and resolution
#   calc beta at pumpFreq
#   calc beta for all pumpFreqs and idler freqencys
#   calc for each freq the gain using betas calced above and other init vars
import numpy as np


def CalculateBetas(FloquetLine, FreqRange):
    Betas = []
    for F in FreqRange:
        _, BetaUnfolded, _, _, _, _, _, _, _ = FloquetLine.abrx(F)
        Betas.append(BetaUnfolded)
    return Betas


def gain(FloquetLine, StartFreq, EndFreq, Resolution, PumpFreq):
    Frequencys = np.linspace(.5e9, PumpFreq * 2, Resolution)

    # step 1 calc beta for given range and resolution (betas for signal freq)
    betas = CalculateBetas(FloquetLine, Frequencys)

    # step 2 find the beta for pumpFreq
    beta_pump = betas[np.searchsorted(Frequencys, PumpFreq)]

    # step 3 calc beta for all idler freqencys
    beta_idler = betas[np.searchsorted(Frequencys, (
                PumpFreq * 2) - Frequencys)]  # todo (PumpFreq*2) - FreqRange may need to be reversed

    # step 4 calc gain for each freq using betas calced above and other init vars
    for i in range(len(Frequencys)):
        AmplitudeEqs1Args = (betas[i], beta_idler[i], beta_pump, I)
        g = Gain(init_vals_arr, AmplitudeEqs1, AmplitudeEqs1Args, z, L)

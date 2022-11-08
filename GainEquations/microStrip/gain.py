import numpy as np
from scipy.integrate import odeint

from GainEquations.microStrip.amplitudeEquations import ApmlitudeEquations


def Gain(freq_sig, freq_pump, z, I, beta_signal, beta_idler, beta_pump, As_0, Ai_0, Ap_0, L):
    # beta at each freq todo map freq to beta or pass in index
    bs = beta_signal[freq_sig]
    bi = beta_idler[2 * beta_pump - freq_sig]
    bp = beta_pump[freq_pump]

    inti_conditions = [As_0, Ai_0, Ap_0]

    soln = odeint(ApmlitudeEquations, inti_conditions, z, args=(bs, bi, bp, I))

    # todo look at gain in mathimatica

    return np.log10((soln[:, 2][L] / soln[:, 2][0]) ** 2)

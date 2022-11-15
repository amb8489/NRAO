import numpy as np
from scipy.integrate import odeint
from GainEquations.microStrip.amplitudeEquations import ApmlitudeEquations
from Supports.Support_Functions import find_idx_of_closest_value


def Gain(freq_idler, signal_freq, z, I, betas, beta_p, As_0, Ai_0, Ap_0, L, resolution, f_range):
    # get index for signal and idler freqs inside beta array
    idx_sig, idx_idler = np.searchsorted(f_range, [signal_freq, freq_idler])
    beta_s = betas[idx_sig]  # get beta for signal freq
    beta_i = betas[idx_idler]  # get beta for idel freq
    soln = odeint(ApmlitudeEquations, [As_0, Ai_0, Ap_0], z, args=(beta_s, beta_i, beta_p, I))

    # todo look at gain in mathimatica where L is used
    return soln[:, 0][L]

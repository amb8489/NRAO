import numpy as np
from scipy.integrate import odeint

from GainEquations.microStrip.amplitudeEquations import ApmlitudeEquations


def Gain(freq, z, I, betas_signal, betas_idler, beta_p, As_0, Ai_0, Ap_0, L, resolution, freq_to_idx):
    # beta at each freq todo map freq to beta or pass in index
    beta_s = betas_signal[freq_to_idx[freq]]

    #  can always just do beta_signal[find_idx_of_closest_value(f_range, idel_freq)] instead
    #todo why does this work but not res - 1 - idx
    beta_i = betas_idler[ freq_to_idx[freq]]
    # beta_i = betas_idler[ resolution - 1 -freq_to_idx[freq]]



    soln = odeint(ApmlitudeEquations, [As_0, Ai_0, Ap_0], z, args=(beta_s, beta_i, beta_p, I))
    # todo look at gain in mathimatica

    return np.log10(soln[:, 0][resolution//2])



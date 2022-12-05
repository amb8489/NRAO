import numpy as np
from scipy.integrate import odeint
from GainEquations.microStrip.AmplitudeEquations.amplitudeEquations import ApmlitudeEquations

signal = 0
idler = 1
pump = 2


def Gain(freq_idler, signal_freq, z, I, betas, beta_p, As_0, Ai_0, Ap_0, L, resolution, f_range):

    """
    Calculates the gain at a frequency
    :param freq_idler: frequency of the idler
    :param signal_freq: frequency of the signal
    :param z:
    :param I:
    :param betas: list of betas
    :param beta_p: beta of the pump
    :param As_0: initial amplitude of Signal
    :param Ai_0: initial amplitude of idler
    :param Ap_0: initial amplitude of pump
    :param L:
    :param f_range: the range of frequencies that will be checked

    :return:
    """
    # get index for signal and idler freqs inside beta array

    idx_sig, idx_idler = np.searchsorted(f_range, [signal_freq, freq_idler])
    beta_s = betas[idx_sig]  # get beta for signal freq
    beta_i = betas[idx_idler]  # get beta for idel freq
    soln = odeint(ApmlitudeEquations, [As_0, Ai_0, Ap_0], z, args=(beta_s, beta_i, beta_p, I))
    # todo look at gain in mathimatica where L is use
    return soln[:, signal][L]

import numpy as np
import cmath


def ApmlitudeEquations(Amplitudes, z, beta_s, beta_i, beta_p, I):
    """
    #todo
    # signal-idler-pump equations for N = 3


    :param Amplitudes:
    :param z:
    :param beta_s:
    :param beta_i:
    :param beta_p:
    :param I:
    :return:
    """

    # Amplitudes[0]  Amplitude for signal
    # Amplitudes[0]  Amplitude for idler
    # Amplitudes[0]  Amplitude for pump
    A_sig = Amplitudes[0]
    A_idler = Amplitudes[1]
    A_pump = Amplitudes[2]

    # conj Amplitudes
    A_star_s = np.conj(Amplitudes[0])
    A_star_i = np.conj(Amplitudes[1])
    A_star_p = np.conj(Amplitudes[2])

    deltaB = (beta_s + beta_i) - (2 * beta_p)

    # Optical coupled equations

    As = ((-1j * ((beta_s) / (8 * (I ** 2)))) *
          (A_sig * ((abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) + (2 * (abs(A_pump) ** 2))) + A_star_i * (
                  A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    Ai = ((-1j * ((beta_i) / (8 * (I ** 2)))) *
          (A_idler * ((2 * (abs(A_sig) ** 2)) + (abs(A_idler) ** 2) + (2 * (abs(A_pump) ** 2))) + A_star_s * (
                  A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    Ap = ((-1j * ((beta_p) / (8 * (I ** 2)))) *
          (A_pump * (2 * (abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) + (abs(A_pump) ** 2)) + 2 * A_star_p *
           A_sig * A_idler * cmath.exp(-1j * deltaB * z)))

    return [As, Ai, Ap]

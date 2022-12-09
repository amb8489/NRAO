import numpy as np
import cmath


def AmplitudeEqs1(Amplitudes, z, beta_s, beta_i, beta_p):
    """

    # signal-idler-pump equations for N = 3


    :param Amplitudes:
    :param z:
    :param beta_s:
    :param beta_i:
    :param beta_p:
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

    AmplitudeSignal =  ((-1j * ((beta_s) / 8)) * (A_sig * ((abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) +
                      (2 * (abs(A_pump) ** 2))) + A_star_i * (A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    AmplitudeIdler = ((-1j * ((beta_i) / 8)) * (A_idler * ((2 * (abs(A_sig) ** 2)) + (abs(A_idler) ** 2) +
                     (2 * (abs(A_pump) ** 2))) + A_star_s *(A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    AmplitudePump = ((-1j * ((beta_p) / 8)) *(A_pump * (2 * (abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) +
                     (abs(A_pump) ** 2)) + 2 * A_star_p * A_sig * A_idler * cmath.exp(-1j * deltaB * z)))

    return [AmplitudeSignal, AmplitudeIdler, AmplitudePump]

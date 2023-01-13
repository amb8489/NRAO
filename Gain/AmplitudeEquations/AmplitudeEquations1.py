import numpy as np
import cmath


# todo make standanrd format (amplitudes, z ,args)

def AmplitudeEqs1(amplitudes, z, args):
    # signal-idler-pump equations for N = 3

    beta_s, beta_i, beta_p = args

    A_sig = amplitudes[0]  # amplitudes[0]  Amplitude for signal
    A_idler = amplitudes[1]  # amplitudes[1]  Amplitude for idler
    A_pump = amplitudes[2]  # amplitudes[2]  Amplitude for pump

    # conj amplitudes
    A_star_s = amplitudes[0].conjugate()
    A_star_i = amplitudes[1].conjugate()
    A_star_p = amplitudes[2].conjugate()

    deltaB = (beta_s + beta_i) - (2 * beta_p)

    # Optical coupled equations

    AmplitudeSignal = ((-1j * (beta_s / 8)) * (A_sig * ((abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) +
                                                        (2 * (abs(A_pump) ** 2))) + A_star_i * (
                                                           A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    AmplitudeIdler = ((-1j * (beta_i / 8)) * (A_idler * ((2 * (abs(A_sig) ** 2)) + (abs(A_idler) ** 2) +
                                                         (2 * (abs(A_pump) ** 2))) + A_star_s * (
                                                          A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    AmplitudePump = ((-1j * (beta_p / 8)) * (A_pump * (2 * (abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) +
                                                       (abs(A_pump) ** 2)) + 2 * A_star_p * A_sig * A_idler * cmath.exp(
                                                          -1j * deltaB * z)))

    return [AmplitudeSignal, AmplitudeIdler, AmplitudePump]

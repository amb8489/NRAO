import numpy as np
import cmath


# optimization cython


def ApmlitudeEquations(Amplitudes, z, B_s, B_i, B_p, I):
    # signal-idler-pump equations for N = 3

    # Amplitudes at 0 is Amplitude for signal 1 is for idler and 2 is for pump
    # todo make usure these inputs are correct in terms of being complex
    A_sig = Amplitudes[0]
    A_idler = Amplitudes[1]
    A_pump = Amplitudes[2]

    # conj Amplitudes at 0 is conj Amplitude for signal 1 is for idler and 2 is for pump
    A_star_s = np.conj(Amplitudes[0])
    A_star_i = np.conj(Amplitudes[1])
    A_star_p = np.conj(Amplitudes[2])


    deltaB = (B_s + B_i) - (2 * B_p)

    # Optical coupled equations for N = 3

    As = ((-1j * ((B_s) / (8 * (I ** 2)))) *
          (A_sig * ((abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) + (2 * (abs(A_pump) ** 2))) + A_star_i * (
                  A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    Ai = ((-1j * ((B_i) / (8 * (I ** 2)))) *
          (A_idler * ((2 * (abs(A_sig) ** 2)) + (abs(A_idler) ** 2) + (2 * (abs(A_pump) ** 2))) + A_star_s * (
                  A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    Ap = ((-1j * ((B_p) / (8 * (I ** 2)))) *
          (A_pump * (2 * (abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) + (abs(A_pump) ** 2)) + 2 * A_star_p *
           A_sig * A_idler * cmath.exp(-1j * deltaB * z)))

    return [As, Ai, Ap]

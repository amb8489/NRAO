import math

import numpy as np
from scipy.integrate import odeint
import cmath
import time
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.Fluqet_line_equations import ABCD_TL, UnitCellABCD_mats
from Fluqet_Line_Equations.microStrip.beta_unfold import calc_aplha_beta_r_x
from TransmissionLineEquations.microStrip.MicroStripModel import SuperConductingMicroStripModel
from Supports.constants import PI


# optimization cython


def Pd(mat):
    mat_A = mat[0][0]
    mat_D = mat[1][1]

    return np.arccosh((mat_A + mat_D) / 2)


def Zb(mat):
    mat_A = mat[0][0]
    mat_B = mat[0][1]
    mat_D = mat[1][1]

    ADs2 = cmath.sqrt(pow(mat_A + mat_D, 2) - 4)

    B2 = 2 * mat_B

    ADm = mat_A - mat_D

    return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]


def fn(gamma, Z):
    r = Z.real
    x = Z.imag
    alpha = gamma.real
    beta = gamma.imag

    return (1 / (2 * beta)) * ((alpha ** 2) - (beta ** 2) - (abs(gamma) ** 2 / abs(Z) ** 2) * ((r ** 2) - (x ** 2)))


def gn(gamma, Z):
    r = Z.real
    x = Z.imag

    alpha = gamma.real
    beta = gamma.imag

    xSqred = x ** 2
    rSqred = r ** 2

    return ((alpha ** 2) * rSqred - (beta ** 2) * xSqred) / (beta * (rSqred + xSqred))


def ApmlitudeEquations(A, z):
    # signal-idler-pump equations for N = 3

    #
    A_s = A[0]
    A_i = A[1]
    A_p = A[2]

    A_star_s = A[0]
    A_star_i = A[1]
    A_star_p = A[2]

    B_s = A[0]
    B_i = A[0]
    B_p = A[0]
    I = 10000000

    # s-i-p equations for N = 3
    # Optical coupled equations
    deltaB = B_s + B_i - (2 * B_p)

    As_prime = ((-1j * (B_s / (8 * (I ** 2)))) *
                (A_s * ((abs(A_s) ** 2) + (2 * (abs(A_i) ** 2)) + (2 * (abs(A_p) ** 2))) + A_star_i * (
                        A_p ** 2) * cmath.exp(1j * deltaB * z)))

    Ai_prime = ((-1j * (B_i / (8 * (I ** 2)))) *
                (A_i * ((2 * (abs(A_s) ** 2)) + (abs(A_i) ** 2) + (2 * (abs(A_p) ** 2))) + A_star_s * (
                        A_p ** 2) * cmath.exp(1j * deltaB * z)))

    Ap_prime = ((-1j * (B_p / (8 * (I ** 2)))) *
                (A_p * (2 * (abs(A_s) ** 2) + (2 * (abs(A_i) ** 2)) + (abs(A_p) ** 2)) + 2 * A_star_p *
                 A_s * A_i * cmath.exp(-1j * deltaB * z)))

    return [As_prime, Ai_prime, Ap_prime]


from bisect import bisect_left

import bisect
def find_idx_of_closest_value(a, x):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """

    i = bisect.bisect_left(a, x)
    if i >= len(a):
        i = len(a) - 1
    elif i and a[i] - x > x - a[i - 1]:
        i = i - 1
    return i




def solveCoupledODE(As_init, Ai_init, Ap_init, d, fStartGain, fEndGain):
    res = 1000
    # constant
    pump_freq = 6.772e9
    pump_freqTimes2 = 2 * pump_freq

    # calc signal freq up to
    lineModel = calc_aplha_beta_r_x()
    beta_signal = []

    s = time.time()

    f_range = np.linspace(1000, pump_freqTimes2, res)
    for i, signal_freq in enumerate(f_range):
        btaUf_signal, bta = lineModel.beta_unfolded(signal_freq)
        beta_signal.append(btaUf_signal)

    print(f"time taken {time.time() - s}")
    print(beta_signal[find_idx_of_closest_value(f_range, pump_freq)])

    # use np search sorted over range of freqs
    for i, signal_freq in enumerate(f_range):
        pass

    exit(1)

    # init conditions
    y0 = [As_init, Ai_init, Ap_init]

    # range over fluquet line
    z = np.linspace(0, d, 100)

    x = odeint(ApmlitudeEquations, y0, z, args=())

    S = x[:, 0]
    I = x[:, 1]
    P = x[:, 2]

    plt.plot(z, S)
    plt.plot(z, I)
    plt.plot(z, P)
    plt.show()


if __name__ == "__main__":
    StartFreq, EndFreq = 6.75e9, 6.85e9
    d = .0023
    # todo init conditions
    solveCoupledODE(.1, 0, .3, d, StartFreq, EndFreq)

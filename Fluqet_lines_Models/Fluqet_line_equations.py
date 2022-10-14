import math
import numpy as np


# ABCD matrix of TLs
# Z characteristic impedance; k wavenumber; l length 


def ABCD_TL(Z, Gamma, l):
    GL = Gamma * l
    coshGL = math.cosh(GL)

    return [[coshGL, Z * math.sinh(GL)],
            [(1 / Z) * math.sinh(GL), coshGL]]


# Product of matrices TL[Z,Gamma,l]
# Z,Gamma,d are given as vectors
def prodTL(Z, Gamma, L):
    return np.multi_dot([ABCD_TL(Z[i], Gamma[i], L[i]) for i in range(len(Z))])


# Transmission of n identical cells
def S21Ncell(n, Zequ1, Zequ2, Gamma_equ, d, Zo):
    return (2 * math.exp(d * n * Gamma_equ) * (Zequ1 - Zequ2) * Zo) / (
            (1 + math.exp(2 * d * n * Gamma_equ)) * (Zequ1 - Zequ2) * Zo - (
            -1 + math.exp(2 * d * n * Gamma_equ)) * (Zequ1 * Zequ2 - Zo ^ 2))

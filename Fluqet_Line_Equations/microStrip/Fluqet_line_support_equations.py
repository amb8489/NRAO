'''

equations needed for making ABCD matrices and ZB and gamma


'''

import cmath
import numpy as np


# ABCD matrix of TLs
# Z characteristic impedance; k wavenumber; l length
def ABCD_TL(Z, Gamma, L):
    GL = Gamma * L
    coshGL = cmath.cosh(GL)
    sinhGL = cmath.sinh(GL)

    return [[coshGL, Z * sinhGL],
            [(1 / Z) * sinhGL, coshGL]]


def Pd(ABCD_mat):
    A = ABCD_mat[0][0]
    D = ABCD_mat[1][1]
    return np.arccosh((A + D) / 2)


def Bloch_impedance_Zb(ABCD_mat):
    A = ABCD_mat[0][0]
    B = ABCD_mat[0][1]
    D = ABCD_mat[1][1]

    ADs2 = cmath.sqrt(pow(A + D, 2) - 4)
    B2 = 2 * B
    ADm = A - D

    # positive dir             # neg dir
    return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]


# todo this is Zb and not Zc?
def RLGC(propagationConst, Zb):
    Z = propagationConst * Zb
    Y = propagationConst / Zb

    R = Z.real
    L = Z.imag
    G = Y.real
    C = Y.imag
    return R, L, G, C



def transmission():

    pass
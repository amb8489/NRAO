'''



equations needed in
'''

import cmath
import math
import numpy as np


# ABCD matrix of TLs
# Z characteristic impedance; k wavenumber; l length 
# TODO WHAT of these formulas are NOT model specific so they can be factored out into a diff file
# ( A B )
# ( C D )


def ABCD_TL(Z, Gamma, L):
    GL = Gamma * L
    coshGL = cmath.cosh(GL)
    sinhGL = cmath.sinh(GL)

    # TODO IN PICTURE THESE IS A J in (0,1) and (1,0)
    return [[coshGL, Z * sinhGL],
            [(1 / Z) * sinhGL, coshGL]]


def Pd(mat):
    mat_A = mat[0][0]
    mat_D = mat[1][1]
    return np.arccosh((mat_A + mat_D) / 2)


# todo in paper they use -2BZ ?
def Bloch_impedance_Zb(mat):
    mat_A = mat[0][0]
    mat_B = mat[0][1]
    mat_D = mat[1][1]

    ADs2 = cmath.sqrt(pow(mat_A + mat_D, 2) - 4)
    B2 = 2 * mat_B
    ADm = mat_A - mat_D

    # positive dir             # neg dir
    return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]





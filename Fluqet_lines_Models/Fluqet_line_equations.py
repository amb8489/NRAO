import math
import numpy as np

from Supports.Support_Functions import isOddInt, Chop
from Supports.constants import PI


# ABCD matrix of TLs
# Z characteristic impedance; k wavenumber; l length 
# TODO WHAT of these formulas are NOT model specific 
# ( A B )
# ( C D )
def ABCD_TL(Z, Gamma, l):
    GL = Gamma * l
    coshGL = math.cosh(GL)

    # TODO IN PICTURE THESE IS A J in (0,1) and (1,0)
    return [[coshGL, Z * math.sinh(GL)],
            [(1 / Z) * math.sinh(GL), coshGL]]


# TODO
def fpos(maxx, ceros, f):
    pass



'''
Propagation constant and Bloch impedance
The propagation constant is obtained through ArcCosh[(A+D)/2]
ZB is selected such that Re[ZB] >= 0
Propagation constant calculated as GammaD
'''

# TODO CHECK FOR CORRECTNESS
def GammaDZB(ABCD_Mat, maxx, ceros, f):
    A = ABCD_Mat[0][0]
    B = ABCD_Mat[0][1]
    C = ABCD_Mat[1][0]
    D = ABCD_Mat[1][1]

    ApD = (A + D)
    ADs2 = math.sqrt(ApD ** 2 - 4)

    ADm = A - D

    # does chap work on the im and real part
    gd = Chop(math.acosh(ApD / 2))

    B2 = 2 * B
    zb1 = -(B2 / (ADm - ADs2))

    zb = zb1 if zb1.real >= 0 else -(B2 / (ADm + ADs2))

    p, j = fpos(maxx, ceros, f)

    z = j - ((j - 1) % 2) if isOddInt(p) else j - (j % 2)

    igd = z * PI - gd.imag if z % 2 == 0 else gd.imag + (z - 1) * PI

    gd = gd.real + 1j * igd

    return [gd, zb]

# TODO CHECK FOR CORRECTNESS

def GammaDZB0(ABCD_Mat, maxx, ceros, f):
    A = ABCD_Mat[0][0]
    B = ABCD_Mat[0][1]
    C = ABCD_Mat[1][0]
    D = ABCD_Mat[1][1]

    ApD = (A + D)
    ADs2 = math.sqrt(ApD ** 2 - 4)

    ADm = A - D

    # does chap work on the im and real part
    gd = Chop(math.acosh(ApD / 2))

    B2 = 2 * B
    zb1 = -(B2 / (ADm - ADs2))

    zb = zb1 if zb1.real >= 0 else -(B2 / (ADm + ADs2))

    p, j = fpos(maxx, ceros, f)

    z = j - ((j - 1) % 2) if isOddInt(p) else j - (j % 2)

    igd = z * PI - gd.imag if z % 2 == 0 else gd.imag + (z - 1) * PI

    igd = 0 if igd % PI == 0 else igd

    gd = gd.real + 1j * igd

    return [gd, zb]


'''
Propagation constant and Bloch impedance
The propagation constant is obtained through ArcCosh[(A+D)/2]
ZB is selected such that Re[ZB] >= 0
Propagation constant calculated as GammaD
This function sets Im[Gamma] =0 or PI inside the gaps
'''
# TODO CHECK FOR CORRECTNESS


def GammaDZB10(ABCD_Mat, maxx, ceros, gaps, f):
    A = ABCD_Mat[0][0]
    B = ABCD_Mat[0][1]
    C = ABCD_Mat[1][0]
    D = ABCD_Mat[1][1]

    ApD = (A + D)
    ADs2 = math.sqrt(ApD ** 2 - 4)

    ADm = A - D

    gd = math.acosh(ApD / 2)
    B2 = 2 * B
    zb1 = - (B2 / (ADm - ADs2))

    zb = zb1 if zb1.real >= 0 else -(B2 / (ADm + ADs2))

    pp, jj = fpos(maxx, ceros, f)

    z = jj - ((jj - 1) % 2) if isOddInt(pp) else jj - (jj % 2)

    if jj > 1 and (gaps[jj - 1][1] <= f <= gaps[jj - 1][2]):
        igd = gd.imag
    else:
        if z % 2 == 0:
            igd = z * PI - gd.imag
        else:
            igd = gd.imag + (z - 1) * PI
    return [gd.real + 1j * igd, zb]


"""
Propagation constant and Bloch impedance
The propagation constant is obtained through ArcCosh[(A+D)/2]
ZB is selected such that Re[ZB] >= 0
Propagation constant calculated as Gamma d
No unfolding of Gamma
"""

# TODO CHECK FOR CORRECTNESS

def GammaDZBN(ABCD_Mat, maxx, f):
    A = ABCD_Mat[0][0]
    B = ABCD_Mat[0][1]
    C = ABCD_Mat[1][0]
    D = ABCD_Mat[1][1]

    ApD = (A + D)
    ADs2 = math.sqrt(ApD ** 2 - 4)

    ADm = A - D

    gd = math.acosh(ApD / 2)
    B2 = 2 * B
    zb1 = - (B2 / (ADm - ADs2))

    zb = zb1 if zb1.real >= 0 else -(B2 / (ADm + ADs2))

    return [gd, zb]


# Product of matrices TL[Z,Gamma,l]
# Z,Gamma,d are given as vectors
def prodTL(Z, Gamma, L):
    return np.multi_dot([ABCD_TL(Z[i], Gamma[i], L[i]) for i in range(len(Z))])


# Transmission of n identical cells
def S21Ncell(n, Zequ1, Zequ2, Gamma_equ, d, Zo):
    return (2 * math.exp(d * n * Gamma_equ) * (Zequ1 - Zequ2) * Zo) / (
            (1 + math.exp(2 * d * n * Gamma_equ)) * (Zequ1 - Zequ2) * Zo - (
            -1 + math.exp(2 * d * n * Gamma_equ)) * (Zequ1 * Zequ2 - Zo ^ 2))

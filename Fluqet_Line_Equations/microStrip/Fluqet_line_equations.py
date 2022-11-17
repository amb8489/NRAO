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


# Product of matrices TL[Z,Gamma,l]
# TODO WHERE CAN I GET THIS FILE of vectors
# Z,Gamma,d are given as vectors
def UnitCellABCD(Z, Gamma, L):
    res = [[1, 0],
           [0, 1]]
    for i in range(len(Z)):

        res = np.matmul(res, ABCD_TL(Z[i], Gamma[i], L[i]))

    return res


# input is an array of mats
def UnitCellABCD_mats(mats):
    res = mats[0]
    for mat in mats[1:]:

        res = [
            [res[0][0]*mat[0][0]+res[0][1]*mat[1][0] ,res[0][0]*mat[0][1]+res[0][1]*mat[1][1]],
            [res[1][0] * mat[0][0] + res[1][1] * mat[1][0], res[1][0] * mat[0][1] + res[1][1] * mat[1][1]]]


    return res


# Transmission of n identical cells
def S21Ncell(n, Zequ1, Zequ2, Gamma_equ, d, Zo):
    return (2 * math.exp(d * n * Gamma_equ) * (Zequ1 - Zequ2) * Zo) / (
            (1 + math.exp(2 * d * n * Gamma_equ)) * (Zequ1 - Zequ2) * Zo - (
            -1 + math.exp(2 * d * n * Gamma_equ)) * (Zequ1 * Zequ2 - (Zo ** 2)))


def S12(ABCD_Mat, Z):
    A = ABCD_Mat[0][0]
    B = ABCD_Mat[0][1]
    C = ABCD_Mat[1][0]
    D = ABCD_Mat[1][1]

    return 10 * cmath.log((2 * ((A * D) - (B * C))) / (A + B / Z + C * Z + D), 10)

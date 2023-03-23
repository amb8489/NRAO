import cmath
import math
import numpy as np
import scipy




# Computes the hyperbolic tangent of 𝑥 if x is floquet_alpha complex number
def ccoth(x):
    return 1 / cmath.tanh(x)


def hertz_to_GHz(frequency):
    return frequency * 1e9


def micro_meters_to_meters(micro_meter):
    return micro_meter / 1e+6


def nano_meters_to_meters(nm):
    return nm / 1e+9


def mm_to_meters(mm):
    return mm / 1000


def micro_ohms_cm_to_ohms_m(micro_ohms):
    return micro_ohms / 100000000


# matrix multiplication of 2x2 matrix
def mult_2x2_mat(mat1, mat2):
    # definition of matrix mult for 2x2 * 2x2
    return [
        [mat1[0][0] * mat2[0][0] + mat1[0][1] * mat2[1][0], mat1[0][0] * mat2[0][1] + mat1[0][1] * mat2[1][1]],
        [mat1[1][0] * mat2[0][0] + mat1[1][1] * mat2[1][0], mat1[1][0] * mat2[0][1] + mat1[1][1] * mat2[1][1]]]


# matrix multiplication of a list of 2x2 matrix
def mult_mats(mats):
    # input is an array of 2x2 matrices
    # does floquet_alpha matrix multiplication of all 2x2 matrices passed in,in array

    res = mats[0]
    for mat in mats[1:]:
        res = [
            [res[0][0] * mat[0][0] + res[0][1] * mat[1][0], res[0][0] * mat[0][1] + res[0][1] * mat[1][1]],
            [res[1][0] * mat[0][0] + res[1][1] * mat[1][0], res[1][0] * mat[0][1] + res[1][1] * mat[1][1]]
        ]
    return res



def ABCD_Mat(zc, gamma, line_length):
    gl = gamma * line_length
    coshGL = cmath.cosh(gl)
    sinhGL = cmath.sinh(gl)

    return [[coshGL, zc * sinhGL],
            [(1 / zc) * sinhGL, coshGL]]


def bloch_impedance_Zb(ABCD_mat_2x2: [[float]]):
    A = ABCD_mat_2x2[0][0]
    B = ABCD_mat_2x2[0][1]
    D = ABCD_mat_2x2[1][1]

    ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
    ADm = A - D

    B2 = 2 * B

    ZB = - (B2 / (ADm + ADs2))

    if ZB.real<0:
        return - (B2 / (ADm - ADs2))
    return ZB


def gamma_d(ABCD_mat_2x2: [[float]]):
    A = ABCD_mat_2x2[0][0]
    D = ABCD_mat_2x2[1][1]
    return cmath.acosh(((A + D) / 2))




#  elliptic integral redefined to contemplate Jochems change
def ellip_k(n):
    return scipy.special.ellipk(n)


# unfolds beta -- makes list of numbers monotonically increasing
def beta_unfold(lst):
    lst = np.abs(lst)
    differ = np.diff(lst) < 0
    acc = 0
    for i in range(1, len(lst)):
        lst[i] += acc
        if differ[i - 1]:
            diff = 2 * (lst[i - 1] - lst[i])
            acc += diff
            lst[i] += diff
    return lst



# debug print function that can be turned on and off using DEBUG_FLAG
DEBUG_FLAG = False
def printDb(*args):
    if DEBUG_FLAG:
        print("DEBUG: ", *args)


# calculates transmission s21 of N repeaded unit cells
def Transmission_Db(N, z0, ZB, floquet_gamma_d):
    # convert to ABCD N-cell matrix
    cosh_N_gamma_d = cmath.cosh(N * floquet_gamma_d)
    sinh_N_gammma_d = cmath.sinh(N * floquet_gamma_d)

    A = cosh_N_gamma_d
    B = ZB * sinh_N_gammma_d
    C = sinh_N_gammma_d / ZB
    D = cosh_N_gamma_d

    # calculate s21
    s21 = 2 / (A + (B / z0) + (C * z0) + D)

    return toDb(abs(s21))


def RLGC_circuit_factors(propagationConst: complex, Zb: complex):
    Z = propagationConst * Zb
    Y = propagationConst / Zb

    R = Z.real
    L = Z.imag

    G = Y.real
    C = Y.imag
    return R, L, G, C

# converts a number to Decibel
def toDb(number):
    return 10 * math.log10(number)

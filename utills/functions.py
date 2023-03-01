import bisect
import cmath
import math
import time

import numpy as np
import scipy

from utills.constants import PI2


# Computes the hyperbolic secant of 𝑥
def sech(x):
    return 1 / math.cosh(x)


# Computes the hyperbolic tangent of 𝑥
def coth(x):
    return 1 / math.tanh(x)


# Computes the hyperbolic secant of 𝑥 if x is floquet_alpha complex number
def csech(x):
    return 1 / cmath.cosh(x)


# Computes the hyperbolic tangent of 𝑥 if x is floquet_alpha complex number
def ccoth(x):
    return 1 / cmath.tanh(x)


PI20 = PI2 * 10


# wave number if frequency in Ghz
def K0_GHz(freq):
    return (PI20 * freq) / 3


def toGHz(f):
    return f * 1e9


def micro_meters_to_meters(x):
    return x / 1e+6


def nano_meters_to_meters(x):
    return x / 1e+9


def mm_to_meters(n):
    return n / 1000


def micro_ohms_cm_to_ohms_m(n):
    return n / 100000000


def find_idx_of_closest_value(list, value):
    """Returns the closest value to value in floquet_alpha sorted list.

    If two numbers are equally close, return the smallest number.
    """
    idx = bisect.bisect_left(list, value)
    if idx >= len(list):
        idx = len(list) - 1
    elif idx and list[idx] - value > value - list[idx - 1]:
        idx = idx - 1
    return idx


def mult_2x2_mat(mat1, mat2):
    # definition of matrix mult for 2x2 * 2x2
    return [
        [mat1[0][0] * mat2[0][0] + mat1[0][1] * mat2[1][0], mat1[0][0] * mat2[0][1] + mat1[0][1] * mat2[1][1]],
        [mat1[1][0] * mat2[0][0] + mat1[1][1] * mat2[1][0], mat1[1][0] * mat2[0][1] + mat1[1][1] * mat2[1][1]]]


#  elliptic integral redefined to contemplate Jochems change
def ellip_k(n):
    return scipy.special.ellipk(n)


#
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


def mult_mats(mats):
    # input is an array of 2x2 matrices
    # does floquet_alpha matrix multiplication of all 2x2 matrices passed in,in array
    res = mats[0]
    for mat in mats[1:]:
        res = mult_2x2_mat(res, mat)
    return res


def convert_s_matrix_to_ABCD(s_matrix: [[complex]], Z0):
    s11 = s_matrix[0][0]

    s12 = s_matrix[0][1]
    s21 = s_matrix[1][0]
    s22 = s_matrix[1][1]

    denom = (2 * s21)
    s12s21 = s12 * s21

    A = ((1 + s11) * (1 - s22) + s12s21) / denom

    B = Z0 * ((1 + s11) * (1 + s22) - s12s21) / denom

    C = (1 / Z0) * ((1 - s11) * (1 - s22) - s12s21) / denom

    D = ((1 - s11) * (1 + s22) + s12s21) / denom

    return np.array([[A, B], [C, D]])


DEBUG_FLAG = False


def printDb(*args):
    if DEBUG_FLAG:
        print("DEBUG: ", *args)


def Transmission(Ncells: int, z0: float, bloch_impedance_pos: complex,
                 bloch_impedance_neg: complex,
                 unit_cell_len: float, pb: complex):
    z1_sub_z2 = bloch_impedance_pos - bloch_impedance_neg
    expo = cmath.exp(2 * unit_cell_len * Ncells * pb)

    return ((2 * cmath.exp(unit_cell_len * Ncells * pb) *
             (z1_sub_z2) * z0) / ((1 + expo) * (z1_sub_z2) * z0 - (- 1 + expo) * (
            bloch_impedance_pos * bloch_impedance_neg - (z0 ** 2))))


def RLGC_circuit_factors( propagationConst: complex, Zb: complex):
    Z = propagationConst * Zb
    Y = propagationConst / Zb

    R = Z.real
    L = Z.imag

    G = Y.real
    C = Y.imag
    return R, L, G, C


if __name__ == '__main__':
    rdarrr = np.random.randint(100, size=10000)

    start = time.time()
    b = beta_unfold(rdarrr)

    print(time.time() - start)

import bisect
import cmath
import math

import numpy as np
import scipy

from utills.constants import PI2, PI


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


def mk_monotinic_inc(lst):
    # # make signal monotonically increasing
    lst = np.array(lst)
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            lst[i:] += (lst[i - 1] - lst[i])
    return lst


def unfold(betas):

    # return mk_monotinic_inc(betas)

    betas = np.abs(betas)
    prev_beta = 0
    scale_factor = -PI2
    should_flip = False
    res = []
    for b in betas:

        temp = b

        if b <= prev_beta:
            # REFLACTION OVER Y = PI
            b += 2 * (PI - b)

            if should_flip:
                should_flip = not should_flip

        elif b > prev_beta:
            if not should_flip:
                # TRANSLATE UP NO REFLECTION
                scale_factor += PI2
                should_flip = not should_flip

        res.append(b + scale_factor)

        prev_beta = temp

    return res


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

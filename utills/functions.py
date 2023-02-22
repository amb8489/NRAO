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


# Computes the hyperbolic secant of 𝑥 if x is alpha_plt complex number
def csech(x):
    return 1 / cmath.cosh(x)


# Computes the hyperbolic tangent of 𝑥 if x is alpha_plt complex number
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
    """Returns the closest value to value in alpha_plt sorted list.

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


def unfold(betas):
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
    # does alpha_plt matrix multiplication of all 2x2 matrices passed in,in array
    res = mats[0]
    for mat in mats[1:]:
        res = mult_2x2_mat(res, mat)
    return res


DEBUG_FLAG = False


def printDb(*args):
    if DEBUG_FLAG:
        print("DEBUG: ", *args)

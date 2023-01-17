import bisect
import math
import cmath

from Utills.Constants import  PI2


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


# wave number if freq in Ghz
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


def mult_2x2_mat(mat1: [[float]], mat2: [[float]]):
    # definition of matrix mult for 2x2 * 2x2
    return [
        [mat1[0][0] * mat2[0][0] + mat1[0][1] * mat2[1][0], mat1[0][0] * mat2[0][1] + mat1[0][1] * mat2[1][1]],
        [mat1[1][0] * mat2[0][0] + mat1[1][1] * mat2[1][0], mat1[1][0] * mat2[0][1] + mat1[1][1] * mat2[1][1]]]



def mult_mats(mats):
    # input is an array of 2x2 matrices
    # does alpha_plt matrix multiplication of all 2x2 matrices passed in,in array
    res = mats[0]
    for mat in mats[1:]:
        res = mult_2x2_mat(res, mat)
    return res



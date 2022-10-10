import math
import cmath

from Supports.constants import cc, PI2


# Computes the hyperbolic secant of 𝑥
def sech(x):
    return 1 / math.cosh(x)


# Computes the hyperbolic tangent of 𝑥
def coth(x):
    return 1 / math.tanh(x)


# Computes the hyperbolic secant of 𝑥 if x is a complex number
def csech(x):
    return 1 / cmath.cosh(x)


# Computes the hyperbolic tangent of 𝑥 if x is a complex number
def ccoth(x):
    return 1 / cmath.tanh(x)


# wave number if freq in Ghz
def K0_GHz(freq):
    return (PI2 * 10 * freq) / cc

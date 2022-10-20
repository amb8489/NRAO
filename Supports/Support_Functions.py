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


# TODO test
# returns true if number is an int and odd otherwise false
def isOddInt(n):
    if isinstance(n, int):
        return n & 1
    return False


def Chop(n, max=9):
    realPart = abs(n.real)

    return 1

    # out = 0 if realPart <= max else n.real
    #
    # if decimalOfReal <= max:
    #     out = intReal


def Chop(number, decimals=6):
    """
    Returns a value truncated to a specific number of decimal places.

    basically if a number is like 1.00000000132434 itll just be 1.0
    """

    factor = 10.0 ** decimals
    return (math.trunc(number.real * factor) / factor) + (1j * math.trunc(number.imag * factor) / factor)

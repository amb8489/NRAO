
import math
import cmath

# Computes the hyperbolic secant of 𝑥
def sech(x):
    return 1/ math.cosh(x)


# Computes the hyperbolic tangent of 𝑥
def coth(x):
    return 1 / math.tanh(x)


# Computes the hyperbolic secant of 𝑥 if x if a complex number
def csech(x):
    return 1 / cmath.cosh(x)


# Computes the hyperbolic tangent of 𝑥 if a complex number
def ccoth(x):
    return 1 / cmath.tanh(x)

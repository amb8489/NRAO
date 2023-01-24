import math
import scipy.constants

"""
useful constants

"""

# PI consts
PI = math.pi
PI2 = 2 * math.pi
PI4 = 4 * math.pi

# Planck's constant UNITS ev.s
PLANCK_CONSTev = 4.135667662E-15

# PLANCK_CONST REDUCED in ev.s
PLANCK_CONST_REDUCEDev = PLANCK_CONSTev / PI2

# Boltzmann's constant in eV/K
BOLTZMANN_CONSTev = 8.6173303E-5
KB = 8.6173303E-5
# The vacuum magnetic permeability in UNITS h.m^-1
MU_0 = PI4 * (10 ** -7)

# characteristic impedance of vacuum in UNITS ohm's
Z0 = 120 * PI

# Giga hertz
GHZ = 10 ** 9

# speed of light m/s
C = scipy.constants.speed_of_light

SPEED_OF_LIGHT = scipy.constants.speed_of_light

PI_DIV_2 = math.pi / 2


epsilono = ...

# nano meter
NANO_METER = 10 ** -9

micro_METER = 10 ** -6

CM = 10 ** -2

MM = 10 ** -3


# wave number
def K0(f):
    return PI2 / (C / f)

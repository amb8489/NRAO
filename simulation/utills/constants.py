import math
import scipy.constants

"""
                        
                            useful constants
"""

# PI consts
PI = math.pi
PI2 = 2 * math.pi
PI4 = 4 * math.pi
PI_DIV_2 = math.pi / 2

# Planck's constant UNITS ev.s
PLANCK_CONSTev = 4.135667662E-15

# PLANCK_CONST REDUCED in ev.s
PLANCK_CONST_REDUCEDev = PLANCK_CONSTev / PI2

# Boltzmann's constant in eV/K
BOLTZMANN_CONSTev = 8.6173303E-5

# The vacuum magnetic permeability in UNITS h.m^-1
MU_0 = PI4 * (10 ** -7)

# characteristic impedance of vacuum in UNITS ohm's
Z0 = 120 * PI

# speed of light m/s
SPEED_OF_LIGHT = scipy.constants.speed_of_light


#Vacuum permittivity
epsilon_0 = 8.854187*10**-12

# lengths meter
NANO_METER = 10 ** -9
MICRO_METER = 10 ** -6
CM = 10 ** -2
MM = 10 ** -3


# wave number
def K0(f):
    return PI2 / (SPEED_OF_LIGHT / f)


# model names
MICRO_STRIP_TYPE = "MICRO_STRIP"
CPW_TYPE = "CPW"
ARTIFICIAL_CPW = "ARTIFICIAL_CPW"
HFSS_TOUCHSTONE_FILE = "HFSS_TOUCHSTONE_FILE"


import math

import scipy.constants

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

# The vacuum magnetic permeability in UNITS H.m^-1
MU_0 = PI4 * (10 ** -7)

# characteristic impedance of vacuum in UNITS ohm's
z0 = 120 * PI

# Giga hertz
GHz = 10 ** 9

# speed of light m/s
c = scipy.constants.speed_of_light

# speed of light m/s for GHz freq
cc = 3

# nano meter
nano_meter = 10 ** -9

micro_meter = 10 ** -6

cm = 10 ** -2

mm = 10 ** -3

# wave number when freq is in GHz
# TODO is this right
K0 = (PI2 * 10) / cc

# Impedance of free space
N0 = 120 * PI

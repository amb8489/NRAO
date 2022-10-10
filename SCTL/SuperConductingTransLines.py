"""

Aaron Berghash this code will take in a model and take from that model

g1 g2 Zs epsilon_fm


"""

import cmath
from Supports.constants import N0, K0

"""
series impedance of a TEM transmission line
ko is the free-space wavenumber
No is the impedance of free space
Zs, is the surface impedance of the conductors
g1 and g2 are geometrical factors, which characterize the particular transmission line being used.
"""


def series_impedance_Z(Zs, g1, g2):
    return (1j * (K0 * N0) * g1) + (2 * g2 * Zs)


"""
shunt admittance of a TEM transmission line
ko is the free-space wavenumber
No is the impedance of free space
epsilon_fm the effective dielectric constant in the modal sense.
g1 is a geometrical factor, which characterize the particular transmission line being used.
"""


# TODO where does is epsilon_fm come from and is it model dependent
def shunt_admittance_Y(epsilon_fm, g1):
    return 1j * (K0 / N0) * (epsilon_fm / g1)


# Zc
def characteristic_impedance(Z, Y):
    return cmath.sqrt(Z / Y)


def propagation_constant(Z, Y):
    return cmath.sqrt(Y * Z)

    # TOdo what are these used for where do we calc these?
    # attenuation const
    # alpha = ...
    #
    # # wave number
    #
    # beta = ...

    pass

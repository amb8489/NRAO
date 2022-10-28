"""
NRAO
Aaron Berghash amb8489@g.rit.edu
"""
import cmath
import math

from scipy.integrate import quad

from Supports.Support_Functions import ccoth
from Supports.constants import BOLTZMANN_CONSTev, PLANCK_CONSTev, PI2, MU_0, KB

"""
---INPUTS---

freq range    : the range of DC frequency to test in units of GHz
conductivity  : the temperature of operation in Kelvin
ts            : thickness of super conductor
Pn            : normal resistivity
TempK         : temp of operation in kelvin


---OUT---

conductivity 
Zs (surface in impedance)         
"""

'''
------------------------------functions to support conductivity ------------------------------
'''


def e1(e, delta):
    return math.sqrt(e ** 2 - delta ** 2)


def e2(e, delta, freq):
    return math.sqrt(((e + freq) ** 2) - delta ** 2)


def e3(e, delta, freq):
    return (e ** 2) + (delta ** 2) + (freq * e)


def e4(e, delta):
    return math.sqrt(delta ** 2 - e ** 2)


def g(e, delta, freq):
    return e3(e, delta, freq) / (e1(e, delta) * e2(e, delta, freq))


def g2(e, delta, freq):
    bottom = ((e4(e, delta) * e2(e, delta, freq)) )
    if bottom == 0:
        bottom = .0000001
    return e3(e, delta, freq) / bottom


# ---- WHEN TEMPK IS 0
# put 0 for freq when not adding anything to E and put the freq when adding any value to e when temp is zero
# fermiDistrib E             -> fermiDistrib(E, 0)
# fermiDistrib E + someValue -> fermiDistrib(E + someValue, 0, someValue)
# the freq tells use where the step is when temp is 0

# ---- WHEN TEMPK IS NOT ZERO:
# fermiDistrib E             -> fermiDistrib(E, 0)
# fermiDistrib E + someValue -> fermiDistrib(E + someValue, 0)

def fermiDistrib(E, tempK, freq=0):
    # special case for temp = 0
    if tempK == 0:

        if (E - freq) >= -freq:
            return 0
        return 1
    # normal case for temp > 0

    # math.exp(E / tempK) can be extremely large e^ 2000 +
    # at very lage math.exp(E / tempK) we just return 0
    try:
        return 1 / (1 + math.exp(E / tempK))
    except OverflowError:
        return 0


def ff(e, freq, tempK):
    return fermiDistrib(e, tempK, 0) - fermiDistrib(e + freq, tempK, freq)


def f2(e, freq, tempK):
    return 1 - (2 * fermiDistrib(e + freq, tempK, freq))


def int1(e, delta, freq, tempK):
    return ff(e, freq, tempK) * g(e, delta, freq)


def int11(e, delta, freq, tempK):
    return f2(e, freq, tempK) * g(e, delta, freq)


def int2(e, delta, freq, tempK):
    return f2(e, freq, tempK) * g2(e, delta, freq)


def sigma_1_N_L(delta, freq, tempK):
    f = lambda x: int1(delta + x ** 2, delta, freq, tempK) * 2 * x

    lower_bound = 0
    upper_bound = 20 * math.sqrt(delta)
    return (2 / freq) * quad(f, lower_bound, upper_bound)[0]


def sigma_1_N_U(delta, freq, tempK):
    f1 = lambda x: int11(delta - freq + x ** 2, delta, freq, tempK) * 2 * x
    f2 = lambda x: int11(-delta - x ** 2, delta, freq, tempK) * 2 * x

    lower_bound = 0
    upper_bound = math.sqrt((freq / 2) - delta)
    return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])


def sigma_1_N(delta, freq, tempK):
    if freq <= 2 * delta:
        return sigma_1_N_L(delta, freq, tempK)
    return sigma_1_N_L(delta, freq, tempK) - sigma_1_N_U(delta, freq, tempK)


def sigma_2_N_L(delta, freq, tempK):
    f1 = lambda x: int2(delta - freq + x ** 2, delta, freq, tempK) * 2 * x
    f2 = lambda x: int2(delta - x ** 2, delta, freq, tempK) * 2 * x

    lower_bound = 0
    upper_bound = math.sqrt(freq / 2)
    return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])


def sigma_2_N_U(delta, freq, tempK):
    f1 = lambda x: int2(-delta + x ** 2, delta, freq, tempK) * 2 * x
    f2 = lambda x: int2(delta - x ** 2, delta, freq, tempK) * 2 * x

    lower_bound = 0
    upper_bound = math.sqrt(delta)
    return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])


def sigma_2_N(delta, freq, tempK):
    if freq <= 2 * delta:
        return sigma_2_N_L(delta, freq, tempK)
    return sigma_2_N_U(delta, freq, tempK)


def Delta_O(critical_temp):
    return 1.764 * BOLTZMANN_CONSTev * critical_temp


def calc_delta(temperature, critical_temp):
    PiDiv2 = math.pi / 2
    TempDiv = temperature / critical_temp

    return Delta_O(critical_temp) * math.sqrt(math.cos(PiDiv2 * (TempDiv ** 2)))


def sigma_N(delta, freq, tempK):

    return sigma_1_N(delta, freq, tempK) - 1j * sigma_2_N(delta, freq, tempK)


def gap_freq(delta):
    return (2 * delta) / PLANCK_CONSTev


def conductivityNormalized(freq, Operation_temperatureK, critical_temp):
    delta = calc_delta(Operation_temperatureK, critical_temp)
    return sigma_N(delta, freq, Operation_temperatureK)



"""
-INPUTS-

freq                    : frequency of DC i units of GHz
Operation_temperatureK  : the temperature of operation in Kelvin
critical_temp           : the temperature of transition between normal and super conductor in Kelvin
Pn                      : normal resistivity in micro ohms / cm


-OUT-
 
conductivity            : is the conductivity at input conditions
"""


def conductivity(freq, Operation_temperatureK, critical_temp, Pn):
    delta = calc_delta(Operation_temperatureK, critical_temp)

    return sigma_N(delta, freq*PLANCK_CONSTev, Operation_temperatureK*KB)







"""
-INPUTS-

freq          : frequency of DC i units of GHz
conductivity  : conductivity
ts            : thickness of super conductor

-OUT-

Zs - surface impenitence          
"""


def Zs(freq, Conductivity, ts):
    # TODO ask about the complex square root should just the real part be rooted or both re and im parts

    a = cmath.sqrt((1j * PI2 * freq * MU_0) / Conductivity)
    b = ccoth(cmath.sqrt(1j * PI2 * freq * MU_0 * Conductivity) * ts)
    
    return a * b

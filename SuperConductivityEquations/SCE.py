'''
NRAO
Aaron Berghash amb8489@g.rit.edu
'''

import math
from scipy.integrate import quad
from constants import BOLTZMANN_CONSTev, PLANCKC_CONST

'''
------------------------------definitions------------------------------
'''


def e1(e, delta):
    return math.sqrt(e ** 2 - delta ** 2)


def e2(e, delta, freq):
    return math.sqrt(((e + freq) ** 2) - delta ** 2)


def e3(e, delta, freq):
    return e ** 2 + delta ** 2 + freq * e


def e4(e, delta):
    return math.sqrt(delta ** 2 - e ** 2)


def g(e, delta, freq):
    return e3(e, delta, freq) / (e1(e, delta) * e2(e, delta, freq))


def g2(e, delta, freq):
    return e3(e, delta, freq) / (e4(e, delta) * e2(e, delta, freq))


# TODO careful when tempK = 0
def fd(E, tempK):


    # if tempK == 0:
    #
    #     if E  >= 0:
    #         return 0
    #     return 1

    return 1 / (1 + math.exp(E / tempK ))


def ff(e, freq, tempK):
    return fd(e, tempK) - fd(e + freq, tempK)


def f2(e, freq, tempK):
    return 1 - (2 * fd(e + freq, tempK))


def int1(e, delta, freq, tempK):
    return ff(e, freq, tempK) * g(e, delta, freq)


def int11(e, delta, freq, tempK):
    return f2(e, freq, tempK) * g(e, delta, freq)


def int2(e, delta, freq, tempK):
    return f2(e, freq, tempK) * g2(e, delta, freq)


def sigma_1_N_L(delta, freq, tempK):
    lower = 0
    upper = 20 * math.sqrt(delta)
    f = lambda x: int1(delta + x ** 2, delta, freq, tempK) * 2 * x

    return (2 / freq) * quad(f, lower, upper)[0]


def sigma_1_N_U(delta, freq, tempK):
    lower = 0
    upper = math.sqrt((freq / 2) - delta)

    f1 = lambda x: int11(delta - freq + x ** 2, delta, freq, tempK) * 2 * x
    f2 = lambda x: int11(-delta - x ** 2, delta, freq, tempK) * 2 * x

    return (1 / freq) * (quad(f1, lower, upper)[0] + quad(f2, lower, upper)[0])


def sigma_1_N(delta, freq, tempK):
    if freq <= 2 * delta:
        return sigma_1_N_L(delta, freq, tempK)
    return sigma_1_N_L(delta, freq, tempK) - sigma_1_N_U(delta, freq, tempK)


def sigma_2_N_L(delta, freq, tempK):
    lower = 0
    upper = math.sqrt((freq / 2))

    f1 = lambda x: int2(delta - freq + x ** 2, delta, freq, tempK) * 2 * x
    f2 = lambda x: int2(delta - x ** 2, delta, freq, tempK) * 2 * x

    return (1 / freq) * (quad(f1, lower, upper)[0] + quad(f2, lower, upper)[0])


def sigma_2_N_U(delta, freq, tempK):
    lower = 0
    upper = math.sqrt(delta)

    f1 = lambda x: int2(-delta + x ** 2, delta, freq, tempK) * 2 * x
    f2 = lambda x: int2(delta - x ** 2, delta, freq, tempK) * 2 * x

    return (1 / freq) * (quad(f1, lower, upper)[0] + quad(f2, lower, upper)[0])


def sigma_2_N(delta, freq, tempK):
    if freq <= 2 * delta:
        return sigma_2_N_L(delta, freq, tempK)
    return sigma_2_N_U(delta, freq, tempK)


def Delta_O(critical_temp):
    return 1.764 * BOLTZMANN_CONSTev * critical_temp


def calc_delta(temperature, critical_temp):

    PiDiv2 = math.pi / 2
    TempDiv = temperature / critical_temp

    # TODO careful of units of boltzsman const

    return Delta_O(critical_temp) * math.sqrt( math.cos( PiDiv2 * (TempDiv ** 2)) )


def sigma_N(delta, freq, tempK):
    return sigma_1_N(delta, freq, tempK) - 1j * sigma_2_N(delta, freq, tempK)


def gap_freq(delta):
    return (2 * delta) / PLANCKC_CONST


def conductivity(freq, temperatureK, critical_temp):
    # test plot

    delta = calc_delta(temperatureK, critical_temp)
    return sigma_N(delta, freq, temperatureK)

delta = calc_delta(0, 14.1)
deltaO = Delta_O(14.1)

print("delta:  ",delta)
print("deltaO: ",deltaO)
print("fgap : ",gap_freq(delta))





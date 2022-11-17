"""
NRAO
Aaron Berghash amb8489@g.rit.edu
"""
import cmath
import math
from scipy.integrate import quad
from Supports.Support_Functions import ccoth
from Supports.constants import PLANCK_CONSTev, PI2, MU_0, KB, PiDiv2


class SuperConductivity():
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

    def __init__(self, Operation_temperatureK, critical_temp, Pn,cached = False):

        # calulations that only need to be done once per run

        self.sigma = 1 / Pn
        self.TempDiv = Operation_temperatureK / critical_temp
        self.jPI2MU_0 = 1j * PI2 * MU_0
        self.delta = self.calc_delta(critical_temp)
        self.OpTempTimesKB = Operation_temperatureK * KB



        # opt cache for a run

    def e1(self, e, delt):
        return math.sqrt(e ** 2 - delt ** 2)

    def e2(self, e, delt, freq):
        return math.sqrt(((e + freq) ** 2) - delt ** 2)

    def e3(self, e, delt, freq):
        return (e ** 2) + (delt ** 2) + (freq * e)

    def e4(self, e, delt):
        return math.sqrt(delt ** 2 - e ** 2)

    def g(self, e, delt, freq):
        return self.e3(e, delt, freq) / (self.e1(e, delt) * self.e2(e, delt, freq))

    def g2(self, e, delt, freq):
        bottom = ((self.e4(e, delt) * self.e2(e, delt, freq)))

        if bottom == 0:
            bottom = .00001

        return self.e3(e, delt, freq) / (bottom)

    # ---- WHEN TEMPK IS 0
    # put 0 for freq when not adding anything to E and put the freq when adding any value to e when temp is zero
    # fermiDistrib E             -> fermiDistrib(E, 0)
    # fermiDistrib E + someValue -> fermiDistrib(E + someValue, 0, someValue)
    # the freq tells use where the step is when temp is 0

    # ---- WHEN TEMPK IS NOT ZERO:
    # fermiDistrib E             -> fermiDistrib(E, 0)
    # fermiDistrib E + someValue -> fermiDistrib(E + someValue, 0)

    # TODO come back to this and maybe just simplify  the (E - freq)

    def fermiDistrib(self, E, tempK, freq=0):



        if tempK == 0:
            return 0 if (E - freq) >= -freq else 1

        edivk = E / tempK
        return 0 if edivk > 30 else 1 / (1 + math.exp(edivk))


    def ff(self, e, freq, tempK):
        return self.fermiDistrib(e, tempK, 0) - self.fermiDistrib(e + freq, tempK, freq)

    def f2(self, e, freq, tempK):
        return 1 - (2 * self.fermiDistrib(e + freq, tempK, freq))

    def int1(self, e, delt, freq, tempK):
        # opt g(e, delta, freq) could maybe be cached

        return self.ff(e, freq, tempK) * self.g(e, delt, freq)

    def int11(self, e, delt, freq, tempK):
        return self.f2(e, freq, tempK) * self.g(e, delt, freq)

    def int2(self, e, delt, freq, tempK):
        return self.f2(e, freq, tempK) * self.g2(e, delt, freq)

    def sigma_1_N_L(self, delt, freq, tempK):

        def f(x):
            return self.int1(delt + x ** 2, delt, freq, tempK) * 2 * x

        lower_bound = 0
        upper_bound = 20 * math.sqrt(delt)
        return (2 / freq) * quad(f, lower_bound, upper_bound)[0]

    def sigma_1_N_U(self, delt, freq, tempK):

        def f1(x):
            return self.int11(delt - freq + x ** 2, delt, freq, tempK) * 2 * x

        def f2(x):
            return self.int11(-delt - x ** 2, delt, freq, tempK) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt((freq / 2) - delt)

        return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def sigma_1_N(self, delt, freq, tempK):
        if freq <= 2 * delt:
            return self.sigma_1_N_L(delt, freq, tempK)
        return self.sigma_1_N_L(delt, freq, tempK) - self.sigma_1_N_U(delt, freq, tempK)

    def sigma_2_N_L(self, delt, freq, tempK):

        def f1(x):
            return self.int2(delt - freq + x ** 2, delt, freq, tempK) * 2 * x

        def f2(x):
            return self.int2(delt - x ** 2, delt, freq, tempK) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt(freq / 2)

        return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def sigma_2_N_U(self, delt, freq, tempK):

        def f1(x):
            return self.int2(-delt + x ** 2, delt, freq, tempK) * 2 * x

        def f2(x):
            return self.int2(delt - x ** 2, delt, freq, tempK) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt(delt)
        return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def sigma_2_N(self, delt, freq, tempK):
        if freq <= 2 * delt:
            return self.sigma_2_N_L(delt, freq, tempK)
        return self.sigma_2_N_U(delt, freq, tempK)

    def Delta_O(self, critical_temp):
        return 1.764 * KB * critical_temp

    def calc_delta(self, critical_temp):
        return self.Delta_O(critical_temp) * math.sqrt(math.cos(PiDiv2 * (self.TempDiv ** 2)))

    def sigma_N(self, delt, freq, tempK):
        return self.sigma_1_N(delt, freq, tempK) - 1j * self.sigma_2_N(delt, freq, tempK)

    def gap_freq(self, delt):
        return (2 * delt) / PLANCK_CONSTev

    def conductivityNormalized(self, freq, Operation_temperatureK):
        return self.sigma_N(self.delta, freq, Operation_temperatureK)

    """
    -INPUTS-
    freq                    : frequency of DC i units of GHz
    Operation_temperatureK  : the temperature of operation in Kelvin
    critical_temp           : the temperature of transition between normal and super conductor in Kelvin
    Pn                      : normal resistivity in micro ohms / cm
    -OUT-
     
    conductivity            : is the conductivity at input conditions
    """

    def conductivity(self, freq):
        return self.sigma * self.sigma_N(self.delta, freq * PLANCK_CONSTev, self.OpTempTimesKB)

    """
    -INPUTS-
    freq          : frequency of DC i units of GHz
    conductivity  : conductivity
    ts            : thickness of super conductor
    -OUT-
    Zs - surface impenitence          
    """

    def Zs(self, freq, Conductivity, ts):
        # opt might be able to do this ad a numppy op for all freq then index into it
        # opt (1j * PI2 * MU_0) * np.linspace(StartFreq, EndFreq, resolution)

        return cmath.sqrt(self.jPI2MU_0 * freq / Conductivity) * ccoth(
            cmath.sqrt(self.jPI2MU_0 * freq * Conductivity) * ts)

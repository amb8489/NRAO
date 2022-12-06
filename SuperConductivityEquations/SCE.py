"""



"""
import cmath
import math
from scipy.integrate import quad
from utills_funcs_and_consts.Functions import ccoth
from utills_funcs_and_consts.Constants import PLANCK_CONSTev, PI2, MU_0, KB, PiDiv2


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

    def __init__(self, Operation_temperatureK, critical_temp, Pn):

        # calulations that only need to be done once per run

        self.sigma = 1 / Pn
        self.TempDiv = Operation_temperatureK / critical_temp
        self.jPI2MU_0 = 1j * PI2 * MU_0
        self.delta = self.calc_delta(critical_temp)
        self.OpTempTimesKB = Operation_temperatureK * KB

    def fermiDistrib(self, E, tempK):
        if tempK == 0:
            return 0 if E >= 0 else 1

        EdivT = E / tempK
        return 0 if EdivT > 30 else 1 / (1 + math.exp(EdivT))

    def g2(self, e, delt, freq):

        deltdSqrd = delt ** 2
        eSqrd = e ** 2

        return ((eSqrd) + (deltdSqrd) + (freq * e)) / (
                (math.sqrt(deltdSqrd - eSqrd)) * (math.sqrt(((e + freq) ** 2) - deltdSqrd)))

    def int1(self, e, delt, freq, tempK):
        deltdSqrd = delt ** 2
        eSqrd = e ** 2

        return (self.fermiDistrib(e, tempK) - self.fermiDistrib(e + freq, tempK)) * (
                ((eSqrd) + (deltdSqrd) + (freq * e)) / (
                    (math.sqrt(eSqrd - deltdSqrd)) * (math.sqrt(((e + freq) ** 2) - deltdSqrd))))

    def int11(self, e, delt, freq, tempK):

        deltdSqrd = delt ** 2
        eSqrd = e ** 2

        return ((1 - (2 * self.fermiDistrib(e + freq, tempK))) * (
                (eSqrd + deltdSqrd + (freq * e)) / (
                    (math.sqrt(eSqrd - deltdSqrd)) * (math.sqrt(((e + freq) ** 2) - deltdSqrd)))))

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
            e = delt - freq + x ** 2
            return ((1 - (2 * self.fermiDistrib(e + freq, tempK))) * self.g2(e, delt, freq)) * 2 * x

        def f2(x):
            e = delt - x ** 2
            return ((1 - (2 * self.fermiDistrib(e + freq, tempK))) * self.g2(e, delt, freq)) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt(freq / 2)

        return (1 / freq) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def sigma_2_N_U(self, delt, freq, tempK):

        def f1(x):
            e = -delt + x ** 2
            return ((1 - (2 * self.fermiDistrib(e + freq, tempK))) * self.g2(e, delt, freq)) * 2 * x

        def f2(x):
            e = delt - x ** 2
            return ((1 - (2 * self.fermiDistrib(e + freq, tempK))) * self.g2(e, delt, freq)) * 2 * x

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
    Zs - surface impedance           
    """

    def Zs(self, freq, Conductivity, ts):
        return cmath.sqrt(self.jPI2MU_0 * freq / Conductivity) * ccoth(
            cmath.sqrt(self.jPI2MU_0 * freq * Conductivity) * ts)

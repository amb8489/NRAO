"""


BCS theory on conductivity
"""
import cmath
import math
from scipy.integrate import quad

from simulation.utills.constants import MU_0, PI2, BOLTZMANN_CONSTev, PI_DIV_2, PLANCK_CONSTev
from simulation.utills.functions import ccoth


class SuperConductivity():
    """
    ---INPUTS---
    frequency range    : the range of DC frequency to


    test in units of GHZ
    conductivity  : the temperature of operation in Kelvin
    sc_film_thickness            : thickness of super conductor
    Pn            : normal resistivity
    TempK         : temp of operation in kelvin
    ---OUT---
    conductivity
    Zs (surface in impedance)
    """

    '''
    ------------------------------functions to support conductivity ------------------------------
    '''

    def __init__(self, operation_temperature_k: float, critical_temp_k: float, Pn: float):

        # calulations that only need to be done once per run

        self.crit_temp = critical_temp_k
        self.operation_temperature_k = operation_temperature_k

        self.__sigma = 1 / Pn
        self.__temp_div = operation_temperature_k / critical_temp_k
        self.__jPI2MU_0 = 1j * PI2 * MU_0
        self.__delta = self.__calc_delta(critical_temp_k)
        self.__op_temp_times_kb = operation_temperature_k * BOLTZMANN_CONSTev

    def get_sigma(self):
        return self.__sigma

    def __fermiDistrib(self, E: float, temp_k: float):

        if temp_k == 0:
            # todo retur 0 or .5 if E >= 0

            return 0 if E >= 0 else 1

        EdivT = E / temp_k
        return 0 if EdivT > 30 else 1 / (1 + math.exp(EdivT))

    def __g2(self, e: float, delt: float, frequency: float):

        deltdSqrd = delt ** 2
        eSqrd = e ** 2

        return ((eSqrd) + (deltdSqrd) + (frequency * e)) / (
                (math.sqrt(deltdSqrd - eSqrd)) * (math.sqrt(((e + frequency) ** 2) - deltdSqrd)))

    def __int1(self, e: float, delt: float, frequency: float, temp_k: float):
        deltdSqrd = delt ** 2
        eSqrd = e ** 2

        return (self.__fermiDistrib(e, temp_k) - self.__fermiDistrib(e + frequency, temp_k)) * (
                ((eSqrd) + (deltdSqrd) + (frequency * e)) / (
                (math.sqrt(eSqrd - deltdSqrd)) * (math.sqrt(((e + frequency) ** 2) - deltdSqrd))))

    def __int11(self, e: float, delt: float, frequency: float, temp_k: float):

        deltdSqrd = delt ** 2
        eSqrd = e ** 2

        return ((1 - (2 * self.__fermiDistrib(e + frequency, temp_k))) * (
                (eSqrd + deltdSqrd + (frequency * e)) / (
                (math.sqrt(eSqrd - deltdSqrd)) * (math.sqrt(((e + frequency) ** 2) - deltdSqrd)))))

    def __sigma_1_N_L(self, delt: float, frequency: float, temp_k: float):

        def f(x):
            return self.__int1(delt + x ** 2, delt, frequency, temp_k) * 2 * x

        lower_bound = 0
        upper_bound = 20 * math.sqrt(delt)
        return (2 / frequency) * quad(f, lower_bound, upper_bound)[0]

    def __sigma_1_N_U(self, delt: float, frequency: float, temp_k: float):

        def f1(x):
            return self.__int11(delt - frequency + x ** 2, delt, frequency, temp_k) * 2 * x

        def f2(x):
            return self.__int11(-delt - x ** 2, delt, frequency, temp_k) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt((frequency / 2) - delt)

        return (1 / frequency) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def __sigma_1_N(self, delt: float, frequency: float, temp_k: float):
        if frequency <= 2 * delt:
            return self.__sigma_1_N_L(delt, frequency, temp_k)
        return self.__sigma_1_N_L(delt, frequency, temp_k) - self.__sigma_1_N_U(delt, frequency, temp_k)

    def __sigma_2_N_L(self, delt: float, frequency: float, temp_k: float):

        def f1(x):
            e = delt - frequency + x ** 2
            return ((1 - (2 * self.__fermiDistrib(e + frequency, temp_k))) * self.__g2(e, delt, frequency)) * 2 * x

        def f2(x):
            e = delt - x ** 2
            return ((1 - (2 * self.__fermiDistrib(e + frequency, temp_k))) * self.__g2(e, delt, frequency)) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt(frequency / 2)

        return (1 / frequency) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def __sigma_2_N_U(self, delt: float, frequency: float, temp_k: float):

        def f1(x):
            e = -delt + x ** 2
            return ((1 - (2 * self.__fermiDistrib(e + frequency, temp_k))) * self.__g2(e, delt, frequency)) * 2 * x

        def f2(x):
            e = delt - x ** 2
            return ((1 - (2 * self.__fermiDistrib(e + frequency, temp_k))) * self.__g2(e, delt, frequency)) * 2 * x

        lower_bound = 0
        upper_bound = math.sqrt(delt)
        return (1 / frequency) * (quad(f1, lower_bound, upper_bound)[0] + quad(f2, lower_bound, upper_bound)[0])

    def __sigma_2_N(self, delt: float, frequency: float, tempK: float):
        if frequency <= 2 * delt:
            return self.__sigma_2_N_L(delt, frequency, tempK)
        return self.__sigma_2_N_U(delt, frequency, tempK)

    def __Delta_O(self, critical_temp: float):
        return 1.764 * BOLTZMANN_CONSTev * critical_temp

    def __calc_delta(self, critical_temp: float):
        return self.__Delta_O(critical_temp) * math.sqrt(math.cos(PI_DIV_2 * (self.__temp_div ** 2)))

    def __sigma_N(self, delt: float, frequency: float, tempK: float):
        return self.__sigma_1_N(delt, frequency, tempK) - 1j * self.__sigma_2_N(delt, frequency, tempK)

    def __gap_freq(self, delt: float):
        return (2 * delt) / PLANCK_CONSTev

    def __conductivityNormalized(self, frequency: float, operation_temperature_k: float):
        return self.__sigma_N(self.__delta, frequency, operation_temperature_k)

    """
    -INPUTS-
    frequency                    : frequency of DC i units of GHZ
    operation_temperature_k  : the temperature of operation in Kelvin
    critical_temp_k           : the temperature of transition between normal and super conductor in Kelvin
    Pn                      : normal resistivity in micro ohms / cm
    -OUT-
     
    conductivity            : is the conductivity at input conditions
    """

    # @cache
    def conductivity(self, frequency: float):
        return self.__sigma * self.__sigma_N(self.__delta, frequency * PLANCK_CONSTev, self.__op_temp_times_kb)

    """
    -INPUTS-
    frequency          : frequency of DC i units of GHZ
    conductivity  : conductivity
    sc_film_thickness            : thickness of super conductor
    -OUT-
    Zs - surface impedance           
    """

    # @cache
    def surface_impedance_Zs(self, frequency: float, conductivity: float, sc_film_thickness: float):
        return cmath.sqrt(self.__jPI2MU_0 * frequency / conductivity) * ccoth(
            cmath.sqrt(self.__jPI2MU_0 * frequency * conductivity) * sc_film_thickness)

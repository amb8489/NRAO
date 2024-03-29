import cmath
import math

import numpy as np

from simulation.super_conducting_transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.constants import PI, K0, Z0
from simulation.utills.functions import ellip_k

"""


CPW MODEL FOR TRANSMISSION LINE


"""


class CoplanarWaveguideSC(AbstractSCTL):

    def __init__(self, line_width: float, length: float, s_width: float, thickness: float, er: float, tand: float,
                 crit_current):
        self.ncpw = 2

        self.s_width = s_width
        self.thickness = thickness
        self.line_width = line_width
        self.line_length = length
        self.er = er
        self.efm = self.epsilon_fm(er, tand)
        self.g1 = self.__G1(line_width, s_width, thickness)
        self.g2_line, self.g2_ground = self.__G2(self.g1, line_width, s_width, thickness, thickness)
        self.g2_list = [self.g2_ground, self.g2_line]
        self.IC = crit_current * s_width * thickness

    '''
    Equations from:
    
    PARAMETRIC AMPLIFICATION OF ELECTROMAGNETIC SIGNALS WITH SUPERCONDUCTING TRANSMISSION LINES
    TESIS PARA OPTAR AL GRADO DE
    MAGÍSTER EN CIENCIAS DE LA INGENIERÍA, MENCIÓN ELÉCTRICA
    JAVIER ALEJANDRO CARRASCO ÁVILA


    UNIVERSIDAD DE CHILE
    FACULTAD DE CIENCIAS FÍSICAS Y MATEMÁTICAS DEPARTAMENTO DE INGENIERÍA ELÉCTRICA
    
    '''

    def get_length(self):
        return self.line_length

    def get_width(self):
        return self.line_width

    def __G2(self, g1, width, ground_spacing, thickness, thickness_sc):
        a = width / 2

        b = (width + 2 * ground_spacing) / 2

        dsc = thickness_sc / PI

        w1 = a + (dsc / 2) - (dsc / 2) * math.log(dsc / a) + (3 / 2) * dsc * math.log(2) - (dsc / 2) * math.log(
            (a + b) / (b - a))

        w2 = b - (dsc / 2) + (dsc / 2) * math.log(dsc / b) - ((3 / 2) * dsc * math.log(2)) + (dsc / 2) * math.log(
            (a + b) / (b - a))

        k = w1 / w2

        k_prime = math.sqrt(1 - (k * k))

        elliptic_k = ellip_k(k)

        elliptic_k_prime = ellip_k(k_prime)

        log_diff_div = math.log((b - a) / (b + a))

        G2_central_line = (g1 / (8 * elliptic_k * elliptic_k_prime * (1 - (k ** 2)))) * (
                (PI / a) + (1 / a) * math.log((8 * a) / dsc) + (1 / b) * log_diff_div)

        G2_ground_surface = (g1 / (4 * elliptic_k * elliptic_k_prime * (1 - (k ** 2)))) * (
                (PI / b) + (1 / b) * math.log((8 * b) / dsc) + (1 / a) * log_diff_div)

        return [G2_central_line, G2_ground_surface]

    def __G1(self, width, ground_spacing, thickness_sc):
        a = width / 2
        b = (width + 2 * ground_spacing) / 2

        dsc = thickness_sc / PI

        w1 = a + (dsc / 2) - ((dsc / 2) * math.log(dsc / a) + (3 / 2) * dsc * math.log(2)) - (dsc / 2) * math.log(
            (a + b) / (b - a))

        w2 = b - (dsc / 2) + ((dsc / 2) * math.log(dsc / b) - ((3 / 2) * dsc * math.log(2))) + (dsc / 2) * math.log(
            (a + b) / (b - a))

        k = w1 / w2
        k_prime = math.sqrt(1 - k ** 2)

        return ellip_k(k_prime) / (4 * ellip_k(k))

    # todo move functions below into class to tbe in herited from because they are same betwen all lines

    # Zc
    def characteristic_impedance(self, Z, Y):
        return cmath.sqrt(Z / Y)

    # gamma
    def propagation_constant(self, Z, Y):
        return cmath.sqrt(Z * Y)

    def epsilon_fm(self, er, tand):
        return ((er + 1) / 2) * (1 - 1j * tand)

    def shunt_admittance_Y(self, epsilon_fm, g1, f):
        return 1j * (K0(f) / Z0) * (epsilon_fm / g1)

    def series_impedance_Z(self, g1, list_of_g2, list_of_Zs, f):
        assert len(list_of_Zs) == len(list_of_g2), f"should be an equal number of g2 and Zs"
        # return (1j * (K0(f) * Z0) * g1) + (2 * sum(list_of_g2 * list_of_Zs))
        # todo sum(list_of_g2* list_of_Zs) ? same as prev below
        return (1j * (K0(f) * Z0) * g1) + (2 * sum([g2_n * Zs_n for g2_n, Zs_n in zip(list_of_g2, list_of_Zs)]))

    # this will need to be refactored to take some list of Zs to be made general
    def get_gamma_Zc(self, frequency, surface_impedance):
        zs_ground = surface_impedance
        zs_line = surface_impedance
        surface_impedance_list = np.array([zs_line, zs_ground])

        Z = self.series_impedance_Z(self.g1, self.g2_list, surface_impedance_list, frequency)
        Y = self.shunt_admittance_Y(self.efm, self.g1, frequency)

        propagation_constant = cmath.sqrt(Z * Y)
        characteristic_impedance_Zc = cmath.sqrt(Z / Y)
        return propagation_constant, characteristic_impedance_Zc

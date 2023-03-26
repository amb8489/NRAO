import numpy as cmath

from simulation.super_conducting_transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.constants import SPEED_OF_LIGHT, K0, Z0

'''

MICRO STRIP MODEL FOR TRANSMISSION LINE

'''


# ------------------------ JAVIER thesis MS model todo link to thesis

class MicroStripSC(AbstractSCTL):

    def __init__(self, width, length, thickness, height, epsilon_r, tan_delta, crit_current):
        self.__sc_height = height
        self.__line_width = width
        self.__line_length = length
        self.__sc_thickness = thickness
        self.__epsilon_r = epsilon_r
        self.__tan_delta = tan_delta
        self.__IC = crit_current * width * thickness

        # geometric factors
        self.__g1 = self.__G1(self.__line_width, self.__sc_height, self.__sc_thickness)
        self.__g2 = self.__G2(self.__line_width, self.__sc_height, self.__sc_thickness, self.__g1)

    def get_length(self):
        return self.__line_length

    def get_width(self):
        return self.__line_width

    def __G1(self, sc_width, sc_height, sc_thickness):
        ## geometric factor 1:
        b = 1 + sc_thickness / sc_height
        p = 2 * b ** 2 - 1 + 2 * b * cmath.sqrt(b ** 2 - 1)

        ra = cmath.exp(
            -1 - cmath.pi * sc_width / (2 * sc_height) - ((p + 1) / cmath.sqrt(p)) * cmath.arctanh(
                1 / cmath.sqrt(p))) * 4 * p / (
                     p - 1)

        Lambda = cmath.sqrt(p) * (
                cmath.pi * sc_width / (2 * sc_height) + (1 + cmath.log(4 / (p - 1))) * (p + 1) / (
                2 * cmath.sqrt(p)) - 2 * cmath.arctanh(
            1 / cmath.sqrt(p)))
        Gamma = max(Lambda, p)
        rb0 = Lambda + (p + 1) * cmath.log(Gamma) / 2

        w_h_ratio = sc_width / sc_height
        if w_h_ratio >= 5:
            rb = rb0
        else:
            rb = rb0 - cmath.sqrt((rb0 - 1) * (rb0 - p)) + (p + 1) * cmath.arctanh(cmath.sqrt((rb0 - p) / (rb0 - 1))) \
                 - 2 * cmath.sqrt(p) * cmath.arctanh(cmath.sqrt((rb0 - p) / (p * (rb0 - 1)))) + cmath.pi * cmath.sqrt(
                p) * sc_width / (
                         2 * sc_height)

        g1 = (cmath.pi / 2) / (cmath.log(2 * rb / ra))
        return g1

    # todo could refactor into get g1 and g2 in same fucntion to reduce repeated code
    def __G2(self, sc_width, sc_height, sc_thickness, g1):
        ## geometric factor 1:

        b = 1 + sc_thickness / sc_height
        p = 2 * b ** 2 - 1 + 2 * b * cmath.sqrt(b ** 2 - 1)

        ra = cmath.exp(
            -1 - cmath.pi * sc_width / (2 * sc_height) - ((p + 1) / cmath.sqrt(p)) * cmath.arctanh(
                1 / cmath.sqrt(p))) * 4 * p / (
                     p - 1)

        Lambda = cmath.sqrt(p) * (
                cmath.pi * sc_width / (2 * sc_height) + (1 + cmath.log(4 / (p - 1))) * (p + 1) / (
                2 * cmath.sqrt(p)) - 2 * cmath.arctanh(
            1 / cmath.sqrt(p)))
        Gamma = max(Lambda, p)
        rb0 = Lambda + (p + 1) * cmath.log(Gamma) / 2

        w_h_ratio = sc_width / sc_height
        if w_h_ratio >= 5:
            rb = rb0
        else:
            rb = rb0 - cmath.sqrt((rb0 - 1) * (rb0 - p)) + (p + 1) * cmath.arctanh(cmath.sqrt((rb0 - p) / (rb0 - 1))) \
                 - 2 * cmath.sqrt(p) * cmath.arctanh(cmath.sqrt((rb0 - p) / (p * (rb0 - 1)))) + cmath.pi * cmath.sqrt(
                p) * sc_width / (
                         2 * sc_height)

        ## geometric factor 2:
        I_l = cmath.log((2 * p + 2 * cmath.sqrt(p * (1 - ra) * (p - ra)) - (p + 1) * ra) / (ra * (p - 1)))
        if w_h_ratio < 2:
            K_MS = 2 * sc_height * cmath.log(rb / ra)
        else:
            K_MS = 2 * sc_height * cmath.log(2 * rb / ra)

        psi_l = (I_l + cmath.pi / 2) / K_MS

        g2 = psi_l * g1  # [g2] = [psi] = 1/length

        return g2

    # --------------------------------------------------------------------------------------------------------------

    # todo this could be done in numpy by having a list of frequencies
    def efm(self, frequency, er, tand, sc_height, sc_width):

        # From Pozar's book (eq. 3.195, PDF page 148):
        eps_fm_static = (er + 1) / 2 + (er - 1) / (2 * cmath.sqrt(1 + 12 * sc_height / sc_width))

        # From Roberto Sorretino's book (referencing Yamashita [13] at eq. 3.186, page 100 of PDF):
        F_1_nu = (4 * sc_height * frequency / SPEED_OF_LIGHT) * cmath.sqrt(er - 1) * (
                0.5 + (1 + 2 * cmath.log(1 + sc_width / sc_height)) ** 2)
        eps_fm_nu = ((cmath.sqrt(er) - cmath.sqrt(eps_fm_static)) / (1 + 4 * F_1_nu ** (-1.5)) + cmath.sqrt(
            eps_fm_static)) ** 2

        return eps_fm_nu * (1 - 1j * tand)

    def series_impedance_Z(self, Zs, g1, g2, f):
        return (1j * (K0(f) * Z0) * g1) + (2 * g2 * Zs)

    def shunt_admittance_Y(self, g1, f, er, tand, sc_hight, sc_width):
        return 1j * (K0(f) / Z0) * (self.efm(f, er, tand, sc_hight, sc_width) / g1)

    def characteristic_impedance(self, Z, Y):
        return cmath.sqrt(Z / Y)

    def propagation_constant(self, Z, Y):
        return cmath.sqrt(Z * Y)

    def get_gamma_Zc(self, frequency, surface_impedance):
        Z = self.series_impedance_Z(surface_impedance, self.__g1, self.__g2, frequency)
        Y = self.shunt_admittance_Y(self.__g1, frequency, self.__epsilon_r, self.__tan_delta, self.__sc_height,
                                    self.__line_width)

        propagation_constant = self.propagation_constant(Z, Y)
        characteristic_impedance_Zc = self.characteristic_impedance(Z, Y)
        return propagation_constant, characteristic_impedance_Zc

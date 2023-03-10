import cmath
import numpy as np

from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.constants import C, K0, Z0

'''

MICRO STRIP MODEL FOR TRANSMISSION LINE

'''


# ------------------------ JAVIER thesis MS model

class SuperConductingMicroStripModel(AbstractSCTL):

    def __init__(self, height, width, thickness, epsilon_r, tan_delta, crit_current):
        self.sc_height = height
        self.sc_width = width
        self.sc_thickness = thickness
        self.epsilon_r = epsilon_r
        self.tan_delta = tan_delta

        self.IC = crit_current * width*thickness

        # calc geometric factors
        self.g1 = self.__G1(self.sc_width, self.sc_height, self.sc_thickness)
        self.g2 = self.__G2(self.sc_width, self.sc_height, self.sc_thickness, self.g1)

    def __G1(self, sc_width, sc_height, sc_thickness):
        ## geometric factor 1:
        b = 1 + sc_thickness / sc_height
        p = 2 * b ** 2 - 1 + 2 * b * np.sqrt(b ** 2 - 1)

        ra = np.exp(
            -1 - np.pi * sc_width / (2 * sc_height) - ((p + 1) / np.sqrt(p)) * np.arctanh(1 / np.sqrt(p))) * 4 * p / (
                     p - 1)

        Lambda = np.sqrt(p) * (
                np.pi * sc_width / (2 * sc_height) + (1 + np.log(4 / (p - 1))) * (p + 1) / (
                2 * np.sqrt(p)) - 2 * np.arctanh(
            1 / np.sqrt(p)))
        Gamma = max(Lambda, p)
        rb0 = Lambda + (p + 1) * np.log(Gamma) / 2

        w_h_ratio = sc_width / sc_height
        if w_h_ratio >= 5:
            rb = rb0
        else:
            rb = rb0 - np.sqrt((rb0 - 1) * (rb0 - p)) + (p + 1) * np.arctanh(np.sqrt((rb0 - p) / (rb0 - 1))) \
                 - 2 * np.sqrt(p) * np.arctanh(np.sqrt((rb0 - p) / (p * (rb0 - 1)))) + np.pi * np.sqrt(p) * sc_width / (
                         2 * sc_height)

        g1 = (np.pi / 2) / (np.log(2 * rb / ra))
        return g1

    def __G2(self, sc_width, sc_height, sc_thickness, g1):
        ## geometric factor 1:

        b = 1 + sc_thickness / sc_height
        p = 2 * b ** 2 - 1 + 2 * b * np.sqrt(b ** 2 - 1)

        ra = np.exp(
            -1 - np.pi * sc_width / (2 * sc_height) - ((p + 1) / np.sqrt(p)) * np.arctanh(1 / np.sqrt(p))) * 4 * p / (
                     p - 1)

        Lambda = np.sqrt(p) * (
                np.pi * sc_width / (2 * sc_height) + (1 + np.log(4 / (p - 1))) * (p + 1) / (
                2 * np.sqrt(p)) - 2 * np.arctanh(
            1 / np.sqrt(p)))
        Gamma = max(Lambda, p)
        rb0 = Lambda + (p + 1) * np.log(Gamma) / 2

        w_h_ratio = sc_width / sc_height
        if w_h_ratio >= 5:
            rb = rb0
        else:
            rb = rb0 - np.sqrt((rb0 - 1) * (rb0 - p)) + (p + 1) * np.arctanh(np.sqrt((rb0 - p) / (rb0 - 1))) \
                 - 2 * np.sqrt(p) * np.arctanh(np.sqrt((rb0 - p) / (p * (rb0 - 1)))) + np.pi * np.sqrt(p) * sc_width / (
                         2 * sc_height)

        ## geometric factor 2:
        I_l = np.log((2 * p + 2 * np.sqrt(p * (1 - ra) * (p - ra)) - (p + 1) * ra) / (ra * (p - 1)))
        if w_h_ratio < 2:
            K_MS = 2 * sc_height * np.log(rb / ra)
        else:
            K_MS = 2 * sc_height * np.log(2 * rb / ra)

        psi_l = (I_l + np.pi / 2) / K_MS

        g2 = psi_l * g1  # [g2] = [psi] = 1/length

        return g2

    # --------------------------------------------------------------------------------------------------------------

    # todo this could be done in numpy by having a list of frequencies
    def efm(self, frequency, er, tand, sc_height, sc_width):

        # From Pozar's book (eq. 3.195, PDF page 148):
        eps_fm_static = (er + 1) / 2 + (er - 1) / (2 * np.sqrt(1 + 12 * sc_height / sc_width))

        # From Roberto Sorretino's book (referencing Yamashita [13] at eq. 3.186, page 100 of PDF):
        F_1_nu = (4 * sc_height * frequency / C) * np.sqrt(er - 1) * (
                0.5 + (1 + 2 * np.log(1 + sc_width / sc_height)) ** 2)
        eps_fm_nu = ((np.sqrt(er) - np.sqrt(eps_fm_static)) / (1 + 4 * F_1_nu ** (-1.5)) + np.sqrt(
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

    def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
        Z = self.series_impedance_Z(surface_impedance, self.g1, self.g2, frequency)
        Y = self.shunt_admittance_Y(self.g1, frequency, self.epsilon_r, self.tan_delta, self.sc_height, self.sc_width)

        propagation_constant = self.propagation_constant(Z, Y)
        characteristic_impedance_Zc = self.characteristic_impedance(Z, Y)
        return propagation_constant, characteristic_impedance_Zc

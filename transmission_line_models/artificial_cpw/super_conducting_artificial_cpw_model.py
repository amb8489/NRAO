import cmath
import math

import numpy as np

from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from transmission_line_models.artificial_cpw.artificial_cpw_capacitance import capacitance_model_selector
from transmission_line_models.artificial_cpw.zc_gamma import characteristic_impedance_wt, gamma_wt
from utills.constants import C, PI2, KB, PI, MU_0, PLANCK_CONST_REDUCEDev

"""


CPW MODEL FOR TRANSMISSION LINE


"""


def DELTA_O(sc_crit_temp):
    return 1.764 * KB * sc_crit_temp


def lambda_0(sigma_n, delta_o):
    return math.sqrt(PLANCK_CONST_REDUCEDev / (PI * MU_0 * sigma_n * delta_o))


class SuperConductingArtificialCPWLine(AbstractSCTL):

    def __init__(self,
                 central_line_length_LH: float,
                 central_line_width_WH: float,
                 load_length_LL: float,
                 load_width_WL: float,
                 S: float,
                 number_of_finger_sections: int,
                 epsilon_r: float,
                 thickness: float,
                 height: float,
                 Tc,
                 normal_conductivity,
                 total_line_length=None):
        self.central_line_length_LH = central_line_length_LH
        self.central_line_width_WH = central_line_width_WH
        self.load_length_LL = load_length_LL
        self.load_width_WL = load_width_WL
        self.S = S
        self.number_of_finger_sections = number_of_finger_sections
        self.epsilon_r = epsilon_r
        self.thickness = thickness
        self.height = height
        self.nfb = number_of_finger_sections
        self.Lu = self.central_line_length_LH + S + load_length_LL + S

        self.total_line_length = self.Lu * number_of_finger_sections#todo is this nf or nfb

        self.lambda_O = lambda_0(normal_conductivity, DELTA_O(Tc))

        if total_line_length:

            self.number_of_finger_sections = total_line_length // self.Lu
            self.total_line_length = number_of_finger_sections * self.Lu

            print("calculating number_of_finger_sections based om line length and Lu")

            if self.number_of_finger_sections < 1:
                raise Exception("Lu is greater than total line length")

        lg = ((self.load_width_WL - self.central_line_width_WH) / 2) - self.S

        print("lg :", lg)
        nf = 2 * self.nfb + 1

        self.capacitance = self.calc_capacitance(nf, epsilon_r, S / 2, S / 2, S / 2, 10 * S, height, lg, thickness,
                                                 model_type=1)

        print("capacitance:", self.capacitance)

    def __L_aprox(self, Zo, beta_so, l):
        return Zo * beta_so * (l / C)

    def __clac_L1_L2(self, lH, lL: float, wL: float, wH: float, sM: float, s: float, t: float):

        # looking for errors in these functions

        zH = characteristic_impedance_wt(self.lambda_O, self.epsilon_r, wH, s, t)
        print("ZH", zH)
        beta_wtH = gamma_wt(self.lambda_O, self.epsilon_r, wH, s, t)
        LH = self.__L_aprox(zH, beta_wtH, lH)

        zL = characteristic_impedance_wt(self.lambda_O, self.epsilon_r, wL, s, t)
        beta_wtL = gamma_wt(self.lambda_O, self.epsilon_r, wL, s, t)
        LL = self.__L_aprox(zL, beta_wtL, lL)

        zM = characteristic_impedance_wt(self.lambda_O, self.epsilon_r, wH, sM, t)
        beta_wtM = gamma_wt(self.lambda_O, self.epsilon_r, wH, sM, t)
        LM = self.__L_aprox(zM, beta_wtM, s)

        print("LL: ", LL)
        print("LM: ", LM)

        return LL + LM, LH + LM

    # good
    def propagation_constant(self, L1: float, L2: float, capacitance: float, omega: float):
        return 2 * np.arcsinh(
            1 / 2 * cmath.sqrt(-capacitance * omega ** 2 * (-3 + capacitance * L1 * omega ** 2) * (
                    -2 * L1 - L2 + capacitance * L1 * L2 * omega ** 2)))

    # good
    def characteristic_impedance(self, L1: float, L2: float, capacitance: float, omega: float):
        return (2j * omega * (-1 + capacitance * L1 * omega ** 2) * (
                -L2 + L1 * (-2 + capacitance * L2 * omega ** 2))) / (
                       cmath.sqrt(-capacitance * omega ** 2 * (-3 + capacitance * L1 * omega ** 2) * (
                               -L2 + L1 * (-2 + capacitance * L2 * omega ** 2))) *
                       cmath.sqrt(-(-1 + capacitance * L1 * omega ** 2) * (
                               4 + capacitance * omega ** 2 * (-3 * L2 + L1 * (-2 + capacitance * L2 * omega ** 2)))))

    def calc_capacitance(self, n, epsilon_r, sg, s1, gg, gendg, h: float, l: float, t: float, model_type: int = 1):
        return capacitance_model_selector(n, epsilon_r, sg, s1, gg, gendg, h, l, t, model_type=model_type)

    def get_propagation_constant_characteristic_impedance(self, frequency):

        print("------------------------------------")
        print("nfb:", self.nfb)
        print("er:", self.epsilon_r)
        print("s:", self.S)
        print("wH:", self.central_line_width_WH)
        print("lH:", self.central_line_length_LH)
        print("wL:", self.load_width_WL)
        print("lL:", self.load_length_LL)
        print("h:", self.height)
        print("t:", self.thickness)
        print("fopr:", frequency)
        print("------------------------------------")

        delta_z = 3 * self.S + 2 * self.load_length_LL + self.central_line_length_LH

        print("delta_z:", delta_z)

        sM = ((self.load_width_WL - self.central_line_width_WH) / 2) + self.S
        print("sM:", sM)

        frequency_operation = frequency

        omega = PI2 * frequency_operation
        print("omega:", omega)

        # good to this point including capacitance model 1

        # issue is in __clac_L1 and or in __clac_L2

        L1, L2 = self.__clac_L1_L2(self.central_line_length_LH, self.load_length_LL, self.load_width_WL,
                                   self.central_line_width_WH,
                                   sM, self.S, self.thickness)

        print("L1:", L1)
        print("L2:", L2)

        # these are good
        propagation_constant = self.propagation_constant(L1, L2, 2 * self.capacitance, omega)
        characteristic_impedance_Zc = self.characteristic_impedance(L1, L2, 2 * self.capacitance, omega)

        return (propagation_constant / delta_z).imag, characteristic_impedance_Zc.real

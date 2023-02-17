import numpy as np

from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from transmission_line_models.artificial_cpw.artificial_cpw_capacitance import capacitance_model_selector
from transmission_line_models.artificial_cpw.zc_gamma import charateristic_impedance_wt, gamma_wt
from utills.constants import C, PI2

"""


CPW MODEL FOR TRANSMISSION LINE


"""


class SuperConductingArtificialCPWLine(AbstractSCTL):

    def __init__(self,
                 finger_central_line_length_LH: float,
                 finger_central_line_width_WH: float,
                 finger_load_length_LL: float,
                 finger_load_width_WL: float,
                 S: float,
                 number_of_fingers: int,
                 epsilon_r: float,
                 thickness: float,
                 height: float):
        self.finger_central_line_length_LH = finger_central_line_length_LH
        self.finger_central_line_width_WH = finger_central_line_width_WH
        self.finger_load_length_LL = finger_load_length_LL
        self.finger_load_width_WL = finger_load_width_WL
        self.unit_total_length_Lu = finger_central_line_length_LH + 2 * S + finger_load_length_LL
        self.S = S
        self.number_of_fingers = number_of_fingers
        self.epsilon_r = epsilon_r
        self.thickness = thickness
        self.height = height

        lg = ((self.finger_load_width_WL + self.finger_central_line_width_WH) / 2) - self.S

        nf = 2 * number_of_fingers + 1

        self.capacitance = self.calc_capacitance(nf, epsilon_r, S / 2, S / 2, S / 2, 10 * S, height, lg, thickness,
                                                 model_type=1)

    def __L_aprox(self, Zo, beta_so, l):
        return (Zo * beta_so * l) / C

    def __clac_L1(self, lL: float, wL: float, wH: float, sM: float, s: float, t: float):
        # calculation of LL
        LL_characteristic_impedance_sc_cpw = charateristic_impedance_wt(wL, s, t)
        LL_propagation_const_sc_cpw = gamma_wt(wL, s, t)
        LL = self.__L_aprox(LL_characteristic_impedance_sc_cpw, LL_propagation_const_sc_cpw, lL)

        # calculation of LM we can factor this out to its own function
        LM_characteristic_impedance_sc_cpw = charateristic_impedance_wt(wH, sM, t)
        LM_propagation_const_sc_cpw = gamma_wt(wH, sM, t)
        LM = self.__L_aprox(LM_characteristic_impedance_sc_cpw, LM_propagation_const_sc_cpw, s)

        return LL + LM

    def __clac_L2(self, lH, wH, sM, s, t):
        # calc of LH
        LH_characteristic_impedance_sc_cpw = charateristic_impedance_wt(wH, s, t)
        LH_propagation_const_sc_cpw = gamma_wt(wH, s, t)
        LH = self.__L_aprox(LH_characteristic_impedance_sc_cpw, LH_propagation_const_sc_cpw, lH)

        # calculation of LM we can factor this out to its own function
        LM_characteristic_impedance_sc_cpw = charateristic_impedance_wt(wH, sM, t)
        LM_propagation_const_sc_cpw = gamma_wt(wH, sM, t)
        LM = self.__L_aprox(LM_characteristic_impedance_sc_cpw, LM_propagation_const_sc_cpw, s)

        return LH + LM

    # todo check
    def propagation_constant(self, L1: float, L2: float, capacitance: float, omega: float):
        return 2 * np.arcsinh(
            1 / 2 * np.sqrt(-capacitance * omega ** 2 * (-3 + capacitance * L1 * omega ** 2) * (
                    -2 * L1 - L2 + capacitance * L1 * L2 * omega ** 2)))

    # todo check
    def characteristic_impedance(self, L1: float, L2: float, capacitance: float, omega: float):
        return (2j * omega * (-1 + capacitance * L1 * omega ** 2) * (
                -L2 + L1 * (-2 + capacitance * L2 * omega ** 2))) / (
                       np.sqrt(-capacitance * omega ** 2 * (-3 + capacitance * L1 * omega ** 2) * (
                               -L2 + L1 * (-2 + capacitance * L2 * omega ** 2))) *
                       np.sqrt(-(-1 + capacitance * L1 * omega ** 2) * (
                               4 + capacitance * omega ** 2 * (-3 * L2 + L1 * (-2 + capacitance * L2 * omega ** 2)))))

    def calc_capacitance(self, n, epsilon_r, sg, s1, gg, gendg, h: float, l: float, t: float, model_type: int = 1):
        return capacitance_model_selector(model_type, n, epsilon_r, sg, s1, gg, gendg, h, l, t)

    def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
        delta_z = 3 * self.S + 2 * self.finger_load_length_LL + self.finger_central_line_length_LH

        sM = ((self.finger_load_width_WL + self.finger_central_line_width_WH) / 2) + self.S

        frequency_operation = ...

        omega = PI2 * frequency_operation

        L1 = self.__clac_L1(self.finger_load_length_LL, self.finger_load_width_WL, self.finger_central_line_width_WH,
                            sM, self.S, self.thickness)
        L2 = self.__clac_L2(self.finger_central_line_length_LH, self.finger_central_line_width_WH, sM, self.S,
                            self.thickness)

        propagation_constant = self.propagation_constant(L1, L2, 2 * self.capacitance, omega)
        characteristic_impedance_Zc = self.characteristic_impedance(L1, L2, 2 * self.capacitance, omega)

        return propagation_constant / delta_z, characteristic_impedance_Zc

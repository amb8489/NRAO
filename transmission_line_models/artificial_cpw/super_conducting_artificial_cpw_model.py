import numpy as np

from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from transmission_line_models.artificial_cpw.artificial_cpw_capacitance import capacitance_model_selector
from transmission_line_models.artificial_cpw.zc_gamma import zwt, gamma_wt
from utills.constants import C, PI2

"""


CPW MODEL FOR TRANSMISSION LINE


"""


class SuperConductingArtificialCPWLine(AbstractSCTL):

    def __init__(self, finger_width, finger_length, finger_spacing, central_line_width, number_of_fingers,
                 ground_spacing, epsilon_r):
        self.finger_width = finger_width
        self.finger_length = finger_length
        self.finger_spacing = finger_spacing
        self.central_line_width = central_line_width
        self.number_of_fingers = number_of_fingers
        self.ground_spacing = ground_spacing
        self.epsilon_r = epsilon_r

        self.capacitance = self.calc_capacitance(number_of_fingers, self.epsilon_r, sg, s1, gg, gendg, height, finger_length, thickness )

    # step 1
    def dimension_to_circuit(self):
        pass

    # todo check
    def propagation_constant(self, L1, L2, capacitance, omega):
        return 2 * np.arcsinh(
            1 / 2 * np.sqrt(
                -capacitance * omega ** 2 * (-3 + capacitance * L1 * omega ** 2) * (
                        -2 * L1 - L2 + capacitance * L1 * L2 * omega ** 2)))

    # todo check
    def characteristic_impedance(self, L1, L2, C1, omega):
        return (2j * omega * (-1 + C1 * L1 * omega ** 2) * (-L2 + L1 * (-2 + C1 * L2 * omega ** 2))) / (
                np.sqrt(-C1 * omega ** 2 * (-3 + C1 * L1 * omega ** 2) * (-L2 + L1 * (-2 + C1 * L2 * omega ** 2))) *
                np.sqrt(-(-1 + C1 * L1 * omega ** 2) * (
                        4 + C1 * omega ** 2 * (-3 * L2 + L1 * (-2 + C1 * L2 * omega ** 2)))))

    def L_aprox(self, Zo, beta_so, l):
        return (Zo * beta_so * l) / C

    def calc_capacitance(self, n, epsilon_r, sg, s1, gg, gendg, h, l, t, model_type=1):
        return capacitance_model_selector(model_type, n, epsilon_r, sg, s1, gg, gendg, h, l, t)

    def clac_L1(self, length, wL, wH, sM, s, t):
        # calculation of LL

        LL_characteristic_impedance_sc_cpw = zwt(wL, s, t)
        LL_propagation_const_sc_cpw = gamma_wt(wL, s, t)
        LL = self.L_aprox(LL_characteristic_impedance_sc_cpw, LL_propagation_const_sc_cpw, length)

        # calculation of LM we can factor this out to its own function
        LM_characteristic_impedance_sc_cpw = zwt(wH, sM, t)
        LM_propagation_const_sc_cpw = gamma_wt(wH, sM, t)
        LM = self.L_aprox(LM_characteristic_impedance_sc_cpw, LM_propagation_const_sc_cpw, s)

        return LL + LM

    def clac_L2(self, height, spacing, wH, sM, s, t):
        # calc of LH
        LH_characteristic_impedance_sc_cpw = zwt(wH, s, t)
        LH_propagation_const_sc_cpw = gamma_wt(wH, s, t)
        LH = self.L_aprox(LH_characteristic_impedance_sc_cpw, LH_propagation_const_sc_cpw,
                          height)  # todo make sure this is height

        # calc of LM we can factor this out to its own function
        LM_characteristic_impedance_sc_cpw = zwt(wH, sM, t)
        LM_propagation_const_sc_cpw = gamma_wt(wH, sM, t)
        LM = self.L_aprox(LM_characteristic_impedance_sc_cpw, LM_propagation_const_sc_cpw,
                          spacing)  # todo make sure this is height

        return LH + LM

    def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
        L1 = self.clac_L1()
        L2 = self.clac_L2()

        propagation_constant = self.propagation_constant(L1, L2, 2 * self.capacitance, PI2 * frequency)
        characteristic_impedance_Zc = self.characteristic_impedance(L1, L2, 2 * self.capacitance, PI2 * frequency)

        return propagation_constant, characteristic_impedance_Zc
